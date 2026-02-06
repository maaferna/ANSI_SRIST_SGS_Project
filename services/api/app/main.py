from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.csirt import router as csirt_router

app = FastAPI(title="ANSI SRIST API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://159.138.245.234",
        "http://159.138.245.234:80",
        # agrega aquí tu dominio real si aplica (ideal)
    ],
    allow_credentials=False,
    allow_methods=["*"],   # incluye OPTIONS
    allow_headers=["*"],   # incluye content-type
)

# OJO: aquí NO uses prefix="/api" si ya lo recorta Nginx
app.include_router(csirt_router)
