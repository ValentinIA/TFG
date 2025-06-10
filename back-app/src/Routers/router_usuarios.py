from fastapi import APIRouter, HTTPException

from Models.Usuarios.crearusuario import crear_usuario
from Models.Usuarios.actualizarusuario import actualizar_usuario
from Models.Usuarios.actualizarfoto import actualizar_foto_usuario
from Models.Usuarios.actualizarpass import actualizar_pass_usuario
from Models.Usuarios.mostrarusuario import obtener_perfil_usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/crear")
def crear_usuario_endpoint(
    nombre_usuario: str,
    nombre: str,
    apellidos: str,
    email: str,
    password: str,
    foto: str = None
):
    """Crear un nuevo usuario"""
    try:
        return crear_usuario(
            nombre_usuario,
            nombre,
            apellidos,
            email.lower(),
            password,
            foto
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear usuario: {str(e)}")

@router.get("/{id}")
def obtener_usuario(id: int):
    """Obtener información de un usuario por ID"""
    try:
        return obtener_perfil_usuario(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Usuario no encontrado: {str(e)}")

@router.put("/{id}")
def actualizar_usuario_endpoint(
    id: int,
    nombre_usuario: str,
    nombre: str,
    apellidos: str,
    email: str
):
    """Actualizar datos de usuario"""
    try:
        return actualizar_usuario(
            nombre_usuario,
            nombre,
            apellidos,
            email,
            id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar usuario: {str(e)}")

@router.put("/{id}/password")
def cambiar_password(
    id: int,
    password: str
):
    """Cambiar contraseña de usuario"""
    try:
        return actualizar_pass_usuario(password, id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al cambiar contraseña: {str(e)}")

@router.put("/{id}/foto")
def cambiar_foto(
    id: int,
    foto: str
):
    """Cambiar foto de perfil de usuario"""
    try:
        return actualizar_foto_usuario(foto, id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al cambiar foto: {str(e)}")
