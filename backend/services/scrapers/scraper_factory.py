from services.scrapers.base_scraper import BaseScraper
from services.scrapers.trendyol_scraper import TrendyolScraper
from services.scrapers.amazon_scraper import AmazonScraper

class ScraperFactory:
    @staticmethod
    def get_scraper(url: str) -> BaseScraper | None:
        """
        Gelen URL'e göre uygun scraper sınıfını döndürür.
        """
        if "trendyol.com" in url:
            return TrendyolScraper()
        elif "amazon.com" in url or "amazon.com.tr" in url:
            return AmazonScraper()
        
        return None
