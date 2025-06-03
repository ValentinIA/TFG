from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import json


async def extract_mediamarkt_products():
    browser_config = BrowserConfig(browser_type="chromium", headless=True)

    crawler_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(
            schema={
                "name": "Mediamarkt Product Search Results",
                "baseSelector": ".sc-bd3ffc80-0.cZxRmA",
                "fields": [
                    {
                        "name": "title",
                        "selector": "[data-test='product-title']",
                        "type": "text"
                    },
                    {
                        "name": "url",
                        "selector": "a[data-test='mms-router-link']",
                        "type": "attribute",
                        "attribute": "href",
                    },
                    {
                        "name": "image",
                        "selector": "[data-test='product-image'] img",
                        "type": "attribute",
                        "attribute": "src",
                    },
                    {
                        "name": "price",
                        "selector": "span.sc-e0c7d9f7-0.bPkjPs",
                        "type": "text",
                    },
                ],
            }
        )
    )

    url = "https://www.mediamarkt.es/es/search.html?query=Samsung+Galaxy+Tab"

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=crawler_config)

        if result and result.extracted_content:
            products = json.loads(result.extracted_content)
            
            for product in products:
                print("\nProduct Details:")
                print(f"Title: {product.get('title')}")
                print(f"Price: {product.get('price')}")
                print(f"Url: https://www.mediamarkt.es{product.get('url')}")
                print(f"Image: {product.get('image')}")

if __name__ == "__main__":
    import asyncio

    asyncio.run(extract_mediamarkt_products())