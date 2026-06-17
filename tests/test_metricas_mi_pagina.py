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


def test_read_metricas_mi_paginas_empty():
    response = client.get("/metricas_mi_paginas")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_create_metricas_mi_pagina():
    response = client.post("/metricas_mi_paginas", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "tiene_banner": true,
    "tiene_logo": true,
    "tiene_carruseles": true,
    "categorias_organizadas": true
})
    assert response.status_code == 201
    assert response.json()["metricas_mi_pagina_id"] == 1


def test_read_metricas_mi_pagina():
    client.post("/metricas_mi_paginas", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "tiene_banner": true,
    "tiene_logo": true,
    "tiene_carruseles": true,
    "categorias_organizadas": true
})
    response = client.get("/metricas_mi_paginas/1")
    assert response.status_code == 200
    assert response.json()["metricas_mi_pagina_id"] == 1


def test_update_metricas_mi_pagina():
    client.post("/metricas_mi_paginas", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "tiene_banner": true,
    "tiene_logo": true,
    "tiene_carruseles": true,
    "categorias_organizadas": true
})
    response = client.put("/metricas_mi_paginas/1", json={
    "id_vendedor": "updated",
    "fecha_captura": "updated",
    "tiene_banner": "updated",
    "tiene_logo": "updated",
    "tiene_carruseles": "updated",
    "categorias_organizadas": "updated"
})
    assert response.status_code == 200


def test_delete_metricas_mi_pagina():
    client.post("/metricas_mi_paginas", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "tiene_banner": true,
    "tiene_logo": true,
    "tiene_carruseles": true,
    "categorias_organizadas": true
})
    response = client.delete("/metricas_mi_paginas/1")
    assert response.status_code == 204
    response = client.get("/metricas_mi_paginas/1")
    assert response.status_code == 404


def test_create_metricas_mi_pagina_empty_body():
    response = client.post("/metricas_mi_paginas", json={})
    assert response.status_code == 422


def test_create_metricas_mi_pagina_invalid_types():
    response = client.post("/metricas_mi_paginas", json={
    "id_vendedor": "not_a_number",
    "fecha_captura": "test_fecha_captura",
    "tiene_banner": true,
    "tiene_logo": true,
    "tiene_carruseles": true,
    "categorias_organizadas": true
})
    assert response.status_code == 422


def test_sort_metricas_mi_paginas_asc_desc():
    client.post("/metricas_mi_paginas", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "tiene_banner": true,
    "tiene_logo": true,
    "tiene_carruseles": true,
    "categorias_organizadas": true
})
    response_asc = client.get("/metricas_mi_paginas?sort_by=id_metricas_pagina&sort_desc=false")
    assert response_asc.status_code == 200
    response_desc = client.get("/metricas_mi_paginas?sort_by=id_metricas_pagina&sort_desc=true")
    assert response_desc.status_code == 200


def test_pagination_metricas_mi_paginas():
    # Create 2 records
    client.post("/metricas_mi_paginas", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "tiene_banner": true,
    "tiene_logo": true,
    "tiene_carruseles": true,
    "categorias_organizadas": true
})
    client.post("/metricas_mi_paginas", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "tiene_banner": true,
    "tiene_logo": true,
    "tiene_carruseles": true,
    "categorias_organizadas": true
})
    response = client.get("/metricas_mi_paginas?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2


def test_get_metricas_mi_pagina_not_found():
    response = client.get("/metricas_mi_paginas/99999")
    assert response.status_code == 404


def test_delete_metricas_mi_pagina_not_found():
    response = client.delete("/metricas_mi_paginas/99999")
    assert response.status_code == 404


def test_update_metricas_mi_pagina_not_found():
    response = client.put("/metricas_mi_paginas/99999", json={
    "id_vendedor": "updated",
    "fecha_captura": "updated",
    "tiene_banner": "updated",
    "tiene_logo": "updated",
    "tiene_carruseles": "updated",
    "categorias_organizadas": "updated"
})
    assert response.status_code == 404


def test_sort_metricas_mi_paginas_invalid_field():
    response = client.get("/metricas_mi_paginas?sort_by=invalid_field_xyz")
    assert response.status_code == 200


def test_create_metricas_mi_pagina_extra_fields_rejected():
    response = client.post("/metricas_mi_paginas", json={
    "id_vendedor": 1,
    "fecha_captura": "test_fecha_captura",
    "tiene_banner": true,
    "tiene_logo": true,
    "tiene_carruseles": true,
    "categorias_organizadas": true,
    "_extra_field": "should_be_rejected"
})
    assert response.status_code == 422

