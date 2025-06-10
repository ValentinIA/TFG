from fastapi import APIRouter, HTTPException
from Scripts.ScrapAmazone import get_productos_Amazon
from Scripts.ScrapFnac import get_productos_Fnac
from Scripts.ScrapMediaMarkt import get_productos_MediaMark

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/amazon/{producto}")
async def obtener_productos_amazon(producto: str):
    """Obtener productos de Amazon"""
    try:
        return await get_productos_Amazon(producto)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener productos de Amazon: {str(e)}"
        )


@router.get("/fnac/{producto}")
async def obtener_productos_fnac(producto: str):
    """Obtener productos de Fnac"""
    try:
        return await get_productos_Fnac(producto)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener productos de Fnac: {str(e)}"
        )


@router.get("/mediamarkt/{producto}")
async def obtener_productos_mediamarkt(producto: str):
    """Obtener productos de MediaMarkt"""
    try:
        return await get_productos_MediaMark(producto)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener productos de MediaMarkt: {str(e)}",
        )


@router.get("/todos/{producto}")
async def buscar_en_todas_las_tiendas(producto: str):
    """Buscar un producto en todas las tiendas disponibles"""
    resultados = []

    try:
        resultados.extend(await get_productos_Amazon(producto))
    except Exception as e:
        resultados.append({"error": f"Amazon: {str(e)}"})

    try:
        resultados.extend(await get_productos_Fnac(producto))
    except Exception as e:
        resultados.append({"error": f"Fnac: {str(e)}"})

    try:
        resultados.extend(await get_productos_MediaMark(producto))
    except Exception as e:
        resultados.append({"error": f"MediaMark: {str(e)}"})

    return resultados
