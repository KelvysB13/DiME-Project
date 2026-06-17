import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db import Base, get_db
from main import app

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_metricas_stock_fulls_empty():
    response = client.get("/metricas_stock_fulls")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_create_metricas_stock_full():
    response = client.post("/metricas_stock_fulls", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "espacios_p_asignados": 1,
    "espacios_g_asignados": 1,
    "puntaje_calidad": 1,
    "productos_no_aptos_venta": 1,
    "productos_sin_rotacion": 1,
    "productos_antiguedad": 1,
    "productos_exceso_proyeccion": 1
})
    assert response.status_code == 201
    assert response.json()["metricas_stock_full_id"] == 1


def test_read_metricas_stock_full():
    client.post("/metricas_stock_fulls", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "espacios_p_asignados": 1,
    "espacios_g_asignados": 1,
    "puntaje_calidad": 1,
    "productos_no_aptos_venta": 1,
    "productos_sin_rotacion": 1,
    "productos_antiguedad": 1,
    "productos_exceso_proyeccion": 1
})
    response = client.get("/metricas_stock_fulls/1")
    assert response.status_code == 200
    assert response.json()["metricas_stock_full_id"] == 1


def test_update_metricas_stock_full():
    client.post("/metricas_stock_fulls", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "espacios_p_asignados": 1,
    "espacios_g_asignados": 1,
    "puntaje_calidad": 1,
    "productos_no_aptos_venta": 1,
    "productos_sin_rotacion": 1,
    "productos_antiguedad": 1,
    "productos_exceso_proyeccion": 1
})
    response = client.put("/metricas_stock_fulls/1", json={
    "id_vendedor": "updated",
    "fecha_captura": "updated",
    "espacios_p_asignados": "updated",
    "espacios_g_asignados": "updated",
    "puntaje_calidad": "updated",
    "productos_no_aptos_venta": "updated",
    "productos_sin_rotacion": "updated",
    "productos_antiguedad": "updated",
    "productos_exceso_proyeccion": "updated"
})
    assert response.status_code == 200


def test_delete_metricas_stock_full():
    client.post("/metricas_stock_fulls", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "espacios_p_asignados": 1,
    "espacios_g_asignados": 1,
    "puntaje_calidad": 1,
    "productos_no_aptos_venta": 1,
    "productos_sin_rotacion": 1,
    "productos_antiguedad": 1,
    "productos_exceso_proyeccion": 1
})
    response = client.delete("/metricas_stock_fulls/1")
    assert response.status_code == 204
    response = client.get("/metricas_stock_fulls/1")
    assert response.status_code == 404


def test_create_metricas_stock_full_empty_body():
    response = client.post("/metricas_stock_fulls", json={})
    assert response.status_code == 422


def test_create_metricas_stock_full_invalid_types():
    response = client.post("/metricas_stock_fulls", json={
    "id_vendedor": "not_a_number",
    "fecha_captura": "test_fecha_captura",
    "espacios_p_asignados": 1,
    "espacios_g_asignados": 1,
    "puntaje_calidad": 1,
    "productos_no_aptos_venta": 1,
    "productos_sin_rotacion": 1,
    "productos_antiguedad": 1,
    "productos_exceso_proyeccion": 1
})
    assert response.status_code == 422


def test_sort_metricas_stock_fulls_asc_desc():
    client.post("/metricas_stock_fulls", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "espacios_p_asignados": 1,
    "espacios_g_asignados": 1,
    "puntaje_calidad": 1,
    "productos_no_aptos_venta": 1,
    "productos_sin_rotacion": 1,
    "productos_antiguedad": 1,
    "productos_exceso_proyeccion": 1
})
    response_asc = client.get("/metricas_stock_fulls?sort_by=id_metricas_stock&sort_desc=false")
    assert response_asc.status_code == 200
    response_desc = client.get("/metricas_stock_fulls?sort_by=id_metricas_stock&sort_desc=true")
    assert response_desc.status_code == 200


def test_pagination_metricas_stock_fulls():
    # Create 2 records
    client.post("/metricas_stock_fulls", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "espacios_p_asignados": 1,
    "espacios_g_asignados": 1,
    "puntaje_calidad": 1,
    "productos_no_aptos_venta": 1,
    "productos_sin_rotacion": 1,
    "productos_antiguedad": 1,
    "productos_exceso_proyeccion": 1
})
    client.post("/metricas_stock_fulls", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "espacios_p_asignados": 1,
    "espacios_g_asignados": 1,
    "puntaje_calidad": 1,
    "productos_no_aptos_venta": 1,
    "productos_sin_rotacion": 1,
    "productos_antiguedad": 1,
    "productos_exceso_proyeccion": 1
})
    response = client.get("/metricas_stock_fulls?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2


def test_get_metricas_stock_full_not_found():
    response = client.get("/metricas_stock_fulls/99999")
    assert response.status_code == 404


def test_delete_metricas_stock_full_not_found():
    response = client.delete("/metricas_stock_fulls/99999")
    assert response.status_code == 404


def test_update_metricas_stock_full_not_found():
    response = client.put("/metricas_stock_fulls/99999", json={
    "id_vendedor": "updated",
    "fecha_captura": "updated",
    "espacios_p_asignados": "updated",
    "espacios_g_asignados": "updated",
    "puntaje_calidad": "updated",
    "productos_no_aptos_venta": "updated",
    "productos_sin_rotacion": "updated",
    "productos_antiguedad": "updated",
    "productos_exceso_proyeccion": "updated"
})
    assert response.status_code == 404


def test_sort_metricas_stock_fulls_invalid_field():
    response = client.get("/metricas_stock_fulls?sort_by=invalid_field_xyz")
    assert response.status_code == 200


def test_create_metricas_stock_full_extra_fields_rejected():
    response = client.post("/metricas_stock_fulls", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "espacios_p_asignados": 1,
    "espacios_g_asignados": 1,
    "puntaje_calidad": 1,
    "productos_no_aptos_venta": 1,
    "productos_sin_rotacion": 1,
    "productos_antiguedad": 1,
    "productos_exceso_proyeccion": 1,
    "_extra_field": "should_be_rejected"
})
    assert response.status_code == 422

