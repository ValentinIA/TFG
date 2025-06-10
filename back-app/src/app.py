from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar los routers
from Routers.router_auth import router as router_auth
from Routers.router_index import router as router_index
from Routers.router_usuarios import router as router_usuarios
from Routers.router_productos import router as router_productos
from Routers.router_favoritos import router as router_favoritos 

app = FastAPI(
    title="API de BuyPilot",
    description="API para scraping de productos y gestión de usuarios",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(router_auth, prefix="/api/v1")
app.include_router(router_index, prefix="/api/v1") 
app.include_router(router_usuarios, prefix="/api/v1")
app.include_router(router_productos, prefix="/api/v1") 
app.include_router(router_favoritos, prefix="/api/v1")

# Endpoints de salud
@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}
