import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# El "engine" es la conexión real con PostgreSQL
engine = create_engine(DATABASE_URL)

# SessionLocal genera una "conversación" con la base de datos por cada request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase de la que van a heredar todos nuestros modelos (tablas)
Base = declarative_base()


def get_db():
    """
    Esta función crea una sesión de base de datos para un request,
    la entrega, y la cierra automáticamente al terminar (incluso si hay error).
    FastAPI la va a usar como 'dependencia' en cada endpoint que necesite la DB.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
