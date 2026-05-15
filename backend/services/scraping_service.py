from models.product_schema import Product


def extract_live_product(url: str) -> Product | None:
    # SRS'e gore canli extraction experimental. MVP stabilitesi icin simdilik fallback'e izin verilir.
    return None

