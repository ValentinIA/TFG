import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


def get_producto_pccomponentes(url):
    # Configurar navegador
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 2)

    try:
        driver.get(url)

        # Obtener título
        try:
            title_elem = wait.until(
                EC.presence_of_element_located((By.ID, "pdp-title"))
            )
            title = title_elem.text.strip()
        except Exception:
            title = "Título no encontrado"

        # Obtener precio
        try:
            # Esperar a que esté el span con el precio completo
            precio_entero_element = wait.until(
                EC.presence_of_element_located((By.ID, "pdp-price-current-integer"))
            )

            # Obtener el contenido como texto directo del DOM
            precio = precio_entero_element.get_attribute("textContent").strip()
            precio = float(precio[:-1].replace(",", "."))

        except Exception as e:
            precio = -1

        # Obtener imagen
        try:
            image_elem = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#pdp-section-images img")
                )
            )
            image_url = image_elem.get_attribute("src")
            if image_url.startswith("//"):
                image_url = "https:" + image_url
        except Exception:
            image_url = None

    finally:
        driver.quit()

    return title, precio, image_url


def get_lista_productos_pccomponentes(producto):

    url_producto = f"https://www.pccomponentes.com/search/?query={producto}"

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 4)

    lista_urls = []

    try:
        driver.get(url_producto)

        try:
            boton_cookies = wait.until(
                EC.element_to_be_clickable((By.ID, "cookiesAcceptAll"))
            )
            boton_cookies.click()
            time.sleep(1)
        except:
            pass

        enlaces = driver.find_elements(By.XPATH, '//a[contains(@class, "sc-jTrPJq")]')

        for enlace in enlaces:
            url = enlace.get_attribute("href")
            if url and url not in lista_urls:
                lista_urls.append(url)
            if len(lista_urls) >= 1:
                break

    except:
        lista_urls = []
        return lista_urls

    finally:
        driver.quit()

    print(lista_urls)

    lista_productos = []
    for url_producto in lista_urls:
        titulo, precio, imagen_url = get_producto_pccomponentes(url_producto)
        if precio == -10:
            continue
        obj_producto = {
            "titulo": titulo,
            "precio": precio,
            "tienda": "PCComponentes",
            "imagen_url": imagen_url,
            "url": url_producto,
        }
        lista_productos.append(obj_producto)

    return lista_productos
