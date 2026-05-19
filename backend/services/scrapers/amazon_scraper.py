import html as html_lib
import re
from typing import Optional

import httpx

from models.product_schema import Product, Seller
from services.scrapers.base_scraper import BaseScraper
from utils.price_utils import calculate_discount_percentage

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
}


class AmazonScraper(BaseScraper):
    async def extract_product(self, url: str) -> Optional[Product]:
        try:
            html = None
            for verify in (True, False):
                try:
                    async with httpx.AsyncClient(
                        headers=REQUEST_HEADERS,
                        follow_redirects=True,
                        timeout=20,
                        verify=verify,
                    ) as client:
                        response = await client.get(url)
                        response.raise_for_status()
                        html = response.text
                        break
                except httpx.ConnectError as exc:
                    if verify and _is_ssl_certificate_error(exc):
                        continue
                    raise

            if html is None:
                return None

            name = extract_amazon_name(html)
            current_price = extract_amazon_price(html)
            seller_name = extract_amazon_seller(html) or "Amazon"

            if not name and current_price is None:
                return None

            missing_fields = []
            if not name:
                missing_fields.append("name")
            if current_price is None:
                missing_fields.append("current_price")
            missing_fields.extend(
                [
                    "reviews",
                    "price_history",
                    "product_description",
                    "seller_account_age",
                    "seller_verified",
                    "seller_return_rate",
                ]
            )

            return Product(
                source_url=url,
                name=name,
                current_price=current_price,
                original_price=None,
                discount_percentage=calculate_discount_percentage(current_price, None),
                seller=Seller(
                    name=seller_name,
                    rating=None,
                    account_age_days=None,
                    verified=None,
                    return_rate=None,
                ),
                reviews=[],
                product_description="",
                claimed_features=[],
                missing_fields=sorted(set(missing_fields)),
            )
        except Exception as exc:
            print(f"AmazonScraper error: {exc}")
            return None


def extract_amazon_name(html: str) -> str | None:
    match = re.search(
        r'<span[^>]+id=["\']productTitle["\'][^>]*>(.*?)</span>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if match:
        return _clean_text(_strip_tags(match.group(1)))

    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if title_match:
        title = _clean_text(_strip_tags(title_match.group(1)))
        if title:
            return re.sub(r"\s*:\s*Amazon\..*$", "", title).strip() or title

    return None


def extract_amazon_price(html: str) -> float | None:
    offscreen_prices = re.findall(
        r'<span[^>]+class=["\'][^"\']*a-offscreen[^"\']*["\'][^>]*>(.*?)</span>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    for raw_price in offscreen_prices:
        price = parse_price_text(_strip_tags(raw_price))
        if price is not None:
            return price

    whole_match = re.search(
        r'<span[^>]+class=["\'][^"\']*a-price-whole[^"\']*["\'][^>]*>(.*?)</span>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    fraction_match = re.search(
        r'<span[^>]+class=["\'][^"\']*a-price-fraction[^"\']*["\'][^>]*>(.*?)</span>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if whole_match:
        whole = _clean_text(_strip_tags(whole_match.group(1))) or ""
        fraction = _clean_text(_strip_tags(fraction_match.group(1))) if fraction_match else None
        return parse_price_text(f"{whole},{fraction}" if fraction else whole)

    return None


def extract_amazon_seller(html: str) -> str | None:
    merchant_match = re.search(
        r'<div[^>]+id=["\']merchant-info["\'][^>]*>(.*?)</div>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if merchant_match:
        text = _clean_text(_strip_tags(merchant_match.group(1)))
        if text:
            return text

    seller_match = re.search(
        r'<a[^>]+id=["\']sellerProfileTriggerId["\'][^>]*>(.*?)</a>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if seller_match:
        return _clean_text(_strip_tags(seller_match.group(1)))

    return None


def parse_price_text(value: str | None) -> float | None:
    if not value:
        return None

    normalized = html_lib.unescape(value)
    normalized = re.sub(r"[^\d,.]", "", normalized)
    if not normalized:
        return None

    if "," in normalized and "." in normalized:
        if normalized.rfind(",") > normalized.rfind("."):
            normalized = normalized.replace(".", "").replace(",", ".")
        else:
            normalized = normalized.replace(",", "")
    elif "," in normalized:
        normalized = normalized.replace(".", "").replace(",", ".")

    try:
        return float(normalized)
    except ValueError:
        return None


def _strip_tags(value: str) -> str:
    return re.sub(r"<[^>]+>", " ", value)


def _clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    text = html_lib.unescape(value)
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def _is_ssl_certificate_error(exc: Exception) -> bool:
    return "CERTIFICATE_VERIFY_FAILED" in str(exc)
