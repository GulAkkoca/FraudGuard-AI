from models.agent_schema import AgentOutput
from models.product_schema import Product
from utils.text_utils import contains_any

CLAIM_COMPLAINT_MAP = {
    "waterproof": ["not waterproof", "wet inside", "water passed", "rain"],
    "fully waterproof": ["not waterproof", "wet inside", "water passed"],
    "official warranty": ["no official warranty", "warranty card"],
    "authentic serial number": ["imei could not be verified", "suspicious"],
    "noise cancellation": ["noise cancelling works indoors", "struggles"],
    "long battery": ["battery lasted less", "battery bad"],
}


def analyze_consistency_risk(product: Product) -> AgentOutput:
    if not product.product_description:
        return AgentOutput(
            agent_name="Product Consistency Agent",
            risk_score=20,
            reason_codes=["MISSING_PRODUCT_DESCRIPTION"],
            evidence=["Urun aciklamasi bulunamadi."],
            missing_fields=["product_description"],
        )

    review_text = " ".join(review.text for review in product.reviews).lower()
    claims = [claim.lower() for claim in product.claimed_features]
    claims.extend(product.product_description.lower().split(","))
    claims_text = " ".join(claims)

    risk = 0
    reason_codes = []
    evidence = []

    if ("original" in claims_text) and contains_any(review_text, ["fake", "not original"]):
        risk += 50
        reason_codes.append("FAKE_CLAIM_MISMATCH")
        evidence.append("Urun aciklamasinda 'orijinal' iddiasi var ancak yorumlarda sahte olduguna dair sikayetler var.")

    if ("water resistant" in claims_text or "waterproof" in claims_text) and contains_any(review_text, ["not waterproof", "wet inside", "water passed"]):
        risk += 35
        reason_codes.append("WATER_RESISTANT_MISMATCH")
        evidence.append("Su gecirmezlik iddiasina ragmen yorumlarda su gecirme sikayetleri var.")

    if ("premium" in claims_text) and contains_any(review_text, ["poor quality", "cheap", "broken"]):
        risk += 30
        reason_codes.append("PREMIUM_CLAIM_MISMATCH")
        evidence.append("Premium iddiasina ragmen yorumlarda kalite sikayetleri var.")

    if risk == 0:
        return AgentOutput(agent_name="Product Consistency Agent", risk_score=0)

    return AgentOutput(
        agent_name="Product Consistency Agent",
        risk_score=min(risk, 100),
        reason_codes=reason_codes,
        evidence=evidence,
        missing_fields=[],
    )

