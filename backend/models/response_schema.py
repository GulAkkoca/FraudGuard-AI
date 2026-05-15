from pydantic import BaseModel, Field

from models.agent_schema import AgentOutput
from models.product_schema import Product


class AnalyzeUrlRequest(BaseModel):
    url: str = Field(min_length=3)


class GeminiExplanation(BaseModel):
    summary: str
    user_friendly_explanation: str
    recommended_action: str
    gemini_risk: float | None = Field(default=None, ge=0, le=100)


class TrustReport(BaseModel):
    source: str
    extraction_status: str
    product: Product
    missing_fields: list[str]
    trust_score: int
    risk_level: str
    gemini_used: bool
    reason_codes: list[str]
    evidence: list[str]
    agent_outputs: list[AgentOutput]
    gemini_explanation: GeminiExplanation

