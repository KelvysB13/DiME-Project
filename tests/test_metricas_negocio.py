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


def test_read_metricas_negocios_empty():
    response = client.get("/metricas_negocios")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_create_metricas_negocio():
    response = client.post("/metricas_negocios", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "ventas_brutas_moneda_local": 1.0,
    "ventas_brutas_usd": 1.0,
    "unidades_vendidas": 1,
    "visitas_totales": 1,
    "intencion_compra": 1,
    "ventas_concretadas": 1,
    "precio_promedio_unidad": 1.0,
    "precio_promedio_venta": 1.0
})
    assert response.status_code == 201
    assert response.json()["metricas_negocio_id"] == 1


def test_read_metricas_negocio():
    client.post("/metricas_negocios", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "ventas_brutas_moneda_local": 1.0,
    "ventas_brutas_usd": 1.0,
    "unidades_vendidas": 1,
    "visitas_totales": 1,
    "intencion_compra": 1,
    "ventas_concretadas": 1,
    "precio_promedio_unidad": 1.0,
    "precio_promedio_venta": 1.0
})
    response = client.get("/metricas_negocios/1")
    assert response.status_code == 200
    assert response.json()["metricas_negocio_id"] == 1


def test_update_metricas_negocio():
    client.post("/metricas_negocios", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "ventas_brutas_moneda_local": 1.0,
    "ventas_brutas_usd": 1.0,
    "unidades_vendidas": 1,
    "visitas_totales": 1,
    "intencion_compra": 1,
    "ventas_concretadas": 1,
    "precio_promedio_unidad": 1.0,
    "precio_promedio_venta": 1.0
})
    response = client.put("/metricas_negocios/1", json={
    "id_vendedor": "updated",
    "fecha_captura": "updated",
    "fecha_inicio_periodo": "updated",
    "fecha_fin_periodo": "updated",
    "ventas_brutas_moneda_local": "updated",
    "ventas_brutas_usd": "updated",
    "unidades_vendidas": "updated",
    "visitas_totales": "updated",
    "intencion_compra": "updated",
    "ventas_concretadas": "updated",
    "precio_promedio_unidad": "updated",
    "precio_promedio_venta": "updated"
})
    assert response.status_code == 200


def test_delete_metricas_negocio():
    client.post("/metricas_negocios", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "ventas_brutas_moneda_local": 1.0,
    "ventas_brutas_usd": 1.0,
    "unidades_vendidas": 1,
    "visitas_totales": 1,
    "intencion_compra": 1,
    "ventas_concretadas": 1,
    "precio_promedio_unidad": 1.0,
    "precio_promedio_venta": 1.0
})
    response = client.delete("/metricas_negocios/1")
    assert response.status_code == 204
    response = client.get("/metricas_negocios/1")
    assert response.status_code == 404


def test_create_metricas_negocio_empty_body():
    response = client.post("/metricas_negocios", json={})
    assert response.status_code == 422


def test_create_metricas_negocio_invalid_types():
    response = client.post("/metricas_negocios", json={
    "id_vendedor": "not_a_number",
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "ventas_brutas_moneda_local": 1.0,
    "ventas_brutas_usd": 1.0,
    "unidades_vendidas": 1,
    "visitas_totales": 1,
    "intencion_compra": 1,
    "ventas_concretadas": 1,
    "precio_promedio_unidad": 1.0,
    "precio_promedio_venta": 1.0
})
    assert response.status_code == 422


def test_sort_metricas_negocios_asc_desc():
    client.post("/metricas_negocios", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "ventas_brutas_moneda_local": 1.0,
    "ventas_brutas_usd": 1.0,
    "unidades_vendidas": 1,
    "visitas_totales": 1,
    "intencion_compra": 1,
    "ventas_concretadas": 1,
    "precio_promedio_unidad": 1.0,
    "precio_promedio_venta": 1.0
})
    response_asc = client.get("/metricas_negocios?sort_by=id_metricas_negocio&sort_desc=false")
    assert response_asc.status_code == 200
    response_desc = client.get("/metricas_negocios?sort_by=id_metricas_negocio&sort_desc=true")
    assert response_desc.status_code == 200


def test_pagination_metricas_negocios():
    # Create 2 records
    client.post("/metricas_negocios", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "ventas_brutas_moneda_local": 1.0,
    "ventas_brutas_usd": 1.0,
    "unidades_vendidas": 1,
    "visitas_totales": 1,
    "intencion_compra": 1,
    "ventas_concretadas": 1,
    "precio_promedio_unidad": 1.0,
    "precio_promedio_venta": 1.0
})
    client.post("/metricas_negocios", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "ventas_brutas_moneda_local": 1.0,
    "ventas_brutas_usd": 1.0,
    "unidades_vendidas": 1,
    "visitas_totales": 1,
    "intencion_compra": 1,
    "ventas_concretadas": 1,
    "precio_promedio_unidad": 1.0,
    "precio_promedio_venta": 1.0
})
    response = client.get("/metricas_negocios?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2


def test_get_metricas_negocio_not_found():
    response = client.get("/metricas_negocios/99999")
    assert response.status_code == 404


def test_delete_metricas_negocio_not_found():
    response = client.delete("/metricas_negocios/99999")
    assert response.status_code == 404


def test_update_metricas_negocio_not_found():
    response = client.put("/metricas_negocios/99999", json={
    "id_vendedor": "updated",
    "fecha_captura": "updated",
    "fecha_inicio_periodo": "updated",
    "fecha_fin_periodo": "updated",
    "ventas_brutas_moneda_local": "updated",
    "ventas_brutas_usd": "updated",
    "unidades_vendidas": "updated",
    "visitas_totales": "updated",
    "intencion_compra": "updated",
    "ventas_concretadas": "updated",
    "precio_promedio_unidad": "updated",
    "precio_promedio_venta": "updated"
})
    assert response.status_code == 404


def test_sort_metricas_negocios_invalid_field():
    response = client.get("/metricas_negocios?sort_by=invalid_field_xyz")
    assert response.status_code == 200


def test_create_metricas_negocio_extra_fields_rejected():
    response = client.post("/metricas_negocios", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "ventas_brutas_moneda_local": 1.0,
    "ventas_brutas_usd": 1.0,
    "unidades_vendidas": 1,
    "visitas_totales": 1,
    "intencion_compra": 1,
    "ventas_concretadas": 1,
    "precio_promedio_unidad": 1.0,
    "precio_promedio_venta": 1.0,
    "_extra_field": "should_be_rejected"
})
    assert response.status_code == 422

