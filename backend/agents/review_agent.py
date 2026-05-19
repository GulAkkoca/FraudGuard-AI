from collections import Counter
from difflib import SequenceMatcher

from models.agent_schema import AgentOutput
from models.product_schema import Product

GENERIC_REVIEW_WORDS = ("very good", "amazing", "fast delivery", "fast shipping", "recommend")


def analyze_review_risk(product: Product) -> AgentOutput:
    reviews = product.reviews
    if not reviews:
        return AgentOutput(
            agent_name="Review Risk Agent",
            risk_score=35,
            reason_codes=["MISSING_REVIEWS"],
            evidence=["Urun yorumu bulunamadi."],
            missing_fields=["reviews"],
        )

    risk = 0
    reason_codes: list[str] = []
    evidence: list[str] = []

    dates = [review.date for review in reviews if review.date]
    if dates and Counter(dates).most_common(1)[0][1] >= 3:
        risk += 25
        reason_codes.append("REVIEW_BURST")
        evidence.append("Kisa zaman araliginda yogun yorum paterni tespit edildi.")

    texts = [review.text.lower() for review in reviews]
    similar_pairs = 0
    for index, text in enumerate(texts):
        for other in texts[index + 1 :]:
            if SequenceMatcher(None, text, other).ratio() >= 0.72:
                similar_pairs += 1
    if similar_pairs:
        risk += 35
        reason_codes.append("SIMILAR_REVIEWS")
        evidence.append("Birden fazla yorum metni birbirine yuksek benzerlik gosteriyor.")

    generic_count = sum(any(word in text for word in GENERIC_REVIEW_WORDS) for text in texts)
    if generic_count >= 2:
        risk += 20
        reason_codes.append("GENERIC_SHORT_REVIEWS")
        evidence.append("Yorumlarda tekrar eden genel olumlu ifadeler bulundu.")

    five_star_count = sum(1 for review in reviews if review.rating == 5)
    if len(reviews) > 0 and (five_star_count / len(reviews)) > 0.8:
        risk += 20
        reason_codes.append("HIGH_FIVE_STAR_RATIO")
        evidence.append("5 yildizli yorumlarin orani supheli derecede yuksek.")

    return AgentOutput(
        agent_name="Review Risk Agent",
        risk_score=min(risk, 100),
        reason_codes=reason_codes,
        evidence=evidence,
        missing_fields=[],
    )

