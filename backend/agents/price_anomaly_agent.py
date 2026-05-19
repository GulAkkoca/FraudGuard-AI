from models.agent_schema import AgentOutput
from models.product_schema import Product
from utils.price_utils import calculate_discount_percentage, average_price


def analyze_price_risk(product: Product) -> AgentOutput:
    risk = 0
    reason_codes: list[str] = []
    evidence: list[str] = []
    missing_fields: list[str] = []

    if product.current_price is None:
        missing_fields.append("current_price")
        evidence.append("Güncel fiyat bulunamadığı için fiyat analizi sınırlı.")

    discount = product.discount_percentage
    if discount is None:
        discount = calculate_discount_percentage(product.current_price, product.original_price)

    # Aşırı indirim — tek başına orta risk
    if discount is not None and discount >= 70:
        risk += 35
        reason_codes.append("EXCESSIVE_DISCOUNT")
        evidence.append(f"Çok yüksek indirim oranı tespit edildi: %{int(discount)}")
    elif discount is not None and discount >= 50:
        risk += 20
        reason_codes.append("HIGH_DISCOUNT")
        evidence.append(f"Yüksek indirim oranı tespit edildi: %{int(discount)}")

    if not product.price_history:
        missing_fields.append("price_history")
        reason_codes.append("MISSING_PRICE_HISTORY")
        evidence.append("Fiyat geçmişi bulunamadığı için indirim güveni sınırlı.")
    else:
        historical_average = average_price([e.price for e in product.price_history])
        if historical_average:

            # Şişirilmiş orijinal fiyat
            if product.original_price and product.original_price > historical_average * 1.5:
                risk += 35
                reason_codes.append("INFLATED_ORIGINAL_PRICE")
                evidence.append(
                    f"Orijinal fiyat ({product.original_price:.0f}), geçmiş ortalamadan "
                    f"({historical_average:.0f}) belirgin şekilde yüksek."
                )

            # Sahte indirim — güncel fiyat zaten tarihi ortalamaya yakın
            if (
                product.current_price is not None
                and discount is not None
                and discount >= 40
                and (historical_average * 0.85 <= product.current_price <= historical_average * 1.15)
            ):
                risk += 30
                reason_codes.append("FAKE_DISCOUNT_CURRENT_PRICE")
                evidence.append(
                    f"Güncel fiyat ({product.current_price:.0f}) geçmiş ortalamaya "
                    f"({historical_average:.0f}) yakın olmasına rağmen %{int(discount)} indirim gösteriliyor."
                )

            # Fiyat düşüşü yok ama indirim var
            if (
                product.current_price is not None
                and product.original_price is not None
                and product.original_price <= historical_average * 1.05
                and discount is not None
                and discount >= 30
            ):
                risk += 20
                reason_codes.append("NO_REAL_PRICE_DROP")
                evidence.append("Geçmiş fiyat verisiyle karşılaştırıldığında gerçek bir fiyat düşüşü görülmüyor.")

    return AgentOutput(
        agent_name="Price Anomaly Agent",
        risk_score=min(risk, 100),
        reason_codes=reason_codes,
        evidence=evidence,
        missing_fields=missing_fields,
    )