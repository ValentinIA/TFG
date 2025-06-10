import random
import requests
from bs4 import BeautifulSoup

def get_parser():
    try:
        # Intentar usar lxml primero
        import lxml
        return "lxml"
    except ImportError:
        # Si no está disponible, usar el parser por defecto
        return "html.parser"

def get_producto_mediamarkt(url):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    ]

    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        respuesta = requests.get(url, headers=headers, timeout=10)
        respuesta.raise_for_status()
        parser = get_parser()
        soup = BeautifulSoup(respuesta.text, parser)

        titulo = (
            soup.find("div", attrs={"data-test": "mms-select-details-header"})
            .find("h1")
            .get_text(strip=True)
        ) if soup.find("div", attrs={"data-test": "mms-select-details-header"}) else "Título no encontrado"

        precio_elem = soup.find("span", {"class": "sc-e0c7d9f7-0 bPkjPs"})
        if precio_elem and precio_elem.get_text():
            precio_text = precio_elem.get_text(strip=True)
            precio = float(precio_text[:-1].replace(",", ".").strip())
        else:
            precio = -1

        imagen_elem = soup.find("img", {"class": "sc-3c06cab3-1 iGTXmo pdp-gallery-image"})
        imagen_url = imagen_elem["src"] if imagen_elem else None

        return titulo, precio, imagen_url
    except Exception as e:
        return "Error", -1, None

def get_lista_productos_mediamarkt(producto):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    ]

    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        url = f"https://www.mediamarkt.es/es/search.html?query={producto}"
        respuesta = requests.get(url, headers=headers, timeout=10)
        respuesta.raise_for_status()
        
        parser = get_parser()
        soup = BeautifulSoup(respuesta.text, parser)

        links = soup.find_all(
            "a",
            attrs={
                "data-test": lambda x: x
                and (
                    "mms-router-link-product-list-item-link" in x
                    or "mms-router-link-product-list-item-link_mp" in x
                )
            },
            href=True,
        )

        lista_urls = [
            "https://www.mediamarkt.es" + link["href"]
            for link in links[:10]
        ]

        lista_productos = []
        for url_producto in lista_urls:
            titulo, precio, imagen_url = get_producto_mediamarkt(url_producto)
            if precio == -1:
                continue
            obj_producto = {
                "titulo": titulo,
                "precio": precio,
                "tienda": "MediaMarkt",
                "imagen_url": imagen_url,
                "url": url_producto,
            }
            lista_productos.append(obj_producto)

        return lista_productos
    except Exception as e:
        return []
