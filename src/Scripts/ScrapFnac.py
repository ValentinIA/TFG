from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import json

async def get_productos_Fnac(producto):
    browser_config = BrowserConfig(browser_type="chromium", headless=True)

    crawler_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(
            schema={
                "name": "Fnac Product Search Results",
                "baseSelector": "div.Article-item",
                "fields": [
                    {"name": "title", "selector": "a.Article-title", "type": "text"},
                    {
                        "name": "url",
                        "selector": "a.Article-title",
                        "type": "attribute",
                        "attribute": "href",
                    },
                    {
                        "name": "image_url",
                        "selector": "div.zoomHover__zoomer",
                        "type": "regex",
                        "attribute": "style",
                        "regex_pattern": r"url\('([^']+)'\)"
                    },
                    {"name": "price", "selector": "strong.userPrice", "type": "text"},
                ],
            }
        )
    )

    url = f"https://www.fnac.es/SearchResult/ResultList.aspx?Search={producto}"

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=crawler_config)

        if result and result.extracted_content:
            products = json.loads(result.extracted_content)

            lista_productos = []

            for product in products:

                price = product.get("price").replace(".", "").replace(",", ".").replace("€", "").strip()
            
                try:
                    price = float(price)
                except ValueError:
                    continue

                lista_productos.append(
                    {
                        "titulo": product["title"],
                        "precio": price,
                        "tienda": "Fnac",
                        "imagen_url": product.get("image_url"),
                        "url": product.get("url"),
                    }
                )

                if len(lista_productos) == 10:
                    break
    return lista_productos