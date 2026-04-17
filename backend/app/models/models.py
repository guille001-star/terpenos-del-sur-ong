import uuid
from sqlalchemy import Column, String, Boolean, Float, Date, Enum, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base
import enum

class TipoProductoEnum(str, enum.Enum):
    FLOR = "FLOR"
    ACEITE = "ACEITE"
    CREMA = "CREMA"

class UsuarioSistema(Base):
    __tablename__ = "usuarios_sistema"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario = Column(String(50), unique=True, index=True, nullable=False)
    hash_contrasena = Column(String(255), nullable=False)

class Socio(Base):
    __tablename__ = "socios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dni = Column(String(20), unique=True, index=True, nullable=False)
    nombre_completo = Column(String(150), nullable=False)
    correo = Column(String(150), unique=True, index=True, nullable=False)
    fecha_alta = Column(Date, nullable=False)
    esta_activo = Column(Boolean, default=True)

class ConfiguracionOng(Base):
    __tablename__ = "configuracion_ong"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_ong = Column(String(150), nullable=False)
    matricula_igj = Column(String(100), nullable=False)
    valor_cuota_mensual = Column(Float, nullable=False)
    valor_flor_por_gramo = Column(Float, nullable=False)
    valor_aceite_por_ml = Column(Float, nullable=False)
    valor_crema_por_ml = Column(Float, nullable=False)

class Lote(Base):
    __tablename__ = "lotes"
    id_lote = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    genetica = Column(String(100), nullable=False)
    fecha_siembra = Column(Date, nullable=False)
    fecha_cosecha = Column(Date, nullable=True)
    qr_base64_siembra = Column(Text, nullable=False)
    qr_base64_cosecha = Column(Text, nullable=True)
    esta_activo = Column(Boolean, default=True)

class Inventario(Base):
    __tablename__ = "inventario"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lote_id = Column(UUID(as_uuid=True), ForeignKey("lotes.id_lote"), nullable=False)
    tipo_producto = Column(Enum(TipoProductoEnum), nullable=False)
    cantidad_inicial_ml_o_gramos = Column(Float, nullable=False)
    cantidad_actual_ml_o_gramos = Column(Float, nullable=False)

class PagoCuota(Base):
    __tablename__ = "pagos_cuotas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    socio_id = Column(UUID(as_uuid=True), ForeignKey("socios.id"), nullable=False)
    monto_abonado = Column(Float, nullable=False)
    fecha_pago = Column(Date, nullable=False)
    datos_recibo_json = Column(JSONB, nullable=False)

class Abastecimiento(Base):
    __tablename__ = "abastecimientos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    socio_id = Column(UUID(as_uuid=True), ForeignKey("socios.id"), nullable=False)
    inventario_id = Column(UUID(as_uuid=True), ForeignKey("inventario.id"), nullable=False)
    tipo_producto = Column(Enum(TipoProductoEnum), nullable=False)
    cantidad_entregada = Column(Float, nullable=False)
    monto_solidario = Column(Float, nullable=False)
    fecha_abastecimiento = Column(Date, nullable=False)
    datos_recibo_json = Column(JSONB, nullable=False)
