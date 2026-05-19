
from models.agent_schema import AgentOutput

WEIGHTS = {
    "Review Risk Agent": 0.35,
    "Price Anomaly Agent": 0.25,
    "Seller Risk Agent": 0.25,
    "Product Consistency Agent": 0.15,
}

# Eksik veri başına ceza puanı
MISSING_FIELD_PENALTY = {
    "reviews": 10,
    "price_history": 8,
    "seller.rating": 5,
    "seller.verified": 4,
    "product_description": 4,
    "current_price": 6,
    "seller_account_age": 3,
    "seller_return_rate": 3,
}


def calculate_rule_risk(agent_outputs: list[AgentOutput]) -> float:
    total_weight = 0.0
    weighted_sum = 0.0

    for output in agent_outputs:
        weight = WEIGHTS.get(output.agent_name, 0)
        if weight == 0:
            continue
        # Eksik verisi olan agent'ın skoru var sayma, ağırlığını düşür
        data_completeness = 1.0 - min(len(output.missing_fields) * 0.15, 0.5)
        effective_weight = weight * data_completeness
        weighted_sum += output.risk_score * effective_weight
        total_weight += effective_weight

    if total_weight == 0:
        return 50.0  # hiçbir şey bilmiyoruz, nötr

    base_risk = weighted_sum / total_weight

    # Eksik veri cezası
    all_missing = {f for o in agent_outputs for f in o.missing_fields}
    penalty = sum(MISSING_FIELD_PENALTY.get(f, 2) for f in all_missing)

    return min(base_risk + penalty, 100)