from fastapi import APIRouter, HTTPException

from Models.Index.mostrarportada import mostrar_portada as modelo_mostrar_portada

router = APIRouter(prefix="/index", tags=["Index"])


@router.get("/portada")
def obtener_portada():
    """Obtener productos para la portada"""
    try:
        return modelo_mostrar_portada()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener portada: {str(e)}")