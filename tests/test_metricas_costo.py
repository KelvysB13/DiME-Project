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


def test_read_metricas_costos_empty():
    response = client.get("/metricas_costos")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_create_metricas_costo():
    response = client.post("/metricas_costos", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_cobradas_total": 1.0,
    "neto_recibido": 1.0,
    "cargos_por_venta": 1.0,
    "costos_envio": 1.0,
    "inversion_ads": 1.0,
    "otros_cargos": 1.0,
    "cargos_envio_full": 1.0,
    "descuento_reputacion": 1.0
})
    assert response.status_code == 201
    assert response.json()["metricas_costo_id"] == 1


def test_read_metricas_costo():
    client.post("/metricas_costos", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_cobradas_total": 1.0,
    "neto_recibido": 1.0,
    "cargos_por_venta": 1.0,
    "costos_envio": 1.0,
    "inversion_ads": 1.0,
    "otros_cargos": 1.0,
    "cargos_envio_full": 1.0,
    "descuento_reputacion": 1.0
})
    response = client.get("/metricas_costos/1")
    assert response.status_code == 200
    assert response.json()["metricas_costo_id"] == 1


def test_update_metricas_costo():
    client.post("/metricas_costos", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_cobradas_total": 1.0,
    "neto_recibido": 1.0,
    "cargos_por_venta": 1.0,
    "costos_envio": 1.0,
    "inversion_ads": 1.0,
    "otros_cargos": 1.0,
    "cargos_envio_full": 1.0,
    "descuento_reputacion": 1.0
})
    response = client.put("/metricas_costos/1", json={
    "id_vendedor": "updated",
    "fecha_captura": "updated",
    "ventas_cobradas_total": "updated",
    "neto_recibido": "updated",
    "cargos_por_venta": "updated",
    "costos_envio": "updated",
    "inversion_ads": "updated",
    "otros_cargos": "updated",
    "cargos_envio_full": "updated",
    "descuento_reputacion": "updated"
})
    assert response.status_code == 200


def test_delete_metricas_costo():
    client.post("/metricas_costos", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_cobradas_total": 1.0,
    "neto_recibido": 1.0,
    "cargos_por_venta": 1.0,
    "costos_envio": 1.0,
    "inversion_ads": 1.0,
    "otros_cargos": 1.0,
    "cargos_envio_full": 1.0,
    "descuento_reputacion": 1.0
})
    response = client.delete("/metricas_costos/1")
    assert response.status_code == 204
    response = client.get("/metricas_costos/1")
    assert response.status_code == 404


def test_create_metricas_costo_empty_body():
    response = client.post("/metricas_costos", json={})
    assert response.status_code == 422


def test_create_metricas_costo_invalid_types():
    response = client.post("/metricas_costos", json={
    "id_vendedor": "not_a_number",
    "fecha_captura": "test_fecha_captura",
    "ventas_cobradas_total": 1.0,
    "neto_recibido": 1.0,
    "cargos_por_venta": 1.0,
    "costos_envio": 1.0,
    "inversion_ads": 1.0,
    "otros_cargos": 1.0,
    "cargos_envio_full": 1.0,
    "descuento_reputacion": 1.0
})
    assert response.status_code == 422


def test_sort_metricas_costos_asc_desc():
    client.post("/metricas_costos", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_cobradas_total": 1.0,
    "neto_recibido": 1.0,
    "cargos_por_venta": 1.0,
    "costos_envio": 1.0,
    "inversion_ads": 1.0,
    "otros_cargos": 1.0,
    "cargos_envio_full": 1.0,
    "descuento_reputacion": 1.0
})
    response_asc = client.get("/metricas_costos?sort_by=id_metricas_costo&sort_desc=false")
    assert response_asc.status_code == 200
    response_desc = client.get("/metricas_costos?sort_by=id_metricas_costo&sort_desc=true")
    assert response_desc.status_code == 200


def test_pagination_metricas_costos():
    # Create 2 records
    client.post("/metricas_costos", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_cobradas_total": 1.0,
    "neto_recibido": 1.0,
    "cargos_por_venta": 1.0,
    "costos_envio": 1.0,
    "inversion_ads": 1.0,
    "otros_cargos": 1.0,
    "cargos_envio_full": 1.0,
    "descuento_reputacion": 1.0
})
    client.post("/metricas_costos", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_cobradas_total": 1.0,
    "neto_recibido": 1.0,
    "cargos_por_venta": 1.0,
    "costos_envio": 1.0,
    "inversion_ads": 1.0,
    "otros_cargos": 1.0,
    "cargos_envio_full": 1.0,
    "descuento_reputacion": 1.0
})
    response = client.get("/metricas_costos?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2


def test_get_metricas_costo_not_found():
    response = client.get("/metricas_costos/99999")
    assert response.status_code == 404


def test_delete_metricas_costo_not_found():
    response = client.delete("/metricas_costos/99999")
    assert response.status_code == 404


def test_update_metricas_costo_not_found():
    response = client.put("/metricas_costos/99999", json={
    "id_vendedor": "updated",
    "fecha_captura": "updated",
    "ventas_cobradas_total": "updated",
    "neto_recibido": "updated",
    "cargos_por_venta": "updated",
    "costos_envio": "updated",
    "inversion_ads": "updated",
    "otros_cargos": "updated",
    "cargos_envio_full": "updated",
    "descuento_reputacion": "updated"
})
    assert response.status_code == 404


def test_sort_metricas_costos_invalid_field():
    response = client.get("/metricas_costos?sort_by=invalid_field_xyz")
    assert response.status_code == 200


def test_create_metricas_costo_extra_fields_rejected():
    response = client.post("/metricas_costos", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "ventas_cobradas_total": 1.0,
    "neto_recibido": 1.0,
    "cargos_por_venta": 1.0,
    "costos_envio": 1.0,
    "inversion_ads": 1.0,
    "otros_cargos": 1.0,
    "cargos_envio_full": 1.0,
    "descuento_reputacion": 1.0,
    "_extra_field": "should_be_rejected"
})
    assert response.status_code == 422

