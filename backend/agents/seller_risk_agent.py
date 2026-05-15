from models.agent_schema import AgentOutput
from models.product_schema import Product


def analyze_seller_risk(product: Product) -> AgentOutput:
    seller = product.seller
    risk = 0
    reason_codes: list[str] = []
    evidence: list[str] = []
    missing_fields: list[str] = []

    if not seller.name:
        missing_fields.append("seller.name")
        reason_codes.append("MISSING_SELLER")
        evidence.append("Satici bilgisi eksik.")

    if seller.rating is None:
        missing_fields.append("seller.rating")
    elif seller.rating < 3.5:
        risk += 25
        reason_codes.append("LOW_SELLER_RATING")
        evidence.append("Satici puani dusuk gorunuyor.")

    if seller.verified is None:
        missing_fields.append("seller.verified")
    elif not seller.verified:
        risk += 25
        reason_codes.append("UNVERIFIED_SELLER")
        evidence.append("Satici dogrulanmis gorunmuyor.")

    if seller.account_age_days is None:
        missing_fields.append("seller_account_age")
    elif seller.account_age_days < 30:
        risk += 30
        reason_codes.append("NEW_SELLER")
        evidence.append("Satici hesabi cok yeni.")

    if seller.return_rate is not None and seller.return_rate >= 0.30:
        risk += 20
        reason_codes.append("HIGH_RETURN_RATE")
        evidence.append("Saticinin iade orani yuksek gorunuyor.")

    return AgentOutput(
        agent_name="Seller Risk Agent",
        risk_score=min(risk, 100),
        reason_codes=reason_codes,
        evidence=evidence,
        missing_fields=sorted(set(missing_fields)),
    )

