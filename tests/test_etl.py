import os
import pytest
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
CLIENTES_CSV = os.path.join(DATA_DIR, "clientes_mock.csv")
COLUMNAS_ESPERADAS = {"nombre_organizacion", "email", "plan", "db_name"}

@pytest.fixture
def clientes_df():
    return pd.read_csv(CLIENTES_CSV)

# --- Prueba la existencia del archivo de clientes ---
class TestArchivoClientes:

    def test_archivo_existe(self):
        assert os.path.exists(CLIENTES_CSV)

    def test_tiene_columnas_correctas(self, clientes_df):
        assert COLUMNAS_ESPERADAS.issubset(set(clientes_df.columns))

    def test_tiene_registros(self, clientes_df):
        assert len(clientes_df) > 0

    def test_columnas_criticas_sin_nulos(self, clientes_df):
        nulos = clientes_df[["nombre_organizacion", "email", "db_name"]].isnull().sum().sum()
        assert nulos == 0