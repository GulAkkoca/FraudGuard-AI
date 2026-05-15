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

    mismatches = []
    for claim, complaints in CLAIM_COMPLAINT_MAP.items():
        if any(claim in item for item in claims) and contains_any(review_text, complaints):
            mismatches.append(claim)

    if not mismatches:
        return AgentOutput(agent_name="Product Consistency Agent", risk_score=0)

    return AgentOutput(
        agent_name="Product Consistency Agent",
        risk_score=min(25 + len(mismatches) * 20, 100),
        reason_codes=["CLAIM_MISMATCH"],
        evidence=["Urun aciklamasindaki iddialarla yorumlardaki deneyimler arasinda celiski bulundu."],
        missing_fields=[],
    )

