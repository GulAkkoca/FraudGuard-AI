from agents.price_anomaly_agent import analyze_price_risk
from services.fallback_service import get_product_by_id


def test_price_agent_detects_excessive_discount():
    product = get_product_by_id("p003")
    output = analyze_price_risk(product)

    assert "EXCESSIVE_DISCOUNT" in output.reason_codes

