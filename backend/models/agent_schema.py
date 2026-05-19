from pydantic import BaseModel, Field


class AgentOutput(BaseModel):
    agent_name: str
    risk_score: float = Field(default=0, ge=0, le=100)
    reason_codes: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)
    analysis_notes: list[str] = Field(default_factory=list)
    positive_signals: list[str] = Field(default_factory=list)
    severity: str = "none"
