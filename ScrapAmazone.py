import random
import requests
from bs4 import BeautifulSoup


def get_producto_amazon(url):

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
        titulo = soup.find("span", id="productTitle").get_text(strip=True)
    except AttributeError:
        titulo = "Título no encontrado"
    try:
        precio = soup.find("span", {"class": "a-offscreen"}).get_text(strip=True)
    except AttributeError:
        precio = "Precio no encontrado"
    try:
        imagen_url = soup.find(id="landingImage")["src"]
    except (AttributeError, TypeError):
        imagen_url = None

    return titulo, precio, imagen_url


def get_lista_productos_amazon(producto):
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

    url = f"https://www.amazon.es/s?k={producto}"
    respuesta = requests.get(url, headers=headers)
    soup = BeautifulSoup(respuesta.text, "lxml")

    lista_urls = [
        "https://www.amazon.es" + link["href"]
        for link in soup.find_all(
            "a",
            {"class": "a-link-normal s-line-clamp-4 s-link-style a-text-normal"},
            href=True,
        )[:10]
    ]

    lista_productos = []
    for url_producto in lista_urls:
        titulo, precio, imagen_url = get_producto_amazon(url_producto)
        obj_producto = {
            "titulo": titulo,
            "precio": precio,
            "imagen_url": imagen_url,
            "url": url_producto
        }
        lista_productos.append(obj_producto)

    return lista_productos
