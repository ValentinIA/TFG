from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ScrapAmazone import get_lista_productos_amazone
from ScrapMediaMarkt import get_lista_productos_mediamarkt
from ScrapPcComponentes import get_lista_productos_pccomponentes

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # o ["*"] si es desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_productos_amazone/{producto}")
def get_productos(producto: str):
    return get_lista_productos_amazone(producto)


@app.get("/get_productos_mediamarkt/{producto}")
def get_productos(producto: str):
    return get_lista_productos_mediamarkt(producto)

@app.get("/get_productos_pccomponentes/{producto}")
def get_productos(producto: str):
    return get_lista_productos_pccomponentes(producto)

