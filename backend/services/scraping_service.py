from models.product_schema import Product
from services.scrapers.scraper_factory import ScraperFactory


async def extract_live_product(url: str) -> Product | None:
    scraper = ScraperFactory.get_scraper(url)
    if scraper:
        return await scraper.extract_product(url)
    
    return None

