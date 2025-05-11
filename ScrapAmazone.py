from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import json
from urllib.parse import urljoin

async def get_lista_productos_amazon(producto):

    # Configuración del browser que usará
    browser_config = BrowserConfig(browser_type="chromium", headless=True)

    # Reglas para localizar contenido
    crawler_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(
            schema={
                "name": "Amazon Product Search Results",
                "baseSelector": "[data-component-type='s-search-result']",
                "fields": [
                    {
                        "name": "title",
                        "selector": "h2 span",
                        "type": "text"
                    },
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
                    }
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

        # Formatear datos
        if result and result.extracted_content:
            
            # Se convierte el JSON en un array de productos
            products = json.loads(result.extracted_content)

            # Productos válidos
            lista_productos = []

            for product in products:
                title = product.get('title', '')
                # Truncar el título en el primer ":"
                title = title.split(':')[0].strip()
                product['title'] = title

                if producto.lower() in product['title'].lower():
                    # Formateo de url, se le añade https://amazon.es al inicio
                    product_url = product.get('url', '')
                    if not product_url.startswith('http'):
                        product['url'] = urljoin('https://amazon.es', product_url) 
                    
                    # Eliminar el punto en el precio
                    price = product.get('price', '').replace('.', '').strip()

                    if not price:
                        continue

                    # Formatear el objeto final
                    lista_productos.append({
                        "titulo": product['title'],
                        "precio": price,
                        "tienda": "Amazon",
                        "imagen_url": product.get('image'),
                        "url": product.get('url')
                    })

                    if len(lista_productos) == 10:
                        break

            return lista_productos
    
    return []
