from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth_router, items_router

# Crea las tablas en PostgreSQL si no existen (basado en models.py)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API REST con FastAPI, JWT y PostgreSQL",
    description="Proyecto de portafolio: autenticación, CRUD protegido y base de datos relacional",
    version="1.0.0",
)

# CORS: permite que tu frontend (React en otro puerto) pueda llamar a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción, poné aquí la URL real de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(items_router.router)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}
