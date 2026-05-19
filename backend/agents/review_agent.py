from collections import Counter
from difflib import SequenceMatcher

from models.agent_schema import AgentOutput
from models.product_schema import Product

GENERIC_ENGLISH_PHRASES = ("very good", "amazing", "fast delivery", "fast shipping", "recommend")

GENERIC_TURKISH_PHRASES = (
    "çok güzel", "cok guzel", "tavsiye ederim", "mükemmel", "mukemmel",
    "harika", "süper", "super", "teşekkürler", "tesekkurler",
    "güzel ürün", "guzel urun", "kaliteli", "beğendim", "begendim",
    "hızlı geldi", "hizli geldi", "sağlam", "saglam", "fiyatına göre",
    "fiyatina gore", "tam istediğim", "tam istedigim", "iyi ürün",
)
REPEAT_BUY_PHRASES = (
    # tekrar satın alma
    "sürekli alıyorum", "surekli aliyorum",
    "hep alıyorum", "hep aliyorum",
    "devamlı alıyorum", "devamli aliyorum",
    "düzenli alıyorum", "duzenli aliyorum",
    "her zaman alırım", "her zaman alirim",
    "kaçıncı alışım", "kacinci alisim",
    "kaçıncı kez aldım", "kacinci kez aldim",
    "tekrar aldım", "tekrar aldim",
    "yeniden aldım", "yeniden aldim",
    "bir daha aldım", "bir daha aldim",
    "tekrar sipariş verdim", "tekrar siparis verdim",
    "yeniden sipariş verdim", "yeniden siparis verdim",

    # çoklu satın alma
    "iki tane aldım", "iki tane aldim",
    "3 tane aldım", "3 tane aldim",
    "üç tane aldım", "uc tane aldim",
    "4 tane aldım", "4 tane aldim",
    "dört tane aldım", "dort tane aldim",
    "birkaç tane aldım", "birkac tane aldim",
    "birden fazla aldım", "birden fazla aldim",
    "anneme de aldım", "anneme de aldim",
    "kardeşime de aldım", "kardesime de aldim",
    "arkadaşıma da aldım", "arkadasima da aldim",
    "hediye aldım", "hediye aldim",

    # stoklama
    "stok yaptım", "stok yaptim",
    "stokladım", "stokladim",
    "stok yapıyorum", "stok yapiyorum",
    "stoklamalık", "stoklamalik",
    "yedek aldım", "yedek aldim",
    "bitmeden alıyorum", "bitmeden aliyorum",
    "bittikçe alıyorum", "bittikce aliyorum",
    "indirime girince alıyorum", "indirime girince aliyorum",

    # sıra/kez ifadeleri
    "ikinci kez",
    "2. kez",
    "üçüncü kez", "ucuncu kez",
    "3. kez",
    "dördüncü kez", "dorduncu kez",
    "4. kez",
    "beşinci kez", "besinci kez",
    "5. kez",
    "defalarca aldım", "defalarca aldim",
    "kaç kere aldım", "kac kere aldim",
)
NON_CONSUMABLE_KEYWORDS = (
    # ev / tekstil / dekorasyon
    "yastık", "yastik", "kırlent", "kirlent", "nevresim", "çarşaf", "carsaf",
    "battaniye", "halı", "hali", "kilim", "perde", "masa", "sandalye",
    "tablo", "ayna", "abajur", "avize", "lamba", "vazo", "raf",

    # aksesuar
    "çanta", "canta", "cüzdan", "cuzdan", "kemer", "saat",
    "gözlük", "gozluk", "bileklik", "kolye", "küpe", "kupe", "yüzük", "yuzuk",
    "şapka", "sapka", "bere", "atkı", "atki", "eldiven",

    # ayakkabı / giyim kalıcı ürünler
    "ayakkabı", "ayakkabi", "bot", "çizme", "cizme", "sneaker",
    "mont", "ceket", "kaban", "palto", "trençkot", "trenckot",
    "elbise", "pantolon", "gömlek", "gomlek",

    # kişisel bakım ama tüketilemeyen araçlar
    "tarak", "fırça", "firca", "makyaj fırçası", "makyaj fircasi",
    "saç fırçası", "sac fircasi", "düzleştirici", "duzlestirici",
    "maşa", "masa", "tıraş makinesi", "tiras makinesi",
    "epilatör", "epilator",

    # telefon / elektronik aksesuar
    "kılıf", "kilif", "kapak", "stand", "askı", "aski",
    "telefon tutucu", "tablet kılıfı", "tablet kilifi",
    "kulaklık", "kulaklik", "klavye", "mouse", "hoparlör", "hoparlor",
    "şarj aleti", "sarj aleti", "powerbank",

    # mutfak / ev eşyası
    "tencere", "tava", "tabak", "bardak", "kupa", "çatal", "catal",
    "kaşık", "kasik", "bıçak", "bicak", "saklama kabı", "saklama kabi",
    "termos", "matara",

    # oyuncak / hobi
    "oyuncak", "lego", "puzzle", "kitap", "defter", "kalem",
)
def _is_nonsensical_repeat_buy(review_text: str, product_name: str) -> bool:
    """Ürün tüketilemez türdeyse 'sürekli alıyorum' tarzı yorumları yakala."""
    text_lower = review_text.lower()
    product_lower = product_name.lower() if product_name else ""

    has_repeat = any(phrase in text_lower for phrase in REPEAT_BUY_PHRASES)
    if not has_repeat:
        return False

    is_non_consumable = any(
        kw in product_lower or kw in text_lower
        for kw in NON_CONSUMABLE_KEYWORDS
    )
    return is_non_consumable


