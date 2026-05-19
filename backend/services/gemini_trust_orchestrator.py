import json
import os
import time

import google.generativeai as genai
from models.agent_schema import AgentOutput
from models.product_schema import Product
from models.response_schema import GeminiExplanation

_last_call_time = 0.0
GEMINI_MIN_INTERVAL = 1.0  # saniye — rate limit koruması

def get_api_keys():
    keys = []
    if os.getenv("GEMINI_API_KEY"):
        keys.append(os.getenv("GEMINI_API_KEY"))
    for i in range(1, 10):
        k = os.getenv(f"GEMINI_API_KEY_{i}")
        if k:
            keys.append(k)
    return list(dict.fromkeys(keys))


def build_trust_explanation(product: Product, agent_outputs: list[AgentOutput]) -> GeminiExplanation:
    global _last_call_time
    elapsed = time.time() - _last_call_time
    if elapsed < GEMINI_MIN_INTERVAL:
        time.sleep(GEMINI_MIN_INTERVAL - elapsed)
    _last_call_time = time.time()
    api_keys = get_api_keys()
    if not api_keys:
        return _fallback_explanation(product, [], 50.0)

    from services.rule_engine import calculate_rule_risk
    rule_risk = calculate_rule_risk(agent_outputs)

    missing_fields = sorted({field for output in agent_outputs for field in output.missing_fields})
    reason_codes = sorted({code for output in agent_outputs for code in output.reason_codes})
    evidence = [item for output in agent_outputs for item in output.evidence]

    # Ham yorum metinlerini Gemini'ye ver — asıl değer burada
    review_samples = [
        f"[{review.rating}★] {review.text[:200]}"
        for review in (product.reviews or [])[:15]
    ]

    # review_stats varsa özet bilgileri ekle
    stats = getattr(product, "review_stats", None)
    stats_text = ""
    if stats and stats.total_rating_count and stats.total_rating_count > 0:
        stats_text = (
            f"Global Ortalama: {stats.average_rating} | "
            f"Toplam Rating: {stats.total_rating_count} | "
            f"Toplam Yorum: {stats.total_comment_count}"
        )
        if stats.ai_summary:
            stats_text += f"\nTrendyol AI Özeti: {stats.ai_summary}"

    prompt = f"""Sen FraudGuard AI için güvenilirlik analisti olan Gemini Trust Orchestrator'sın.

KURALLAR:
- Sadece aşağıdaki verilen bilgilere dayan.
- Yeni bilgi uydurma, tahmin yapma.
- Eksik verileri açıkça belirt.
- Yorum metinlerini kendin de analiz et, sadece agent çıktılarına güvenme.

Ayrıca şunları da analiz et:
1. Yorum dilini incele: Aynı kişi farklı hesaplardan mı yazıyor gibi benzer üslup var mı?
2. Yorum içeriklerinde ürünle alakasız detay var mı? (örnek: yastık için 'sürekli stok yapıyorum')
3. Övgü ile şikayetlerin oranı tutarlı mı, yoksa şikayetler gömülmüş mü?
4. Satıcı cevapları varsa savunmacı veya şablondan mı?

Bu analizleri key_concerns'e ekle.

JSON formatında yanıt ver:
{{
  "gemini_risk": <0-100 arası integer>,
  "summary": "<2-3 cümle özet>",
  "user_friendly_explanation": "<kullanıcı dostu detaylı açıklama>",
  "key_concerns": ["<endişe 1>", "<endişe 2>"],
  "recommended_action": "<önerilen aksiyon>",
  "confidence": <0-100 arası integer, verinin ne kadar eksiksiz olduğuna göre>
}}

ÜRÜN BİLGİSİ:
Ad: {product.name}
Kategori: {product.category}
Fiyat: {product.current_price} TL
{stats_text}

RULE-BASED RİSK PUANI: {rule_risk:.1f}/100
TESPİT EDİLEN SORUNLAR: {reason_codes}
KANIT LİSTESİ: {evidence}
EKSİK VERİLER: {missing_fields}

HAM YORUM METİNLERİ ({len(review_samples)} yorum):
{chr(10).join(review_samples) if review_samples else "Yorum bulunamadı."}
"""

    for api_key in api_keys:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(response_mime_type="application/json"),
                request_options={"timeout": 12},
            )
            data = json.loads(response.text)

            return GeminiExplanation(
                summary=data.get("summary", "Özet alınamadı."),
                user_friendly_explanation=data.get("user_friendly_explanation", "Açıklama alınamadı."),
                key_concerns=data.get("key_concerns", []),
                recommended_action=data.get("recommended_action", "Dikkatli inceleyin."),
                confidence=data.get("confidence"),
                gemini_risk=data.get("gemini_risk"),
            )
        except Exception as e:
            err_msg = str(e).lower()
            if "429" in err_msg or "quota" in err_msg or "exhausted" in err_msg or "too many requests" in err_msg:
                print(f"Gemini API Limit Hatası (Key değiştiriliyor...): {e}")
                continue
            else:
                print(f"Gemini API Genel Hatası: {e}")
                return _fallback_explanation(product, agent_outputs, rule_risk)

    print("Tüm API Key'lerin limiti doldu!")
    return _fallback_explanation(product, agent_outputs, rule_risk)


