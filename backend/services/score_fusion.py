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

    # Analysis notes — her zaman en az birkaç madde olacak şekilde doldur
    analysis_notes: list[str] = []
    positive_signals: list[str] = []

    for output in agent_outputs:
        for note in output.evidence:
            if any(kw in note.lower() for kw in ["risk", "şüphe", "uyumsuz", "anomali", "eksik", "sahte", "yüksek", "düşük puan"]):
                analysis_notes.append(note)
            else:
                positive_signals.append(note)

    # Fallback: hiç note yoksa genel bilgi ekle
    if not analysis_notes:
        if trust_score >= 75:
            analysis_notes.append(f"Trust Score {trust_score}/100 — Ürün genel olarak güvenilir görünmektedir.")
        elif trust_score >= 50:
            analysis_notes.append(f"Trust Score {trust_score}/100 — Orta risk seviyesi, bazı alanlar dikkat gerektiriyor.")
        else:
            analysis_notes.append(f"Trust Score {trust_score}/100 — Yüksek risk sinyalleri tespit edildi, dikkatli olunmalı.")

    # Eksik veri varsa bunu da not olarak ekle
    missing = sorted({f for o in agent_outputs for f in o.missing_fields})
    if missing:
        analysis_notes.append(f"Eksik veriler nedeniyle analiz sınırlı tutuldu: {', '.join(missing[:4])}.")

    return TrustReport(
        source=source,
        extraction_status=extraction_status,
        product=product,
        missing_fields=missing,
        trust_score=trust_score,
        risk_level=classify_risk_level(trust_score),
        gemini_used=gemini_used,
        reason_codes=sorted({c for o in agent_outputs for c in o.reason_codes}),
        evidence=[item for o in agent_outputs for item in o.evidence],
        analysis_notes=analysis_notes,
        positive_signals=positive_signals[:5],
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