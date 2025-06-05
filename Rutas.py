from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.Scripts.ScrapAmazone import get_productos_Amazon
from API.Scripts.ScrapFnac import get_productos_Fnac
from API.Scripts.ScrapMediaMarkt import get_productos_MediaMark

from API.Models.crearusuario import usuario_nuevo
from API.Models.iniciosesion import comprobar_pass
from API.Models.crearfavorito import favorito_nuevo
from API.Models.actualizarusuario import actualizar_usuario
from API.Models.actualizarfoto import actualizar_foto
from API.Models.actualizarpass import actualizar_pass
from API.Models.mostrarfavorito import mostrar_favoritos
from API.Models.mostrarportada import mostrar_portada
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


@app.get("/get_productos_Amazon/{producto}")
async def get_lista_productos_Amazon(producto: str):
    return await get_productos_Amazon(producto)


@app.get("/get_productos_Fnac/{producto}")
async def get_lista_productos_Fnac(producto: str):
    return await get_productos_Fnac(producto)


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
    usuario = comprobar_pass(email, password)
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
    id: int,
):
    return actualizar_usuario(nombre_usuario, nombre, apellidos, email, id)


@app.post("/actualizar_pass/")
def actualizar_foto(
    foto: str,
    id: int,
):
    return actualizar_foto(foto, id)


@app.post("/actualizar_foto/")
def actualizar_foto(
    password: str,
    id: int,
):
    return actualizar_pass(password, id)


@app.get("/mostrar_favorito/")
def mostrar_favorito(id: int):
    return mostrar_favoritos(id)


@app.get("/mostrar_portada/")
def mostrar_portada():
    return mostrar_portada()


@app.get("/mostrar_usuario/")
def mostrar_usuario(id: int):
    return mostrar_perfil(id)


@app.post("/eliminar_favorito/")
def eliminarfavorito(ide: int, titulo: str):
    return eliminar_favorito(ide, titulo)
