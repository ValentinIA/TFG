from fastapi import APIRouter, HTTPException
from Models.Auth.login import comprobar_pass

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login_usuario(email: str, password: str):
    """Iniciar sesión de usuario"""
    try:
        return comprobar_pass(email, password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error en el login: {str(e)}")
