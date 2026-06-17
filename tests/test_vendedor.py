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


def test_read_vendedors_empty():
    response = client.get("/vendedors")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_create_vendedor():
    response = client.post("/vendedors", json={
    "user_name": "Test Vendedor",
    "nombre_tienda": "Test Vendedor",
    "codigo_pais": "AR",
    "moneda_local": "ARS",
    "tipo_plan": 1,
    "email": "test@email.com",
    "access_token": "test_access_token",
    "refresh_token": "test_refresh_token",
    "tiempo_token": "test_tiempo_token",
    "esta_activo": true,
    "fecha_creacion": "test_fecha_creacion"
})
    assert response.status_code == 201
    assert response.json()["vendedor_id"] == 1


def test_read_vendedor():
    client.post("/vendedors", json={
    "user_name": "Test Vendedor",
    "nombre_tienda": "Test Vendedor",
    "codigo_pais": "AR",
    "moneda_local": "ARS",
    "tipo_plan": 1,
    "email": "test@email.com",
    "access_token": "test_access_token",
    "refresh_token": "test_refresh_token",
    "tiempo_token": "test_tiempo_token",
    "esta_activo": true,
    "fecha_creacion": "test_fecha_creacion"
})
    response = client.get("/vendedors/1")
    assert response.status_code == 200
    assert response.json()["vendedor_id"] == 1


def test_update_vendedor():
    client.post("/vendedors", json={
    "user_name": "Test Vendedor",
    "nombre_tienda": "Test Vendedor",
    "codigo_pais": "AR",
    "moneda_local": "ARS",
    "tipo_plan": 1,
    "email": "test@email.com",
    "access_token": "test_access_token",
    "refresh_token": "test_refresh_token",
    "tiempo_token": "test_tiempo_token",
    "esta_activo": true,
    "fecha_creacion": "test_fecha_creacion"
})
    response = client.put("/vendedors/1", json={
    "user_name": "updated",
    "nombre_tienda": "updated",
    "codigo_pais": "updated",
    "moneda_local": "updated",
    "email": "updated",
    "esta_activo": "updated",
    "fecha_creacion": "updated"
})
    assert response.status_code == 200


def test_delete_vendedor():
    client.post("/vendedors", json={
    "user_name": "Test Vendedor",
    "nombre_tienda": "Test Vendedor",
    "codigo_pais": "AR",
    "moneda_local": "ARS",
    "tipo_plan": 1,
    "email": "test@email.com",
    "access_token": "test_access_token",
    "refresh_token": "test_refresh_token",
    "tiempo_token": "test_tiempo_token",
    "esta_activo": true,
    "fecha_creacion": "test_fecha_creacion"
})
    response = client.delete("/vendedors/1")
    assert response.status_code == 204
    response = client.get("/vendedors/1")
    assert response.status_code == 404


def test_create_vendedor_empty_body():
    response = client.post("/vendedors", json={})
    assert response.status_code == 422


def test_create_vendedor_invalid_types():
    response = client.post("/vendedors", json={
    "user_name": "Test Vendedor",
    "nombre_tienda": "Test Vendedor",
    "codigo_pais": "AR",
    "moneda_local": "ARS",
    "tipo_plan": "not_a_number",
    "email": "test@email.com",
    "access_token": "test_access_token",
    "refresh_token": "test_refresh_token",
    "tiempo_token": "test_tiempo_token",
    "esta_activo": true,
    "fecha_creacion": "test_fecha_creacion"
})
    assert response.status_code == 422


def test_search_vendedors():
    # Create a record first
    client.post("/vendedors", json={
    "user_name": "Test Vendedor",
    "nombre_tienda": "Test Vendedor",
    "codigo_pais": "AR",
    "moneda_local": "ARS",
    "tipo_plan": 1,
    "email": "test@email.com",
    "access_token": "test_access_token",
    "refresh_token": "test_refresh_token",
    "tiempo_token": "test_tiempo_token",
    "esta_activo": true,
    "fecha_creacion": "test_fecha_creacion"
})
    response = client.get("/vendedors?search=Tes")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


def test_sort_vendedors_asc_desc():
    client.post("/vendedors", json={
    "user_name": "Test Vendedor",
    "nombre_tienda": "Test Vendedor",
    "codigo_pais": "AR",
    "moneda_local": "ARS",
    "tipo_plan": 1,
    "email": "test@email.com",
    "access_token": "test_access_token",
    "refresh_token": "test_refresh_token",
    "tiempo_token": "test_tiempo_token",
    "esta_activo": true,
    "fecha_creacion": "test_fecha_creacion"
})
    response_asc = client.get("/vendedors?sort_by=id_vendedor&sort_desc=false")
    assert response_asc.status_code == 200
    response_desc = client.get("/vendedors?sort_by=id_vendedor&sort_desc=true")
    assert response_desc.status_code == 200


def test_pagination_vendedors():
    # Create 2 records
    client.post("/vendedors", json={
    "user_name": "Test Vendedor",
    "nombre_tienda": "Test Vendedor",
    "codigo_pais": "AR",
    "moneda_local": "ARS",
    "tipo_plan": 1,
    "email": "test@email.com",
    "access_token": "test_access_token",
    "refresh_token": "test_refresh_token",
    "tiempo_token": "test_tiempo_token",
    "esta_activo": true,
    "fecha_creacion": "test_fecha_creacion"
})
    client.post("/vendedors", json={
    "user_name": "Test Vendedor",
    "nombre_tienda": "Test Vendedor",
    "codigo_pais": "AR",
    "moneda_local": "ARS",
    "tipo_plan": 1,
    "email": "test@email.com",
    "access_token": "test_access_token",
    "refresh_token": "test_refresh_token",
    "tiempo_token": "test_tiempo_token",
    "esta_activo": true,
    "fecha_creacion": "test_fecha_creacion"
})
    response = client.get("/vendedors?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2


def test_get_vendedor_not_found():
    response = client.get("/vendedors/99999")
    assert response.status_code == 404


def test_delete_vendedor_not_found():
    response = client.delete("/vendedors/99999")
    assert response.status_code == 404


def test_update_vendedor_not_found():
    response = client.put("/vendedors/99999", json={
    "user_name": "updated",
    "nombre_tienda": "updated",
    "codigo_pais": "updated",
    "moneda_local": "updated",
    "email": "updated",
    "esta_activo": "updated",
    "fecha_creacion": "updated"
})
    assert response.status_code == 404


def test_sort_vendedors_invalid_field():
    response = client.get("/vendedors?sort_by=invalid_field_xyz")
    assert response.status_code == 200


def test_create_vendedor_extra_fields_rejected():
    response = client.post("/vendedors", json={
    "user_name": "Test Vendedor",
    "nombre_tienda": "Test Vendedor",
    "codigo_pais": "AR",
    "moneda_local": "ARS",
    "tipo_plan": 1,
    "email": "test@email.com",
    "access_token": "test_access_token",
    "refresh_token": "test_refresh_token",
    "tiempo_token": "test_tiempo_token",
    "esta_activo": true,
    "fecha_creacion": "test_fecha_creacion",
    "_extra_field": "should_be_rejected"
})
    assert response.status_code == 422

