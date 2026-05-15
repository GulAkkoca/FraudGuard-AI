from models.agent_schema import AgentOutput

WEIGHTS = {
    "Review Risk Agent": 0.35,
    "Price Anomaly Agent": 0.25,
    "Seller Risk Agent": 0.25,
    "Product Consistency Agent": 0.15,
}


def calculate_rule_risk(agent_outputs: list[AgentOutput]) -> float:
    return sum(output.risk_score * WEIGHTS.get(output.agent_name, 0) for output in agent_outputs)

