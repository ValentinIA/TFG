from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.Scripts.ScrapAmazone import get_productos_amazon
from API.Scripts.ScrapFnac import get_productos_fnac
from API.Scripts.ScrapMediaMarkt import get_productos_MediaMark

from API.Models.crearusuario import usuario_nuevo
from API.Models.iniciosesion import comprobarpass
from API.Models.crearfavorito import favorito_nuevo
from API.Models.actualizarusuario import actualizarusuario
from API.Models.mostrarfavorito import mostrarfavoritos
from API.Models.mostrarportada import mostrarportada
from API.Models.mostrarusuario import mostrar_perfil
from API.Models.eliminarFavorito import eliminar_favorito


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
    return await get_productos_amazon(producto)


@app.get("/get_productos_fnac/{producto}")
async def get_lista_productos_fnac(producto: str):
    return await get_productos_fnac(producto)

@app.get("/get_productos_MediaMarkt/{producto}")
async def get_lista_productos_MediaMarkt(producto: str):
    return await get_productos_MediaMark(producto)


@app.post("/crear_usuario/")
def crear_usuario(
    nombre_usuario: str,
    nombre: str,
    apellidos: str,
    email: str,
    password: str,
    foto: str = None,
):
    usuario = usuario_nuevo(
        nombre_usuario, nombre, apellidos, email.lower(), password, foto
    )
    return usuario


@app.get("/loguear_ususario/")
def loguear_ususario(email: str, password: str):
    usuario = comprobarpass(email, password)
    return usuario


@app.post("/crear_favorito/")
def crear_favorito(
    titulo: str, precio: str, imagen_url: str, url: str, id_usuario: str, tienda: str
):
    return favorito_nuevo(titulo, precio, imagen_url, url, id_usuario, tienda)


@app.post("/actualizar_usuario/")
def actualizar_usuario(
    nombre_usuario: str,
    nombre: str,
    apellidos: str,
    email: str,
    password: str,
    foto: str,
    id: int,
):
    return actualizarusuario(
        nombre_usuario, nombre, apellidos, email, password, foto, id
    )


@app.get("/mostrar_favorito/")
def mostrar_favorito(id: int):
    return mostrarfavoritos(id)


@app.get("/mostrar_portada/")
def mostrar_portada():
    return mostrarportada()


@app.get("/mostrar_usuario/")
def mostrar_usuario(id: int):
    return mostrar_perfil(id)


@app.post("/eliminar_favorito/")
def eliminarfavorito(ide: int, titulo: str):
    return eliminar_favorito(ide, titulo)
