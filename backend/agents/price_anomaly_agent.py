from models.agent_schema import AgentOutput
from models.product_schema import Product
from utils.price_utils import calculate_discount_percentage, average_price


def analyze_price_risk(product: Product) -> AgentOutput:
    risk = 0
    reason_codes: list[str] = []
    evidence: list[str] = []
    missing_fields: list[str] = []

    discount = product.discount_percentage
    if discount is None:
        discount = calculate_discount_percentage(product.current_price, product.original_price)

    if discount is not None and discount >= 50:
        risk += 25
        reason_codes.append("EXCESSIVE_DISCOUNT")
        evidence.append("Urunde yuksek indirim orani tespit edildi.")

    if not product.price_history:
        missing_fields.append("price_history")
        reason_codes.append("MISSING_PRICE_HISTORY")
        evidence.append("Fiyat gecmisi bulunamadigi icin indirim guveni sinirli.")
    else:
        historical_average = average_price([entry.price for entry in product.price_history])
        if historical_average:
            if product.original_price and product.original_price > historical_average * 1.6:
                risk += 35
                reason_codes.append("INFLATED_ORIGINAL_PRICE")
                evidence.append("Eski fiyat, gecmis fiyat ortalamasina gore yuksek gorunuyor.")
            
            if discount is not None and discount >= 50 and (historical_average * 0.9 <= product.current_price <= historical_average * 1.1):
                risk += 25
                reason_codes.append("FAKE_DISCOUNT_CURRENT_PRICE")
                evidence.append("Guncel fiyat gecmis ortalamaya yakin olmasina ragmen yuksek indirim gosteriliyor.")

    return AgentOutput(
        agent_name="Price Anomaly Agent",
        risk_score=min(risk, 100),
        reason_codes=reason_codes,
        evidence=evidence,
        missing_fields=missing_fields,
    )

