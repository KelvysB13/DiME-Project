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


def test_read_monedas_empty():
    response = client.get("/monedas")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_create_moneda():
    response = client.post("/monedas", json={
    "codigo_moneda": "USD",
    "nombre_moneda": "Dollar",
    "simbolo": "$"
})
    assert response.status_code == 201
    assert response.json()["codigo_moneda"] == "USD"


def test_read_moneda():
    client.post("/monedas", json={
    "codigo_moneda": "USD",
    "nombre_moneda": "Dollar",
    "simbolo": "$"
})
    response = client.get("/monedas/USD")
    assert response.status_code == 200
    assert response.json()["codigo_moneda"] == "USD"


def test_update_moneda():
    client.post("/monedas", json={
    "codigo_moneda": "USD",
    "nombre_moneda": "Dollar",
    "simbolo": "$"
})
    response = client.put("/monedas/USD", json={
    "nombre_moneda": "updated"
})
    assert response.status_code == 200


def test_delete_moneda():
    client.post("/monedas", json={
    "codigo_moneda": "USD",
    "nombre_moneda": "Dollar",
    "simbolo": "$"
})
    response = client.delete("/monedas/USD")
    assert response.status_code == 204
    response = client.get("/monedas/USD")
    assert response.status_code == 404


def test_create_moneda_empty_body():
    response = client.post("/monedas", json={})
    assert response.status_code == 422


def test_search_monedas():
    # Create a record first
    client.post("/monedas", json={
    "codigo_moneda": "USD",
    "nombre_moneda": "Dollar",
    "simbolo": "$"
})
    response = client.get("/monedas?search=USD")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


def test_sort_monedas_asc_desc():
    client.post("/monedas", json={
    "codigo_moneda": "USD",
    "nombre_moneda": "Dollar",
    "simbolo": "$"
})
    response_asc = client.get("/monedas?sort_by=codigo_moneda&sort_desc=false")
    assert response_asc.status_code == 200
    response_desc = client.get("/monedas?sort_by=codigo_moneda&sort_desc=true")
    assert response_desc.status_code == 200


def test_pagination_monedas():
    # Create 2 records
    client.post("/monedas", json={
    "codigo_moneda": "USD",
    "nombre_moneda": "Dollar",
    "simbolo": "$"
})
    client.post("/monedas", json={
    "codigo_moneda": "EUR",
    "nombre_moneda": "Euro",
    "simbolo": "\u20ac"
})
    response = client.get("/monedas?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2


def test_get_moneda_not_found():
    response = client.get("/monedas/XXX")
    assert response.status_code == 404


def test_delete_moneda_not_found():
    response = client.delete("/monedas/XXX")
    assert response.status_code == 404


def test_update_moneda_not_found():
    response = client.put("/monedas/XXX", json={
    "nombre_moneda": "updated"
})
    assert response.status_code == 404


def test_sort_monedas_invalid_field():
    response = client.get("/monedas?sort_by=invalid_field_xyz")
    assert response.status_code == 200


def test_create_moneda_extra_fields_rejected():
    response = client.post("/monedas", json={
    "codigo_moneda": "USD",
    "nombre_moneda": "Dollar",
    "simbolo": "$",
    "_extra_field": "should_be_rejected"
})
    assert response.status_code == 422
