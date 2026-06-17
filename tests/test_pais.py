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


def test_read_pais_empty():
    response = client.get("/pais")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_create_pais():
    response = client.post("/pais", json={
    "codigo_pais": "AR",
    "nombre_pais": "Argentina"
})
    assert response.status_code == 201
    assert response.json()["codigo_pais"] == "AR"


def test_read_pais():
    client.post("/pais", json={
    "codigo_pais": "AR",
    "nombre_pais": "Argentina"
})
    response = client.get("/pais/AR")
    assert response.status_code == 200
    assert response.json()["codigo_pais"] == "AR"


def test_update_pais():
    client.post("/pais", json={
    "codigo_pais": "AR",
    "nombre_pais": "Argentina"
})
    response = client.put("/pais/AR", json={
    "nombre_pais": "updated"
})
    assert response.status_code == 200


def test_delete_pais():
    client.post("/pais", json={
    "codigo_pais": "AR",
    "nombre_pais": "Argentina"
})
    response = client.delete("/pais/AR")
    assert response.status_code == 204
    response = client.get("/pais/AR")
    assert response.status_code == 404


def test_create_pais_empty_body():
    response = client.post("/pais", json={})
    assert response.status_code == 422


def test_search_pais():
    # Create a record first
    client.post("/pais", json={
    "codigo_pais": "AR",
    "nombre_pais": "Argentina"
})
    response = client.get("/pais?search=AR")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


def test_sort_pais_asc_desc():
    client.post("/pais", json={
    "codigo_pais": "AR",
    "nombre_pais": "Argentina"
})
    response_asc = client.get("/pais?sort_by=codigo_pais&sort_desc=false")
    assert response_asc.status_code == 200
    response_desc = client.get("/pais?sort_by=codigo_pais&sort_desc=true")
    assert response_desc.status_code == 200


def test_pagination_pais():
    # Create 2 records
    client.post("/pais", json={
    "codigo_pais": "AR",
    "nombre_pais": "Argentina"
})
    client.post("/pais", json={
    "codigo_pais": "BR",
    "nombre_pais": "Brasil"
})
    response = client.get("/pais?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2


def test_get_pais_not_found():
    response = client.get("/pais/XX")
    assert response.status_code == 404


def test_delete_pais_not_found():
    response = client.delete("/pais/XX")
    assert response.status_code == 404


def test_update_pais_not_found():
    response = client.put("/pais/XX", json={
    "nombre_pais": "updated"
})
    assert response.status_code == 404


def test_sort_pais_invalid_field():
    response = client.get("/pais?sort_by=invalid_field_xyz")
    assert response.status_code == 200


def test_create_pais_extra_fields_rejected():
    response = client.post("/pais", json={
    "codigo_pais": "AR",
    "nombre_pais": "Argentina",
    "_extra_field": "should_be_rejected"
})
    assert response.status_code == 422
