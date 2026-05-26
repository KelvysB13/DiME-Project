import pytest
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


@pytest.fixture
def clientes_df():
    return pd.read_csv(os.path.join(DATA_DIR, "clientes_mock.csv"))


def test_clientes_csv_existe():
    assert os.path.exists(os.path.join(DATA_DIR, "clientes_mock.csv"))


def test_clientes_tienen_columnas_esperadas(clientes_df):
    expected = {"nombre_organizacion", "email", "plan", "db_name"}
    assert expected.issubset(set(clientes_df.columns))
