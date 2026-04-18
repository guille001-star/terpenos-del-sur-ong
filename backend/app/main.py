from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from pydantic import BaseModel, EmailStr
from datetime import date
import uuid

from .core.config import settings
from .core.database import get_db
from .models.models import Socio

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

# CORS Dinámico: Ahora lee la URL real del entorno
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SocioCreate(BaseModel):
    dni: str
    nombre_completo: str
    correo: EmailStr

@app.get("/health")
def check_health(db = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "PostgreSQL connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

@app.post("/api/socios")
def crear_socio(socio_data: SocioCreate, db = Depends(get_db)):
    nuevo_socio = Socio(
        id=uuid.uuid4(),
        dni=socio_data.dni,
        nombre_completo=socio_data.nombre_completo,
        correo=socio_data.correo,
        fecha_alta=date.today(),
        esta_activo=True
    )
    try:
        db.add(nuevo_socio)
        db.commit()
        db.refresh(nuevo_socio)
        return {"mensaje": "Socio creado exitosamente", "id": str(nuevo_socio.id)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al guardar: {str(e)}")

@app.get("/api/socios")
def obtener_socios(db = Depends(get_db)):
    socios = db.query(Socio).order_by(Socio.nombre_completo).all()
    return [{"id": s.id, "dni": s.dni, "nombre": s.nombre_completo, "correo": s.correo, "activo": s.esta_activo} for s in socios]

@app.put("/api/socios/{socio_id}/baja")
def dar_baja_socio(socio_id: str, db = Depends(get_db)):
    socio = db.query(Socio).filter(Socio.id == socio_id).first()
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    if not socio.esta_activo:
        raise HTTPException(status_code=400, detail="El socio ya está dado de baja")
    socio.esta_activo = False
    db.commit()
    return {"mensaje": "Socio dado de baja correctamente"}
