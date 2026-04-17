from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Crear ENUM usando SQL puro directo a PostgreSQL (Evita cualquier interferencia de SQLAlchemy)
    op.execute("CREATE TYPE tipoproductoenum AS ENUM ('FLOR', 'ACEITE', 'CREMA');")

    # Definir el tipo para usarlo en las columnas (create_type=False evita duplicados)
    tipo_enum = postgresql.ENUM(name='tipoproductoenum', create_type=False)

    # 2. Crear tabla usuarios_sistema
    op.create_table('usuarios_sistema',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('usuario', sa.String(50), nullable=False),
        sa.Column('hash_contrasena', sa.String(255), nullable=False)
    )
    op.create_index('ix_usuarios_sistema_usuario', 'usuarios_sistema', ['usuario'], unique=True)

    # 3. Crear tabla socios
    op.create_table('socios',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('dni', sa.String(20), nullable=False),
        sa.Column('nombre_completo', sa.String(150), nullable=False),
        sa.Column('correo', sa.String(150), nullable=False),
        sa.Column('fecha_alta', sa.Date(), nullable=False),
        sa.Column('esta_activo', sa.Boolean(), default=True)
    )
    op.create_index('ix_socios_dni', 'socios', ['dni'], unique=True)
    op.create_index('ix_socios_correo', 'socios', ['correo'], unique=True)

    # 4. Crear tabla configuracion_ong
    op.create_table('configuracion_ong',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nombre_ong', sa.String(150), nullable=False),
        sa.Column('matricula_igj', sa.String(100), nullable=False),
        sa.Column('valor_cuota_mensual', sa.Float(), nullable=False),
        sa.Column('valor_flor_por_gramo', sa.Float(), nullable=False),
        sa.Column('valor_aceite_por_ml', sa.Float(), nullable=False),
        sa.Column('valor_crema_por_ml', sa.Float(), nullable=False)
    )

    # 5. Crear tabla lotes
    op.create_table('lotes',
        sa.Column('id_lote', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('genetica', sa.String(100), nullable=False),
        sa.Column('fecha_siembra', sa.Date(), nullable=False),
        sa.Column('fecha_cosecha', sa.Date(), nullable=True),
        sa.Column('qr_base64_siembra', sa.Text(), nullable=False),
        sa.Column('qr_base64_cosecha', sa.Text(), nullable=True),
        sa.Column('esta_activo', sa.Boolean(), default=True)
    )

    # 6. Crear tabla inventario
    op.create_table('inventario',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('lote_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tipo_producto', tipo_enum, nullable=False),
        sa.Column('cantidad_inicial_ml_o_gramos', sa.Float(), nullable=False),
        sa.Column('cantidad_actual_ml_o_gramos', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['lote_id'], ['lotes.id_lote'], ondelete='CASCADE')
    )

    # 7. Crear tabla pagos_cuotas
    op.create_table('pagos_cuotas',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('socio_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('monto_abonado', sa.Float(), nullable=False),
        sa.Column('fecha_pago', sa.Date(), nullable=False),
        sa.Column('datos_recibo_json', postgresql.JSONB(), nullable=False),
        sa.ForeignKeyConstraint(['socio_id'], ['socios.id'], ondelete='CASCADE')
    )

    # 8. Crear tabla abastecimientos
    op.create_table('abastecimientos',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('socio_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('inventario_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tipo_producto', tipo_enum, nullable=False),
        sa.Column('cantidad_entregada', sa.Float(), nullable=False),
        sa.Column('monto_solidario', sa.Float(), nullable=False),
        sa.Column('fecha_abastecimiento', sa.Date(), nullable=False),
        sa.Column('datos_recibo_json', postgresql.JSONB(), nullable=False),
        sa.ForeignKeyConstraint(['socio_id'], ['socios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['inventario_id'], ['inventario.id'], ondelete='CASCADE')
    )

def downgrade() -> None:
    op.drop_table('abastecimientos')
    op.drop_table('pagos_cuotas')
    op.drop_table('inventario')
    op.drop_table('lotes')
    op.drop_table('configuracion_ong')
    op.drop_table('socios')
    op.drop_table('usuarios_sistema')
    op.execute("DROP TYPE tipoproductoenum;")
