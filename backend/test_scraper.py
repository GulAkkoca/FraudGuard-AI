import asyncio
import sys

# To ensure imports work
import os
sys.path.insert(0, os.path.abspath("."))

from services.scrapers.trendyol_scraper import TrendyolScraper

async def main():
    scraper = TrendyolScraper()
    product = await scraper.extract_product("https://www.trendyol.com/icollagen/kolajen-ve-prebiyotik-tablet-p-752356123")
    if product:
        print("BULDUM:", product.name)
    else:
        print("BULAAMADIM, None döndü.")

if __name__ == "__main__":
    # Windows'ta playwright için bazen bu policy gerekebiliyor
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
