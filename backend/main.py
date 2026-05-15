from fastapi import FastAPI, HTTPException

from agents.consistency_agent import analyze_consistency_risk
from agents.price_anomaly_agent import analyze_price_risk
from agents.review_agent import analyze_review_risk
from agents.seller_risk_agent import analyze_seller_risk
from models.response_schema import AnalyzeUrlRequest, TrustReport
from services.fallback_service import get_product_by_id
from services.gemini_trust_orchestrator import build_trust_explanation
from services.rule_engine import calculate_rule_risk
from services.score_fusion import build_final_report
from services.url_ingestion_service import ingest_url

app = FastAPI(title="FraudGuard AI Backend", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "FraudGuard AI Backend"}


@app.post("/analyze-url", response_model=TrustReport)
def analyze_url(payload: AnalyzeUrlRequest) -> TrustReport:
    ingestion = ingest_url(payload.url)
    return _analyze_product(ingestion.product, ingestion.source, ingestion.extraction_status)


@app.post("/analyze-demo/{product_id}", response_model=TrustReport)
def analyze_demo(product_id: str) -> TrustReport:
    product = get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Demo urun bulunamadi.")

    return _analyze_product(product, "demo_mapping_used", "success")


def _analyze_product(product, source: str, extraction_status: str) -> TrustReport:
    agent_outputs = [
        analyze_review_risk(product),
        analyze_price_risk(product),
        analyze_seller_risk(product),
        analyze_consistency_risk(product),
    ]
    rule_risk = calculate_rule_risk(agent_outputs)
    gemini_explanation = build_trust_explanation(product, agent_outputs)

    return build_final_report(
        product=product,
        source=source,
        extraction_status=extraction_status,
        agent_outputs=agent_outputs,
        rule_risk=rule_risk,
        gemini_explanation=gemini_explanation,
    )

