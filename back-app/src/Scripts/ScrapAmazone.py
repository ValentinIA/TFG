from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import json


async def get_productos_Amazon(producto):

    # Configuración del browser que usará
    browser_config = BrowserConfig(browser_type="chromium", headless=True)

    # Reglas para localizar contenido
    crawler_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(
            schema={
                "name": "Amazon Product Search Results",
                "baseSelector": "[data-component-type='s-search-result']",
                "fields": [
                    {"name": "title", "selector": "h2 span", "type": "text"},
                    {
                        "name": "url",
                        "selector": "a.a-link-normal.s-no-outline",
                        "type": "attribute",
                        "attribute": "href",
                    },
                    {
                        "name": "image",
                        "selector": ".s-image",
                        "type": "attribute",
                        "attribute": "src",
                    },
                                        {
                        "name": "price",
                        "selector": ".a-price .a-offscreen",
                        "type": "text",
                    },
                ],
            }
        )
    )

    # Url que scrappeará
    url = f"https://www.amazon.es/s?k={producto}"

    # Función que devuelve el json con los datos
    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Extrae los datos
        result = await crawler.arun(url=url, config=crawler_config)

        products = json.loads(result.extracted_content)

        lista_productos = []

        for product in products:
            
            price = product.get("price", "").strip()

            if price.startswith("€"):
                price = price.replace("€", "").strip()
            else:
                price = price.replace(".", "").replace(",", ".").replace("€", "").strip()

            try:
                price = float(price)
            except ValueError:
                continue
        
            lista_productos.append(
                {
                    "titulo": product["title"],
                    "precio": price,
                    "tienda": "Amazon",
                    "imagen_url": product.get("image"),
                    "url": f"https://www.amazon.es{product.get('url')}",
                }
            )

            if len(lista_productos) == 10:
                break

    return lista_productos