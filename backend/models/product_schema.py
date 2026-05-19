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
    likes_count: int | None = None
    seller_name: str | None = None


class ReviewStats(BaseModel):
    average_rating: float | None = None
    total_comment_count: int | None = None
    total_rating_count: int | None = None
    rating_counts: dict[str, int] = Field(default_factory=dict)  # {"1": x, "5": x ...}
    total_pages: int | None = None
    ai_summary: str | None = None
    tags: list[str] = Field(default_factory=list)


class Product(BaseModel):
    id: str | None = None
    source_url: str | None = None
    name: str | None = None
    category: str | None = None
    current_price: float | None = None
    original_price: float | None = None
    discount_percentage: float | None = None
    price_history: list[PriceHistoryEntry] = Field(default_factory=list)
    seller: Seller = Field(default_factory=Seller)
    reviews: list[Review] = Field(default_factory=list)
    review_stats: ReviewStats = Field(default_factory=ReviewStats)
    product_description: str = ""
    claimed_features: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)
    expected_scenario: str | None = None
