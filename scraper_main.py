# scraper_main.py

from concurrent.futures import ThreadPoolExecutor
from scraper_worker import scrape_website

# Website details
website_configs = [
    {
        "name": "Virgio",
        "url": "https://www.virgio.com",
        "collections": ["https://www.virgio.com/collections/all"],
        "product_pattern": "/products/",
        "max_products": 1000
    },
    {
        "name": "NykaaFashion",
        "url": "https://www.nykaafashion.com",
        "collections": ["https://www.nykaafashion.com/women/c/6557"],
        "product_pattern": "/p/",
        "max_products": 300
    },
    {
        "name": "TataCliq",
        "url": "https://www.tatacliq.com",
        "collections": ["https://www.tatacliq.com/mens-clothing/c-msh11"],
        "product_pattern": "/p-",
        "max_products": 300
    },
    {
        "name": "Westside",
        "url": "https://www.westside.com",
        "collections": ["https://www.westside.com/collections/new-in-western-wear-for-women"],
        "product_pattern": "/products/",
        "max_products": 300
    }
]

# Run all scrapers in parallel
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(scrape_website, website_configs)
