from agents.review_agent import analyze_review_risk
from services.fallback_service import get_product_by_id


def test_review_agent_detects_similar_reviews():
    product = get_product_by_id("p002")
    output = analyze_review_risk(product)

    assert "SIMILAR_REVIEWS" in output.reason_codes