def _is_too_short(text: str) -> bool:
    words = text.strip().split()
    return len(words) <= 3


def _is_generic(text: str) -> bool:
    text_lower = text.lower()
    return any(phrase in text_lower for phrase in GENERIC_TURKISH_PHRASES + GENERIC_ENGLISH_PHRASES)

def analyze_review_risk(product: Product) -> AgentOutput:
    stats = product.review_stats

    # Genel rating dağılımı güvenilir mi?
    reliable_global_rating = (
        stats.average_rating is not None
        and stats.total_rating_count is not None
        and stats.total_rating_count >= 100
    )
    reviews = product.reviews
    if not reviews:
        return AgentOutput(
            agent_name="Review Risk Agent",
            risk_score=35,
            reason_codes=["MISSING_REVIEWS"],
            evidence=["Urun yorumu bulunamadi.Bu durum doğrudan risk değil, analiz kapsamını sınırlar."],
            missing_fields=["reviews"],
        )

    risk = 0
    reason_codes: list[str] = []
    evidence: list[str] = []
    most_common_date = None
    date_count = 0
    burst_ratio = 0


    # 1. Yorum patlaması (aynı gün 3+ yorum)
    dates = [str(r.date) for r in reviews if r.date]
    if dates:
        most_common_date, date_count = Counter(dates).most_common(1)[0]
        burst_ratio = date_count / len(reviews)

    # burst koşulunu ayrı değerlendir (dates boş olsa da güvenli)
    if date_count and len(reviews) >= 20 and burst_ratio >= 0.35:
        risk += 20
        reason_codes.append("REVIEW_BURST")
        # most_common_date genellikle string olarak ayarlandı (str(r.date))
        evidence.append(
            f"İncelenen yorumların %{int(burst_ratio * 100)} kadarı aynı tarihte ({most_common_date}) toplanmış görünüyor."
        )
    # 2. Birbirine benzer yorumlar
    texts = [review.text.lower() for review in reviews]
    similar_pairs = 0
    for index, text in enumerate(texts):
        for other in texts[index + 1:]:
            if SequenceMatcher(None, text, other).ratio() >= 0.72:
                similar_pairs += 1
    if similar_pairs:
        risk += 35
        reason_codes.append("SIMILAR_REVIEWS")
        evidence.append(f"{similar_pairs} yorum cifti birbirine yuksek benzerlik gosteriyor.")

    # 3. Generic/anlamsız kısa yorumlar
    weak_count = sum(_is_generic(t) or _is_too_short(t) for t in texts)
    weak_ratio = weak_count/ len(reviews)

    if weak_ratio >= 0.5:
        risk += 25
        reason_codes.append("GENERIC_SHORT_REVIEWS")
        evidence.append(
            f"Yorumlarin %{int(weak_ratio * 100)}'i cok kisa veya genel ifadeler iceriyor."
        )
    elif weak_ratio >= 0.3:
        risk += 10
        reason_codes.append("GENERIC_SHORT_REVIEWS")
        evidence.append("Yorumlarin onemli bir kismi genel veya kisa ifadelerden olusuyor.")

    # 4. Ürünle mantıksız tekrar alım yorumları
    nonsensical_count = sum(
        _is_nonsensical_repeat_buy(r.text, product.name or "")
        for r in reviews
    )
    if nonsensical_count >= 1:
        risk += 30
        reason_codes.append("NONSENSICAL_REPEAT_BUY")
        evidence.append(
            f"{nonsensical_count} yorumda tuketilemez urun icin 'surekli aliyorum' tarzı ifade var."
        )

    # 5. 5 yıldız oranı — tek başına değil, diğer sinyallerle birlikte değerlendir
    five_star_count = sum(1 for r in reviews if r.rating == 5)
    five_star_ratio = five_star_count / len(reviews) if reviews else 0

    supporting_signals = sum(
        code in reason_codes
        for code in [
            "REVIEW_BURST",
            "SIMILAR_REVIEWS",
            "GENERIC_SHORT_REVIEWS",
            "NONSENSICAL_REPEAT_BUY",
        ]
    )

    if five_star_ratio > 0.85 and supporting_signals >= 2:
        reason_codes.append("HIGH_RATING_WITH_MANIPULATION_SIGNALS")
        evidence.append(
            "5 yıldız oranı yüksek ve yorumlarda başka şüpheli paternler de bulundu."
        )
    return AgentOutput(
        agent_name="Review Risk Agent",
        risk_score=min(risk, 100),
        reason_codes=reason_codes,
        evidence=evidence,
        missing_fields=[],
    )
