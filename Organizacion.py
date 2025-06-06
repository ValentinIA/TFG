

# API/Routers/favoritos_router.py (NUEVO ARCHIVO)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from API.Models.crearfavorito import favorito_nuevo
from API.Models.mostrarfavorito import mostrar_favoritos as modelo_mostrar_favoritos
from API.Models.mostrarportada import mostrar_portada as modelo_mostrar_portada
from API.Models.eliminarFavorito import eliminar_favorito

router = APIRouter(prefix="/favoritos", tags=["Favoritos"])

class FavoritoCreate(BaseModel):
    titulo: str
    precio: str
    imagen_url: str
    url: str
    id_usuario: str
    tienda: str

class FavoritoDelete(BaseModel):
    titulo: str

@router.post("/crear")
def crear_favorito(favorito: FavoritoCreate):
    """Crear un nuevo favorito"""
    try:
        return favorito_nuevo(
            favorito.titulo,
            favorito.precio,
            favorito.imagen_url,
            favorito.url,
            favorito.id_usuario,
            favorito.tienda
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear favorito: {str(e)}")

@router.get("/usuario/{id}")
def obtener_favoritos(id: int):
    """Obtener todos los favoritos de un usuario"""
    try:
        return modelo_mostrar_favoritos(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener favoritos: {str(e)}")

@router.get("/portada")
def obtener_portada():
    """Obtener productos para la portada"""
    try:
        return modelo_mostrar_portada()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener portada: {str(e)}")

@router.delete("/usuario/{id}")
def eliminar_favorito_usuario(id: int, favorito_data: FavoritoDelete):
    """Eliminar un favorito de usuario"""
    try:
        return eliminar_favorito(id, favorito_data.titulo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar favorito: {str(e)}")

# Mantener compatibilidad con endpoints antiguos
@router.get("/mostrar_favorito/")
def mostrar_favorito_legacy(id: int):
    """Endpoint legacy para mostrar favoritos (mantener compatibilidad)"""
    return modelo_mostrar_favoritos(id)

@router.get("/mostrar_portada/")
def mostrar_portada_legacy():
    """Endpoint legacy para mostrar portada (mantener compatibilidad)"""
    return modelo_mostrar_portada()

@router.post("/crear_favorito/")
def crear_favorito_legacy(
    titulo: str, precio: str, imagen_url: str, url: str, id_usuario: str, tienda: str
):
    """Endpoint legacy para crear favorito (mantener compatibilidad)"""
    return favorito_nuevo(titulo, precio, imagen_url, url, id_usuario, tienda)

@router.post("/eliminar_favorito/")
def eliminar_favorito_legacy(id: int, titulo: str):
    """Endpoint legacy para eliminar favorito (mantener compatibilidad)"""
    return eliminar_favorito(id, titulo)


# API/Routers/__init__.py (NUEVO ARCHIVO)
# Archivo vacío para hacer del directorio un paquete Python