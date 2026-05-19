from pydantic import BaseModel, Field


class AgentOutput(BaseModel):
    agent_name: str
    risk_score: float = Field(ge=0, le=100)
    reason_codes: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)

