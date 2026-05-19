import json
from functools import lru_cache
from pathlib import Path

from models.product_schema import PriceHistoryEntry, Product
from utils.price_utils import calculate_discount_percentage

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "fallback_products.json"


@lru_cache
def load_fallback_products() -> list[Product]:
    raw_products = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return [normalize_product(raw) for raw in raw_products]


def get_product_by_id(product_id: str) -> Product | None:
    return next((product for product in load_fallback_products() if product.id == product_id), None)


def get_default_fallback_product() -> Product:
    return load_fallback_products()[0]


def normalize_product(raw: dict) -> Product:
    price_history = []
    for index, item in enumerate(raw.get("price_history") or []):
        if isinstance(item, dict):
            price_history.append(PriceHistoryEntry(**item))
        else:
            price_history.append(PriceHistoryEntry(date=None, price=float(item)))

    if raw.get("discount_percentage") is None:
        raw["discount_percentage"] = calculate_discount_percentage(
            raw.get("current_price"), raw.get("original_price")
        )

    return Product(**{**raw, "price_history": price_history})

