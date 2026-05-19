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
    gemini_used = gemini_explanation is not None and getattr(gemini_explanation, "explanation_source", "") == "gemini"

    final_risk = rule_risk

    # Kritik reason code varsa taban skoru zorla
    critical_codes = {"FAKE_PRODUCT_COMPLAINTS", "VISUAL_MISMATCH", "NONSENSICAL_REPEAT_BUY"}
    has_critical = any(
        code in critical_codes
        for output in agent_outputs
        for code in output.reason_codes
    )
    if has_critical:
        final_risk = max(final_risk, 60)

    trust_score = max(0, min(100, round(100 - final_risk)))

    return TrustReport(
        source=source,
        extraction_status=extraction_status,
        product=product,
        missing_fields=sorted({f for o in agent_outputs for f in o.missing_fields}),
        trust_score=trust_score,
        risk_level=classify_risk_level(trust_score),
        gemini_used=gemini_used,
        reason_codes=sorted({c for o in agent_outputs for c in o.reason_codes}),
        evidence=[item for o in agent_outputs for item in o.evidence],
        agent_outputs=agent_outputs,
        gemini_explanation=gemini_explanation,
    )


def classify_risk_level(trust_score: int) -> str:
    if trust_score >= 75:
        return "Low"
    if trust_score >= 50:
        return "Medium"
    if trust_score >= 30:
        return "High"
    return "Critical"