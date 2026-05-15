from models.agent_schema import AgentOutput
from models.product_schema import Product
from models.response_schema import GeminiExplanation, TrustReport


def build_final_report(
    product: Product,
    source: str,
    extraction_status: str,
    agent_outputs: list[AgentOutput],
    rule_risk: float,
    gemini_explanation: GeminiExplanation,
) -> TrustReport:
    gemini_used = gemini_explanation.gemini_risk is not None
    final_risk = rule_risk
    if gemini_used:
        final_risk = (rule_risk * 0.70) + ((gemini_explanation.gemini_risk or 0) * 0.30)

    trust_score = max(0, min(100, round(100 - final_risk)))
    return TrustReport(
        source=source,
        extraction_status=extraction_status,
        product=product,
        missing_fields=sorted({field for output in agent_outputs for field in output.missing_fields}),
        trust_score=trust_score,
        risk_level=classify_risk_level(trust_score),
        gemini_used=gemini_used,
        reason_codes=sorted({code for output in agent_outputs for code in output.reason_codes}),
        evidence=[item for output in agent_outputs for item in output.evidence],
        agent_outputs=agent_outputs,
        gemini_explanation=gemini_explanation,
    )


def classify_risk_level(trust_score: int) -> str:
    if trust_score >= 75:
        return "Low"
    if trust_score >= 50:
        return "Medium"
    return "High"

