import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath("."))

from services.scrapers.trendyol_scraper import (
    extract_description_from_html,
    extract_price_from_html,
    extract_product_name_from_html,
    fetch_trendyol_html,
)


async def main():
    url = "https://www.trendyol.com/icollagen/kolajen-ve-prebiyotik-tablet-p-752356123"
    html = await fetch_trendyol_html(url)

    print("NAME:", extract_product_name_from_html(html))
    print("DESCRIPTION:", extract_description_from_html(html))
    print("PRICE:", extract_price_from_html(html))


if __name__ == "__main__":
    asyncio.run(main())
