import asyncio
from datetime import datetime, timezone
import html as html_lib
import json
import re
from typing import Any, Optional
from urllib.parse import parse_qs, urlparse

import httpx

from models.product_schema import Product, Review, Seller
from services.scrapers.base_scraper import BaseScraper
from utils.price_utils import calculate_discount_percentage

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json;q=0.8,*/*;q=0.7",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
}


class TrendyolScraper(BaseScraper):
    async def extract_product(self, url: str) -> Optional[Product]:
        product_content_id = extract_product_content_id(url)

        try:
            for verify in (True, False):
                try:
                    async with httpx.AsyncClient(
                        headers=REQUEST_HEADERS,
                        follow_redirects=True,
                        timeout=20,
                        verify=verify,
                    ) as client:
                        html = await fetch_trendyol_html(url, client=client)
                        price_data = extract_price_from_html(html)
                        name = extract_product_name_from_html(html)
                        category = extract_category_from_html(html)
                        merchant_id = extract_merchant_id_from_html(html)
                        seller_name = extract_seller_name_from_html(html)
                        seller_rating = extract_seller_rating_from_html(html)
                        seller_verified = extract_seller_verified_from_html(html)
                        image_url = extract_image_url_from_html(html)
                        html_reviews = extract_reviews_from_html(html)

                        if product_content_id:
                            review_response, description_response = await asyncio.gather(
                                fetch_trendyol_reviews(client, product_content_id, page_cookies=dict(client.cookies)),
                                fetch_first_json(client, build_description_urls(product_content_id)),
                            )
                        else:
                            review_response = None
                            description_response = None

                        reviews = normalize_reviews(review_response or {})

                        if not reviews:
                            reviews = html_reviews  

                        description_data = normalize_descriptions(description_response or {})
                        product_description = (
                            description_data.get("product_description")
                            or extract_description_from_html(html)
                            or ""
                        )
                        seller_name = (
                            description_data.get("seller_name")
                            or seller_name
                            or extract_seller_name_from_reviews(reviews)
                        )

                        if not product_content_id and not name and price_data.get("current_price") is None:
                            return None

                        return build_product_schema(
                            url=url,
                            product_content_id=product_content_id,
                            name=name,
                            category=category,
                            price_data=price_data,
                            image_url=image_url,
                            seller_name=seller_name,
                            seller_rating=seller_rating,
                            seller_verified=seller_verified,
                            reviews=reviews,
                            product_description=product_description,
                        )
                except httpx.ConnectError as exc:
                    if verify and _is_ssl_certificate_error(exc):
                        continue
                    raise
        except Exception as exc:
            print(f"TrendyolScraper error: {exc}")
            return None


def extract_product_content_id(url: str) -> str | None:
    match = re.search(r"-p-(\d+)", url)
    if match:
        return match.group(1)

    parsed = urlparse(url)
    content_id = parse_qs(parsed.query).get("contentId")
    if content_id and content_id[0].isdigit():
        return content_id[0]

    return None


async def fetch_trendyol_html(url: str, client: httpx.AsyncClient | None = None) -> str:
    if client is not None:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

    for verify in (True, False):
        try:
            async with httpx.AsyncClient(
                headers=REQUEST_HEADERS,
                follow_redirects=True,
                timeout=20,
                verify=verify,
            ) as own_client:
                response = await own_client.get(url)
                response.raise_for_status()
                return response.text
        except httpx.ConnectError as exc:
            if verify and _is_ssl_certificate_error(exc):
                continue
            raise

    raise RuntimeError("Trendyol HTML fetch failed.")


def extract_price_from_html(html: str) -> dict[str, float | str | None]:
    envoy_price = _extract_price_from_envoy_product(html)
    if envoy_price:
        return envoy_price

    json_ld_price = _extract_price_from_json_ld(html)
    if json_ld_price:
        return json_ld_price

    return {
        "current_price": _extract_price_value(html, "discountedPrice"),
        "selling_price": _extract_price_value(html, "sellingPrice"),
        "original_price": _extract_price_value(html, "originalPrice"),
        "currency": _extract_currency(html) or "TRY",
    }


def build_product_schema(
    url: str,
    product_content_id: str | None,
    name: str | None,
    category: str | None,
    price_data: dict[str, Any],
    image_url: str | None,
    seller_name: str | None,
    seller_rating: float | None,
    seller_verified: bool | None,
    reviews: list[Review],
    product_description: str | None,
) -> Product:
    current_price = _as_float(price_data.get("current_price"))
    original_price = _as_float(price_data.get("original_price"))
    missing_fields: list[str] = []

    if not name:
        missing_fields.append("name")
    if current_price is None:
        missing_fields.append("current_price")
    if not seller_name:
        missing_fields.append("seller.name")
    if seller_rating is None:
        missing_fields.append("seller.rating")
    if seller_verified is None:
        missing_fields.append("seller_verified")
    if not reviews:
        missing_fields.append("reviews")
    if not product_description:
        missing_fields.append("product_description")

    missing_fields.extend(
        [
            "price_history",
            "seller_account_age",
            "seller_return_rate",
        ]
    )

    return Product(
        id=product_content_id,
        source_url=url,
        name=name,
        image_url=image_url,
        category=category,
        current_price=current_price,
        original_price=original_price,
        discount_percentage=calculate_discount_percentage(current_price, original_price),
        price_history=[],
        seller=Seller(
            name=seller_name,
            rating=seller_rating,
            account_age_days=None,
            verified=seller_verified,
            return_rate=None,
        ),
        reviews=reviews,
        product_description=product_description or "",
        claimed_features=[],
        missing_fields=sorted(set(missing_fields)),
    )


def build_review_url(product_content_id: str, page: int = 0, page_size: int = 20) -> str:
    return (
        "https://apigw.trendyol.com/discovery-storefront-trproductgw-service/"
        "api/review-read/product-reviews/detailed"
        f"?contentId={product_content_id}"
        f"&page={page}"
        f"&pageSize={page_size}"
        "&channelId=1"
    )
async def fetch_trendyol_reviews(
    client: httpx.AsyncClient,
    product_content_id: str,
    page: int = 0,
    page_cookies: dict = {},
    page_size: int = 20,
) -> dict[str, Any] | None:
    url = build_review_url(product_content_id, page=page, page_size=page_size)
    from curl_cffi.requests import AsyncSession
    for attempt in range(3):
        try:
            await asyncio.sleep(attempt * 2) 
            async with AsyncSession(impersonate="chrome124") as session:
                response = await session.get(
                url,
                headers={
                    **REQUEST_HEADERS,
                    "Accept": "application/json",
                    "Origin": "https://www.trendyol.com",
                    "Referer": "https://www.trendyol.com/",
                },
                cookies=page_cookies,
                timeout=15,
            )
            if response.status_code == 429:
                await asyncio.sleep(5 + attempt * 3)
                continue
            if response.status_code >= 400:
                print(f"[WARN] Review API {response.status_code} contentId={product_content_id}")
                return None

            data = response.json()

            result = data.get("result")
            if not isinstance(result, dict):
                return None
            if not isinstance(result.get("reviews"), list):
                return None
            return data
        except (httpx.HTTPError, json.JSONDecodeError, ValueError) as e:
            print(f"[WARN] Review fetch attempt {attempt+1} failed: {e}")

    return None

def build_description_urls(product_content_id: str) -> list[str]:
    query = "storefrontId=1&culture=tr-TR"
    return [
        f"https://apigw.trendyol.com/discovery-web-productgw-service/api/productDetail/{product_content_id}?{query}",
        f"https://public.trendyol.com/discovery-web-productgw-service/api/productDetail/{product_content_id}?{query}",
        f"https://public-mdc.trendyol.com/discovery-web-productgw-service/api/productDetail/{product_content_id}?{query}",
    ]


async def fetch_first_json(client: httpx.AsyncClient, urls: list[str]) -> dict[str, Any] | None:
    tasks = [asyncio.create_task(_fetch_json(client, url)) for url in urls]
    try:
        for task in asyncio.as_completed(tasks, timeout=8):
            data = await task
            if data:
                return data
    except TimeoutError:
        return None
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()

    return None


async def _fetch_json(client: httpx.AsyncClient, url: str) -> dict[str, Any] | None:
    try:
        response = await client.get(
            url,
            headers={**REQUEST_HEADERS, "Accept": "application/json"},
            timeout=6,
        )
        if response.status_code >= 400:
            return None
        return response.json()
    except (httpx.HTTPError, json.JSONDecodeError, ValueError):
        return None


def normalize_reviews(review_response: dict[str, Any]) -> list[Review]:
    review_items = _find_review_items(review_response)
    normalized: list[Review] = []

    for item in review_items:
        text = _clean_text(
            item.get("comment")
            or item.get("text")
            or item.get("reviewComment")
            or item.get("content")
        )
        if not text:
            continue

        normalized.append(
            Review(
                rating=_as_int(item.get("rate") or item.get("rating") or item.get("score")),
                text=text,
                date=_normalize_review_date(
                    item.get("createdAt")
                    or item.get("commentDateISOtype")
                    or item.get("reviewDate")
                    or item.get("date")
                ),
                likes_count=_as_int(item.get("likesCount") or item.get("likeCount")),
                seller_name=_extract_nested_name(item.get("seller")),
            )
        )

    return normalized


def _normalize_review_date(value: Any) -> str | None:
    if value is None or value == "":
        return None

    if isinstance(value, (int, float)):
        timestamp = value / 1000 if value > 10_000_000_000 else value
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()

    text = _clean_text(value)
    if text and text.isdigit():
        timestamp_value = int(text)
        timestamp = timestamp_value / 1000 if timestamp_value > 10_000_000_000 else timestamp_value
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()

    return text


def extract_reviews_from_html(html: str) -> list[Review]:
    json_ld_product = _extract_json_ld_product(html)
    if not json_ld_product:
        return []

    review_items = json_ld_product.get("review") or []
    if isinstance(review_items, dict):
        review_items = [review_items]
    if not isinstance(review_items, list):
        return []

    reviews: list[Review] = []
    for item in review_items:
        if not isinstance(item, dict):
            continue

        review_rating = item.get("reviewRating")
        rating = None
        if isinstance(review_rating, dict):
            rating = _as_int(review_rating.get("ratingValue"))

        text = _clean_text(item.get("reviewBody"))
        if not text:
            continue

        reviews.append(
            Review(
                rating=rating,
                text=text,
                date=_clean_text(item.get("datePublished")),
                likes_count=None,
                seller_name=None,
            )
        )

    return reviews


def extract_average_rating(review_response: dict[str, Any]) -> float | None:
    value = _find_first_key(
        review_response,
        ("averageRating", "averageScore", "ratingAverage", "avgRating"),
    )
    return _as_float(value)


def normalize_descriptions(description_response: dict[str, Any]) -> dict[str, str | None]:
    descriptions = _find_first_key(description_response, ("descriptions", "descriptionList"))
    texts: list[str] = []
    seller_name = _extract_seller_name_from_json(description_response)

    if isinstance(descriptions, str):
        texts.append(_clean_text(descriptions))
    elif isinstance(descriptions, list):
        for item in descriptions:
            if not isinstance(item, dict):
                continue

            text = _clean_text(item.get("text") or item.get("description"))
            if text:
                texts.append(text)

            components = item.get("textComponents") or {}
            if isinstance(components, dict):
                pre = _clean_text(components.get("pre")) or ""
                mid = _clean_text(components.get("mid")) or ""
                post = _clean_text(components.get("post")) or ""

                if "Bu urun" in _ascii_fold(pre) and "tarafindan gonderilecektir" in _ascii_fold(post):
                    seller_name = mid or seller_name

    return {
        "seller_name": seller_name,
        "product_description": "\n".join(text for text in texts if text),
    }


def extract_product_name_from_html(html: str) -> str | None:
    json_ld_product = _extract_json_ld_product(html)
    if json_ld_product:
        name = _clean_text(json_ld_product.get("name"))
        if name:
            return name

    for key in ("productName", "name"):
        value = _extract_json_string_field(html, key)
        if value:
            return value

    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.IGNORECASE | re.DOTALL)
    if h1_match:
        value = _clean_text(_strip_tags(h1_match.group(1)))
        if value:
            return value

    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if title_match:
        value = _clean_text(_strip_tags(title_match.group(1)))
        if value:
            return re.sub(r"\s*-\s*Trendyol.*$", "", value).strip() or value

    return None


def extract_description_from_html(html: str) -> str | None:
    json_ld_product = _extract_json_ld_product(html)
    if json_ld_product:
        description = _clean_text(json_ld_product.get("description"))
        if description:
            return description

    return _extract_json_string_field(html, "description")


def extract_category_from_html(html: str) -> str | None:
    product = _extract_envoy_product(html)
    if isinstance(product, dict):
        category = product.get("category")
        if isinstance(category, dict):
            name = _clean_text(category.get("name"))
            if name:
                return name

        web_category = product.get("webCategory")
        if isinstance(web_category, dict):
            name = _clean_text(web_category.get("name"))
            if name:
                return name

    json_ld_product = _extract_json_ld_product(html)
    if json_ld_product:
        category = json_ld_product.get("category")
        if isinstance(category, str):
            return _clean_text(category)

    return None


def extract_image_url_from_html(html: str) -> str | None:
    # 1. En güvenilir yöntem: Sayfanın meta etiketlerinden (og:image) okumak
    # Bu sayede seçili olan varyantın (bordo elbise, siyah çanta vb.) ana resmi gelir.
    meta_tags = re.findall(r'<meta[^>]+>', html, re.IGNORECASE)
    for tag in meta_tags:
        if 'og:image' in tag or 'twitter:image' in tag:
            content_match = re.search(r'content=["\']([^"\']+)["\']', tag, re.IGNORECASE)
            if content_match:
                img_url = _clean_text(content_match.group(1))
                if img_url:
                    return img_url

    # 2. Fallback: JSON-LD (Base ürünü getirebilir)
    json_ld_product = _extract_json_ld_product(html)
    if json_ld_product:
        image = json_ld_product.get("image")
        if isinstance(image, str):
            return _clean_text(image)
        elif isinstance(image, list) and image:
            return _clean_text(image[0])
            
    # 3. Fallback: Envoy Object
    product = _extract_envoy_product(html)
    if isinstance(product, dict):
        images = product.get("images")
        if isinstance(images, list) and images:
            img = images[0]
            if isinstance(img, str):
                if img.startswith("http"):
                    return img
                return f"https://cdn.dsmcdn.com{img}"
                
    return None


def extract_seller_rating_from_html(html: str) -> float | None:
    product = _extract_envoy_product(html)
    if not isinstance(product, dict):
        return None

    merchant_listing = product.get("merchantListing")
    if not isinstance(merchant_listing, dict):
        return None

    merchant = merchant_listing.get("merchant")
    if not isinstance(merchant, dict):
        return None

    seller_score = merchant.get("sellerScore")
    if isinstance(seller_score, dict):
        return _as_float(seller_score.get("value"))

    return None


def extract_seller_verified_from_html(html: str) -> bool | None:
    merchant = _extract_envoy_merchant(html)
    if not isinstance(merchant, dict):
        return None

    badges = merchant.get("merchantBadges")
    if not isinstance(badges, list):
        return None

    for badge in badges:
        if not isinstance(badge, dict):
            continue

        badge_text = " ".join(
            str(value)
            for key, value in badge.items()
            if key.lower().endswith("url") or key in {"type", "name", "title", "displayName"}
        )
        normalized = _ascii_fold(badge_text).lower()
        if any(marker in normalized for marker in ("yetkilisatici", "authorized", "approved")):
            return True

    return False


def extract_merchant_id_from_html(html: str) -> str | None:
    patterns = (
        r'"merchantId"\s*:\s*(\d+)',
        r'"merchant"\s*:\s*\{[^{}]*"id"\s*:\s*(\d+)',
        r'"seller"\s*:\s*\{[^{}]*"id"\s*:\s*(\d+)',
    )
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1)
    return None


def extract_seller_name_from_html(html: str) -> str | None:
    for key in ("merchantName", "sellerName", "supplierName"):
        value = _extract_json_string_field(html, key)
        if value:
            return value

    seller_match = re.search(
        r'"(?:merchant|seller)"\s*:\s*\{[^{}]*"name"\s*:\s*"((?:\\.|[^"\\])*)"',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if seller_match:
        return _decode_json_string(seller_match.group(1))

    plain_text = _clean_text(_strip_tags(html)) or ""
    sender_match = re.search(
        r"Bu\s+urun\s+(.+?)\s+tarafindan\s+gonderilecektir",
        _ascii_fold(plain_text),
        flags=re.IGNORECASE,
    )
    if sender_match:
        return sender_match.group(1).strip()

    return None


def extract_seller_name_from_reviews(reviews: list[Review]) -> str | None:
    for review in reviews:
        if review.seller_name:
            return review.seller_name
    return None


def _extract_price_value(html: str, key: str) -> float | None:
    block_match = re.search(
        rf'"{re.escape(key)}"\s*:\s*\{{(?P<body>.*?)\}}',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not block_match:
        return None

    body = block_match.group("body")
    value_match = re.search(r'"value"\s*:\s*([0-9]+(?:\.[0-9]+)?)', body)
    if value_match:
        return float(value_match.group(1))

    text_match = re.search(r'"text"\s*:\s*"((?:\\.|[^"\\])*)"', body)
    if text_match:
        return parse_price_text(_decode_json_string(text_match.group(1)))

    return None


def _extract_price_from_envoy_product(html: str) -> dict[str, float | str | None] | None:
    product = _extract_envoy_product(html)
    if not isinstance(product, dict):
        return None

    merchant_listing = product.get("merchantListing")
    if not isinstance(merchant_listing, dict):
        return None

    price = None
    winner_variant = merchant_listing.get("winnerVariant")
    if isinstance(winner_variant, dict):
        price = winner_variant.get("price")

    if not isinstance(price, dict):
        price = merchant_listing.get("price")

    if not isinstance(price, dict):
        return None

    return _normalize_price_object(price)


def _extract_envoy_product(html: str) -> dict[str, Any] | None:
    props = _extract_envoy_shared_props(html)
    product = props.get("product") if isinstance(props, dict) else None
    return product if isinstance(product, dict) else None


def _extract_envoy_merchant(html: str) -> dict[str, Any] | None:
    product = _extract_envoy_product(html)
    if not isinstance(product, dict):
        return None

    merchant_listing = product.get("merchantListing")
    if not isinstance(merchant_listing, dict):
        return None

    merchant = merchant_listing.get("merchant")
    return merchant if isinstance(merchant, dict) else None


def _normalize_price_object(price: dict[str, Any]) -> dict[str, float | str | None]:
    discounted_price = _nested_price_value(price, "discountedPrice")
    selling_price = _nested_price_value(price, "sellingPrice")
    original_price = _nested_price_value(price, "originalPrice")

    basket_price = (
        _nested_price_value(price, "tyPlusCouponApplicablePrice")
        or _nested_price_value(price, "couponApplicablePrice")
        or _nested_price_value(price, "discountedPriceAfterNoLimitPromotions")
    )
    current_price = basket_price or discounted_price or selling_price

    return {
        "current_price": current_price,
        "selling_price": selling_price,
        "original_price": original_price,
        "discounted_price": discounted_price,
        "basket_price": basket_price,
        "currency": _clean_text(price.get("currency")) or "TRY",
    }


def _nested_price_value(price: dict[str, Any], key: str) -> float | None:
    value = price.get(key)
    if not isinstance(value, dict):
        return None

    return _as_float(value.get("value")) or parse_price_text(_clean_text(value.get("text")))


def _extract_price_from_json_ld(html: str) -> dict[str, float | str | None] | None:
    product = _extract_json_ld_product(html)
    if not product:
        return None

    offers = product.get("offers")
    if isinstance(offers, list):
        offers = next((item for item in offers if isinstance(item, dict)), None)

    if not isinstance(offers, dict):
        return None

    current_price = _as_float(offers.get("price"))
    if current_price is None:
        return None

    return {
        "current_price": current_price,
        "selling_price": current_price,
        "original_price": current_price,
        "currency": _clean_text(offers.get("priceCurrency")) or "TRY",
    }


def _extract_envoy_shared_props(html: str) -> dict[str, Any]:
    marker = 'window["__envoy__SHARED_PROPS"]'
    marker_index = html.find(marker)
    if marker_index == -1:
        return {}

    assignment_index = html.find("=", marker_index)
    if assignment_index == -1:
        return {}

    start_index = html.find("{", assignment_index)
    if start_index == -1:
        return {}

    end_index = _find_matching_brace(html, start_index)
    if end_index is None:
        return {}

    raw_json = html[start_index : end_index + 1]
    try:
        return json.loads(raw_json)
    except json.JSONDecodeError:
        return {}


def _find_matching_brace(text: str, start_index: int) -> int | None:
    depth = 0
    in_string = False
    escape = False

    for index in range(start_index, len(text)):
        char = text[index]

        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index

    return None


def _extract_currency(html: str) -> str | None:
    value = _extract_json_string_field(html, "currency")
    return value if value and len(value) == 3 else None


def parse_price_text(value: str | None) -> float | None:
    if not value:
        return None

    normalized = re.sub(r"[^\d,.]", "", value)
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


def _find_review_items(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict):
        for key in ("reviews", "comments", "content", "items"):
            value = data.get(key)
            if _looks_like_review_list(value):
                return value

        for value in data.values():
            found = _find_review_items(value)
            if found:
                return found

    if isinstance(data, list):
        if _looks_like_review_list(data):
            return data
        for item in data:
            found = _find_review_items(item)
            if found:
                return found

    return []


def _looks_like_review_list(value: Any) -> bool:
    return isinstance(value, list) and any(
        isinstance(item, dict)
        and any(key in item for key in ("comment", "text", "reviewComment"))
        and any(key in item for key in ("rate", "rating", "score"))
        for item in value
    )


def _find_first_key(data: Any, keys: tuple[str, ...]) -> Any:
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if value not in (None, ""):
                return value
        for value in data.values():
            found = _find_first_key(value, keys)
            if found not in (None, ""):
                return found

    if isinstance(data, list):
        for item in data:
            found = _find_first_key(item, keys)
            if found not in (None, ""):
                return found

    return None


def _extract_seller_name_from_json(data: Any) -> str | None:
    for key in ("merchantName", "sellerName", "supplierName"):
        value = _find_first_key(data, (key,))
        if isinstance(value, str):
            return _clean_text(value)

    for key in ("merchant", "seller", "supplier"):
        value = _find_first_key(data, (key,))
        nested_name = _extract_nested_name(value)
        if nested_name:
            return nested_name

    return None


def _extract_nested_name(value: Any) -> str | None:
    if isinstance(value, dict):
        return _clean_text(value.get("name") or value.get("sellerName") or value.get("merchantName"))
    if isinstance(value, str):
        return _clean_text(value)
    return None


def _extract_json_ld_product(html: str) -> dict[str, Any] | None:
    scripts = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )

    for script in scripts:
        try:
            data = json.loads(html_lib.unescape(script).strip())
        except json.JSONDecodeError:
            continue

        for item in _iter_json_objects(data):
            item_type = item.get("@type")
            if item_type == "Product" or (isinstance(item_type, list) and "Product" in item_type):
                return item

    return None


def _iter_json_objects(data: Any):
    if isinstance(data, dict):
        yield data
        for value in data.values():
            yield from _iter_json_objects(value)
    elif isinstance(data, list):
        for item in data:
            yield from _iter_json_objects(item)


def _extract_json_string_field(text: str, key: str) -> str | None:
    match = re.search(
        rf'"{re.escape(key)}"\s*:\s*"((?:\\.|[^"\\])*)"',
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None

    return _decode_json_string(match.group(1))


def _decode_json_string(value: str) -> str | None:
    try:
        decoded = json.loads(f'"{value}"')
    except json.JSONDecodeError:
        decoded = value
    return _clean_text(decoded)


def _strip_tags(value: str) -> str:
    return re.sub(r"<[^>]+>", " ", value)


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None

    text = html_lib.unescape(str(value))
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def _as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return parse_price_text(str(value))


def _as_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _is_ssl_certificate_error(exc: Exception) -> bool:
    return "CERTIFICATE_VERIFY_FAILED" in str(exc)


def _ascii_fold(value: str) -> str:
    return (
        value.replace("ü", "u")
        .replace("Ü", "U")
        .replace("ı", "i")
        .replace("İ", "I")
        .replace("ö", "o")
        .replace("Ö", "O")
        .replace("ğ", "g")
        .replace("Ğ", "G")
        .replace("ş", "s")
        .replace("Ş", "S")
        .replace("ç", "c")
        .replace("Ç", "C")
    )
