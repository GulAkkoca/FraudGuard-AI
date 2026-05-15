from pydantic import BaseModel, Field


class PriceHistoryEntry(BaseModel):
    date: str | None = None
    price: float


class Seller(BaseModel):
    name: str | None = None
    rating: float | None = None
    account_age_days: int | None = None
    verified: bool | None = None
    return_rate: float | None = None


class Review(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    text: str
    date: str | None = None


class Product(BaseModel):
    id: str | None = None
    source_url: str | None = None
    name: str
    category: str | None = None
    current_price: float
    original_price: float | None = None
    discount_percentage: float | None = None
    price_history: list[PriceHistoryEntry] = Field(default_factory=list)
    seller: Seller = Field(default_factory=Seller)
    reviews: list[Review] = Field(default_factory=list)
    product_description: str = ""
    claimed_features: list[str] = Field(default_factory=list)
    expected_scenario: str | None = None

