import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath("."))

from services.scrapers.trendyol_scraper import (
    extract_merchant_id_from_html,
    extract_price_from_html,
    extract_product_content_id,
    extract_product_name_from_html,
    extract_seller_name_from_html,
    fetch_trendyol_html,
)


async def main():
    url = "https://www.trendyol.com/icollagen/kolajen-ve-prebiyotik-tablet-p-752356123"
    html = await fetch_trendyol_html(url)

    print("PRODUCT CONTENT ID:", extract_product_content_id(url))
    print("TITLE:", extract_product_name_from_html(html))
    print("PRICE:", extract_price_from_html(html))
    print("MERCHANT ID:", extract_merchant_id_from_html(html))
    print("SELLER:", extract_seller_name_from_html(html))


if __name__ == "__main__":
    asyncio.run(main())
