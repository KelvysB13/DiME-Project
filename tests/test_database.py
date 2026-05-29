import pytest
from sqlalchemy import text
from app.core.database import SessionLocal, get_client_session

@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture
def db_cliente():
    session = get_client_session("dime_cliente_1")
    yield session
    session.close()

# --- Prueba la conexión maestra con PostgreSQL ---
class TestConexionMaestra:

    def test_ejecuta_select_1(self, db):
        resultado = db.execute(text("SELECT 1")).scalar()
        assert resultado == 1

    def test_tabla_clientes_existe(self, db):
        existe = db.execute(
            text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'clientes')")
        ).scalar()
        assert existe is True

    def test_tabla_servicios_existe(self, db):
        existe = db.execute(
            text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'servicios_ofrecidos')")
        ).scalar()
        assert existe is True

    def test_clientes_tiene_datos(self, db):
        cantidad = db.execute(text("SELECT COUNT(*) FROM clientes")).scalar()
        assert cantidad > 0

# --- Prueba la conexión de cliente con PostgreSQL ---
class TestConexionCliente:

    def test_ejecuta_select_1(self, db_cliente):
        resultado = db_cliente.execute(text("SELECT 1")).scalar()
        assert resultado == 1

    @pytest.mark.parametrize("tabla", [
        "metricas_publicaciones",
        "metricas_reputacion",
        "metricas_costos",
        "metricas_envios",
        "metricas_stock",
    ])

    def test_tablas_existen(self, db_cliente, tabla):
        existe = db_cliente.execute(
            text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = :t)"),
            {"t": tabla}
        ).scalar()
        assert existe is True, f"Tabla '{tabla}' no existe"
