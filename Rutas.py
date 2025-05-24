from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ScrapAmazone import get_lista_productos_amazon as obtener_productos_amazon
from ScrapMediaMarkt import get_lista_productos_mediamarkt, get_producto_mediamarkt
from ScrapPcComponentes import (
    get_lista_productos_pccomponentes,
    get_producto_pccomponentes,
)
from crearusuario import usuario_nuevo
from mostrarusuario import comprobar_pass
from crearfavorito import favorito_nuevo

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # o ["*"] si es desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_productos_amazon/{producto}")
async def get_lista_productos_amazon(producto: str):
    return await obtener_productos_amazon(producto)


@app.get("/get_productos_mediamarkt/{producto}")
def get_productos_mediamarkt(producto: str):
    return get_lista_productos_mediamarkt(producto)


@app.get("/get_productos_pccomponentes/{prourlducto}")
def get_productos_pccomponentes(producto: str):
    return get_lista_productos_pccomponentes(producto)


@app.get("/get_producto_mediamarkt/{url:path}")
def get_productos_mediamarkt(url: str):
    titulo, precio, imagen_url = get_producto_mediamarkt(url)
    return {"titulo": titulo, "precio": precio, "imagen_url": imagen_url, "url": url}


@app.get("/get_producto_pccomponente/{url:path}")
def get_productos_pccomponentes(url: str):
    titulo, precio, imagen_url = get_producto_pccomponentes(url)
    return {"titulo": titulo, "precio": precio, "imagen_url": imagen_url, "url": url}


@app.post("/crear_usuario/")
def crear_usuario(
    nombre_usuario: str,
    nombre: str,
    apellidos: str,
    email: str,
    password: str,
    foto: str,
):
    usuario = usuario_nuevo(nombre_usuario, nombre, apellidos, email, password, foto)
    return usuario


@app.get("/loguear_ususario/")
def loguear_ususario(email: str, password: str):
    usuario = comprobar_pass(email, password)
    return usuario


@app.post("/crearfavorito/")
def crearfavorito(
    titulo: str, precio: str, imagen_url: str, url: str, id_usuario: str, tienda: str
):
    return favorito_nuevo(titulo, precio, imagen_url, url, id_usuario, tienda)
