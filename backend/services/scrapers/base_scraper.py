from abc import ABC, abstractmethod
from typing import Optional
from models.product_schema import Product

class BaseScraper(ABC):
    @abstractmethod
    async def extract_product(self, url: str) -> Optional[Product]:
        """
        Gelen URL üzerinden ürün detaylarını (isim, fiyat, vb.)
        asenkron olarak kazıyıp Product nesnesi olarak döndürür.
        """
        pass
