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


def test_read_metricas_reputacions_empty():
    response = client.get("/metricas_reputacions")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_create_metricas_reputacion():
    response = client.post("/metricas_reputacions", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_totales_periodo": 1,
    "total_reclamos": 1,
    "total_mediaciones": 1,
    "total_canceladas": 1,
    "total_envios_incorrectos": 1,
    "nivel_reputacion": "test_nivel_reputacion",
    "insignia": "test_insignia"
})
    assert response.status_code == 201
    assert response.json()["metricas_reputacion_id"] == 1


def test_read_metricas_reputacion():
    client.post("/metricas_reputacions", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_totales_periodo": 1,
    "total_reclamos": 1,
    "total_mediaciones": 1,
    "total_canceladas": 1,
    "total_envios_incorrectos": 1,
    "nivel_reputacion": "test_nivel_reputacion",
    "insignia": "test_insignia"
})
    response = client.get("/metricas_reputacions/1")
    assert response.status_code == 200
    assert response.json()["metricas_reputacion_id"] == 1


def test_update_metricas_reputacion():
    client.post("/metricas_reputacions", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_totales_periodo": 1,
    "total_reclamos": 1,
    "total_mediaciones": 1,
    "total_canceladas": 1,
    "total_envios_incorrectos": 1,
    "nivel_reputacion": "test_nivel_reputacion",
    "insignia": "test_insignia"
})
    response = client.put("/metricas_reputacions/1", json={
    "id_vendedor": "updated",
    "fecha_captura": "updated",
    "ventas_totales_periodo": "updated",
    "total_reclamos": "updated",
    "total_mediaciones": "updated",
    "total_canceladas": "updated",
    "total_envios_incorrectos": "updated",
    "nivel_reputacion": "updated"
})
    assert response.status_code == 200


def test_delete_metricas_reputacion():
    client.post("/metricas_reputacions", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_totales_periodo": 1,
    "total_reclamos": 1,
    "total_mediaciones": 1,
    "total_canceladas": 1,
    "total_envios_incorrectos": 1,
    "nivel_reputacion": "test_nivel_reputacion",
    "insignia": "test_insignia"
})
    response = client.delete("/metricas_reputacions/1")
    assert response.status_code == 204
    response = client.get("/metricas_reputacions/1")
    assert response.status_code == 404


def test_create_metricas_reputacion_empty_body():
    response = client.post("/metricas_reputacions", json={})
    assert response.status_code == 422


def test_create_metricas_reputacion_invalid_types():
    response = client.post("/metricas_reputacions", json={
    "id_vendedor": "not_a_number",
    "fecha_captura": "test_fecha_captura",
    "ventas_totales_periodo": 1,
    "total_reclamos": 1,
    "total_mediaciones": 1,
    "total_canceladas": 1,
    "total_envios_incorrectos": 1,
    "nivel_reputacion": "test_nivel_reputacion",
    "insignia": "test_insignia"
})
    assert response.status_code == 422


def test_search_metricas_reputacions():
    # Create a record first
    client.post("/metricas_reputacions", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_totales_periodo": 1,
    "total_reclamos": 1,
    "total_mediaciones": 1,
    "total_canceladas": 1,
    "total_envios_incorrectos": 1,
    "nivel_reputacion": "test_nivel_reputacion",
    "insignia": "test_insignia"
})
    response = client.get("/metricas_reputacions?search=tes")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


def test_sort_metricas_reputacions_asc_desc():
    client.post("/metricas_reputacions", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_totales_periodo": 1,
    "total_reclamos": 1,
    "total_mediaciones": 1,
    "total_canceladas": 1,
    "total_envios_incorrectos": 1,
    "nivel_reputacion": "test_nivel_reputacion",
    "insignia": "test_insignia"
})
    response_asc = client.get("/metricas_reputacions?sort_by=id_metricas_reputacion&sort_desc=false")
    assert response_asc.status_code == 200
    response_desc = client.get("/metricas_reputacions?sort_by=id_metricas_reputacion&sort_desc=true")
    assert response_desc.status_code == 200


def test_pagination_metricas_reputacions():
    # Create 2 records
    client.post("/metricas_reputacions", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_totales_periodo": 1,
    "total_reclamos": 1,
    "total_mediaciones": 1,
    "total_canceladas": 1,
    "total_envios_incorrectos": 1,
    "nivel_reputacion": "test_nivel_reputacion",
    "insignia": "test_insignia"
})
    client.post("/metricas_reputacions", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_totales_periodo": 1,
    "total_reclamos": 1,
    "total_mediaciones": 1,
    "total_canceladas": 1,
    "total_envios_incorrectos": 1,
    "nivel_reputacion": "test_nivel_reputacion",
    "insignia": "test_insignia"
})
    response = client.get("/metricas_reputacions?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2


def test_get_metricas_reputacion_not_found():
    response = client.get("/metricas_reputacions/99999")
    assert response.status_code == 404


def test_delete_metricas_reputacion_not_found():
    response = client.delete("/metricas_reputacions/99999")
    assert response.status_code == 404


def test_update_metricas_reputacion_not_found():
    response = client.put("/metricas_reputacions/99999", json={
    "id_vendedor": "updated",
    "fecha_captura": "updated",
    "ventas_totales_periodo": "updated",
    "total_reclamos": "updated",
    "total_mediaciones": "updated",
    "total_canceladas": "updated",
    "total_envios_incorrectos": "updated",
    "nivel_reputacion": "updated"
})
    assert response.status_code == 404


def test_sort_metricas_reputacions_invalid_field():
    response = client.get("/metricas_reputacions?sort_by=invalid_field_xyz")
    assert response.status_code == 200


def test_create_metricas_reputacion_extra_fields_rejected():
    response = client.post("/metricas_reputacions", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_totales_periodo": 1,
    "total_reclamos": 1,
    "total_mediaciones": 1,
    "total_canceladas": 1,
    "total_envios_incorrectos": 1,
    "nivel_reputacion": "test_nivel_reputacion",
    "insignia": "test_insignia",
    "_extra_field": "should_be_rejected"
})
    assert response.status_code == 422

