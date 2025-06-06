from fastapi import APIRouter, HTTPException

from Models.Favoritos.crearfavorito import favorito_nuevo
from Models.Favoritos.mostrarfavorito import mostrar_favoritos
from Models.Favoritos.eliminarFavorito import eliminar_favorito

router = APIRouter(prefix="/favoritos", tags=["Favoritos"])

@router.post("/crear")
def crear_favorito(
    titulo: str,
    precio: str,
    imagen_url: str,
    url: str,
    id_usuario: str,
    tienda: str
):
    """Crear un nuevo favorito"""
    try:
        return favorito_nuevo(
            titulo,
            precio,
            imagen_url,
            url,
            id_usuario,
            tienda
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear favorito: {str(e)}")

@router.get("/usuario/{id}")
def obtener_favoritos(id: int):
    """Obtener todos los favoritos de un usuario"""
    try:
        return mostrar_favoritos(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener favoritos: {str(e)}")

@router.delete("/usuario/{id}")
def eliminar_favorito_usuario(id: int, titulo: str):
    """Eliminar un favorito de usuario"""
    try:
        return eliminar_favorito(id, titulo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar favorito: {str(e)}")

