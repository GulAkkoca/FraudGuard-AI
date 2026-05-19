import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath("."))

from services.scrapers.trendyol_scraper import fetch_trendyol_html


async def main():
    url = "https://www.trendyol.com/icollagen/kolajen-ve-prebiyotik-tablet-p-752356123"
    html = await fetch_trendyol_html(url)
    with open("dump.html", "w", encoding="utf-8") as file:
        file.write(html)
    print("DUMPED!")


if __name__ == "__main__":
    asyncio.run(main())
