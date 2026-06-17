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


def test_read_plan_saas_empty():
    response = client.get("/plan_saas")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_create_plan_saas():
    response = client.post("/plan_saas", json={
    "nombre_plan": "Test Plan saas",
    "descripcion": "Descripción de prueba para descripcion"
})
    assert response.status_code == 201
    assert response.json()["plan_saas_id"] == 1


def test_read_plan_saas():
    client.post("/plan_saas", json={
    "nombre_plan": "Test Plan saas",
    "descripcion": "Descripción de prueba para descripcion"
})
    response = client.get("/plan_saas/1")
    assert response.status_code == 200
    assert response.json()["plan_saas_id"] == 1


def test_update_plan_saas():
    client.post("/plan_saas", json={
    "nombre_plan": "Test Plan saas",
    "descripcion": "Descripción de prueba para descripcion"
})
    response = client.put("/plan_saas/1", json={
    "nombre_plan": "updated"
})
    assert response.status_code == 200


def test_delete_plan_saas():
    client.post("/plan_saas", json={
    "nombre_plan": "Test Plan saas",
    "descripcion": "Descripción de prueba para descripcion"
})
    response = client.delete("/plan_saas/1")
    assert response.status_code == 204
    response = client.get("/plan_saas/1")
    assert response.status_code == 404


def test_create_plan_saas_empty_body():
    response = client.post("/plan_saas", json={})
    assert response.status_code == 422


def test_search_plan_saas():
    # Create a record first
    client.post("/plan_saas", json={
    "nombre_plan": "Test Plan saas",
    "descripcion": "Descripción de prueba para descripcion"
})
    response = client.get("/plan_saas?search=Tes")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


def test_sort_plan_saas_asc_desc():
    client.post("/plan_saas", json={
    "nombre_plan": "Test Plan saas",
    "descripcion": "Descripción de prueba para descripcion"
})
    response_asc = client.get("/plan_saas?sort_by=id_plan&sort_desc=false")
    assert response_asc.status_code == 200
    response_desc = client.get("/plan_saas?sort_by=id_plan&sort_desc=true")
    assert response_desc.status_code == 200


def test_pagination_plan_saas():
    # Create 2 records
    client.post("/plan_saas", json={
    "nombre_plan": "Test Plan saas",
    "descripcion": "Descripción de prueba para descripcion"
})
    client.post("/plan_saas", json={
    "nombre_plan": "Test Plan saas",
    "descripcion": "Descripción de prueba para descripcion"
})
    response = client.get("/plan_saas?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2


def test_get_plan_saas_not_found():
    response = client.get("/plan_saas/99999")
    assert response.status_code == 404


def test_delete_plan_saas_not_found():
    response = client.delete("/plan_saas/99999")
    assert response.status_code == 404


def test_update_plan_saas_not_found():
    response = client.put("/plan_saas/99999", json={
    "nombre_plan": "updated"
})
    assert response.status_code == 404


def test_sort_plan_saas_invalid_field():
    response = client.get("/plan_saas?sort_by=invalid_field_xyz")
    assert response.status_code == 200


def test_create_plan_saas_extra_fields_rejected():
    response = client.post("/plan_saas", json={
    "nombre_plan": "Test Plan saas",
    "descripcion": "Descripción de prueba para descripcion",
    "_extra_field": "should_be_rejected"
})
    assert response.status_code == 422

