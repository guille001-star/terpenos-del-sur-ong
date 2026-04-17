from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

# Motor de base de datos con tolerancia a fallos
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Vital: revisa si la conexion está viva antes de usarla
    pool_size=5,          # Mantiene 5 conexiones listas para responder rápido
    max_overflow=10       # Si hay pico de demanda, abre hasta 10 conexiones extra
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Garantiza que la conexion se cierre siempre, evitando fugas de memoria
