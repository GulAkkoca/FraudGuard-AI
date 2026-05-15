import json
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from fastapi import HTTPException

from models.product_schema import Product
from services.fallback_service import get_default_fallback_product, get_product_by_id
from services.scraping_service import extract_live_product

SAMPLE_LINKS_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_links.json"


@dataclass
class IngestionResult:
    product: Product
    source: str
    extraction_status: str


def ingest_url(url: str) -> IngestionResult:
    _validate_url_or_demo_key(url)
    demo_product = _match_demo_link(url)
    if demo_product is not None:
        return IngestionResult(demo_product, "demo_mapping_used", "success")

    live_product = extract_live_product(url)
    if live_product is not None:
        return IngestionResult(live_product, "live_url", "success")

    fallback = get_default_fallback_product()
    return IngestionResult(fallback, "fallback", "failed_fallback_used")


def _validate_url_or_demo_key(value: str) -> None:
    if value.startswith("demo-"):
        return

    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise HTTPException(status_code=400, detail="Gecerli bir URL veya demo link girin.")


def _match_demo_link(value: str) -> Product | None:
    sample_links = json.loads(SAMPLE_LINKS_PATH.read_text(encoding="utf-8"))
    for demo_key, product_id in sample_links.items():
        if demo_key in value:
            return get_product_by_id(product_id)
    return None

