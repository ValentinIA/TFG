from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import json


async def get_productos_MediaMark(producto):

    # Configuración del browser que usará
    browser_config = BrowserConfig(browser_type="chromium", headless=True)

    # Reglas para localizar contenido
    crawler_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(
            schema={
                "name": "Mediamarkt Product Search Results",
                "baseSelector": ".sc-bd3ffc80-0",
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

    # Url que scrappeará
    url = f"https://www.mediamarkt.es/es/search.html?query={producto}"

    # Función que devuelve el json con los datos
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Extrae los datos
        result = await crawler.arun(url=url, config=crawler_config)

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
                    "titulo": product.get("title"),
                    "precio": price,
                    "tienda": "MediaMarkt",
                    "imagen_url": product.get("image"),
                    "url": f"https://www.mediamarkt.es{product.get('url')}",
                }
            )

            if len(lista_productos) == 10:
                break

    return lista_productos