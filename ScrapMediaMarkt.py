import random
import requests
from bs4 import BeautifulSoup


def get_producto(url):

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
    }

    respuesta = requests.get(url, headers=headers)
    soup = BeautifulSoup(respuesta.text, "lxml")

    try:
        titulo = soup.find("div", attrs={"data-test": "mms-select-details-header"}).find("h1").get_text(strip=True)
    except AttributeError:
        titulo = "Título no encontrado"
    try:
        precio = soup.find("span", {"class": "sc-e0c7d9f7-0 bPkjPs"}).get_text(strip=True)
    except AttributeError:
        precio = "Precio no encontrado"
    try:
        imagen_url = soup.find("img", {"class": "sc-3c06cab3-1 iGTXmo pdp-gallery-image"})["src"]
    except (AttributeError, TypeError):
        imagen_url = None


    return titulo, precio, imagen_url


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
    }

    url = f"https://www.mediamarkt.es/es/search.html?query={producto}"
    respuesta = requests.get(url, headers=headers)
    soup = BeautifulSoup(respuesta.text, "lxml")

    lista_urls = [
        "https://www.mediamarkt.es" + link["href"]
        for link in soup.find_all(
            "a", 
            attrs={"data-test": lambda x: x and ("mms-router-link-product-list-item-link" in x or "mms-router-link-product-list-item-link_mp" in x)},
            href=True,
        )[:10]
    ]

    lista_productos = []
    for url_producto in lista_urls:
        titulo, precio, imagen_url = get_producto(url_producto)
        obj_producto = {
            "titulo": titulo,
            "precio": precio,
            "imagen_url": imagen_url,
            "url": url_producto,
        }
        lista_productos.append(obj_producto)

    return lista_productos