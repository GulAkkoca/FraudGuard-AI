from models.agent_schema import AgentOutput
from models.product_schema import Product
from models.response_schema import GeminiExplanation


def build_trust_explanation(product: Product, agent_outputs: list[AgentOutput]) -> GeminiExplanation:
    high_risk_reasons = [code for output in agent_outputs for code in output.reason_codes]
    missing_fields = [field for output in agent_outputs for field in output.missing_fields]

    if not high_risk_reasons:
        summary = "Bu urunde belirgin bir supheli sinyal bulunmadi."
        explanation = "Yorumlar, fiyat gecmisi, satici profili ve urun aciklamasi genel olarak tutarli gorunuyor."
        action = "Yine de satin almadan once urun detaylarini ve guncel satici kosullarini kontrol edin."
    else:
        summary = "Bu urunde dikkat edilmesi gereken guven sinyalleri var."
        explanation = "Analiz, verilen kanitlara dayanarak bazi risk sinyalleri tespit etti. Kesin fraud iddiasi yerine supheli sinyal olarak degerlendirilmelidir."
        action = "Satin almadan once satici profilini, yorumlari ve fiyat gecmisini ayrintili inceleyin."

    if missing_fields:
        explanation += " Eksik veri alanlari analiz guvenini sinirlayabilir."

    gemini_risk = max((output.risk_score for output in agent_outputs), default=0)
    return GeminiExplanation(
        summary=summary,
        user_friendly_explanation=explanation,
        recommended_action=action,
        gemini_risk=gemini_risk,
    )

