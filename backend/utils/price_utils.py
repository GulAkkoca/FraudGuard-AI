def calculate_discount_percentage(current_price: float | None, original_price: float | None) -> float | None:
    if not current_price or not original_price or original_price <= current_price:
        return None
    return round(((original_price - current_price) / original_price) * 100, 2)


def average_price(prices: list[float]) -> float | None:
    if not prices:
        return None
    return sum(prices) / len(prices)

