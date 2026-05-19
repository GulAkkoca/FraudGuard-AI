from pydantic import BaseModel, Field

from models.agent_schema import AgentOutput
from models.product_schema import Product


class AnalyzeUrlRequest(BaseModel):
    url: str = Field(min_length=3)


class GeminiExplanation(BaseModel):
    summary: str = ""
    user_friendly_explanation: str = ""
    key_concerns: list[str] = Field(default_factory=list)
    recommended_action: str = ""
    missing_data_explanation: str = ""
    confidence: int | None = None
    gemini_risk: int | None = None

    # Gemini skor üretmez. Sadece açıklama üretir.
    explanation_source: str = "gemini"


class TrustReport(BaseModel):
    source: str
    extraction_status: str

    product: Product

    trust_score: int = Field(ge=0, le=100)
    risk_level: str

    reason_codes: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)

    # Frontend için çok önemli
    analysis_notes: list[str] = Field(default_factory=list)
    positive_signals: list[str] = Field(default_factory=list)

    agent_outputs: list[AgentOutput] = Field(default_factory=list)

    gemini_used: bool = False
    gemini_explanation: GeminiExplanation | None = None