def _fallback_explanation(product: Product | None = None, agent_outputs=None, rule_risk: float = 50.0) -> GeminiExplanation:
    """Gemini API'ye ulaşılamadığında rule-based veriden anlamlı açıklama üretir."""
    risk_level = "düşük" if rule_risk < 35 else "orta" if rule_risk < 65 else "yüksek"
    trust_score = max(0, min(100, round(100 - rule_risk)))

    concerns = []
    if agent_outputs:
        for output in agent_outputs:
            concerns.extend(output.evidence[:2])
    if not concerns:
        concerns = ["Ürün verisi sınırlı, detaylı analiz yapılamadı."]

    product_name = getattr(product, "name", None) or "Bu ürün"
    price = getattr(product, "current_price", None)
    price_text = f"Güncel fiyat {price} TL." if price else "Fiyat bilgisi alınmış."

    has_price_history = bool(getattr(product, "price_history", None))
    seller_verified = getattr(getattr(product, "seller", None), "verified", None)

    missing_notes = []
    if not has_price_history:
        missing_notes.append("Fiyat geçmişi bulunamadı.")
    if seller_verified is None:
        missing_notes.append("Satıcı doğrulama bilgisi sınırlı olabilir.")

    summary = (
        f"{product_name} {risk_level} riskli görünüyor. "
        f"{price_text} "
        f"{'Fiyat tarafında belirgin bir indirim anomalisi görülmüyor.' if rule_risk < 40 else 'Bazı risk sinyalleri tespit edildi.'}"
    )

    user_friendly = (
        f"Ürün için hesaplanan Trust Score {trust_score}/100. "
        f"{'İncelenen verilerde güçlü bir sahte yorum veya fiyat manipülasyonu sinyali bulunmadı.' if rule_risk < 50 else 'Bazı risk göstergeleri mevcut, dikkatli incelenmelidir.'}"
        + (" Ancak fiyat geçmişi olmadığı için uzun dönemli indirim güvenilirliği doğrulanamadı." if not has_price_history else "")
    )

    recommended = (
        "Satın almadan önce son yorumları ve satıcı profilini kontrol et."
        if rule_risk < 60 else
        "Bu ürünü almadan önce dikkatli bir şekilde yorumları ve satıcıyı araştırmanızı öneririz."
    )

    return GeminiExplanation(
        summary=summary,
        user_friendly_explanation=user_friendly,
        key_concerns=missing_notes + concerns[:3],
        recommended_action=recommended,
        confidence=max(30, min(85, round(100 - rule_risk * 0.5))),
        gemini_risk=round(rule_risk),
        explanation_source="rule_based",
    )