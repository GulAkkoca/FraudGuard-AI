def clamp_risk_score(value: float) -> float:
    return max(0, min(100, value))

