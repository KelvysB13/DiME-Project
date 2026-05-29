import pytest
from app.database import get_maestra_connection


@pytest.fixture
def conn():
    c = get_maestra_connection()
    yield c
    c.close()


def test_conexion_maestra(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        assert cur.fetchone()[0] == 1


def test_tabla_clientes_existe(conn):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'clientes')"
        )
        assert cur.fetchone()[0]
