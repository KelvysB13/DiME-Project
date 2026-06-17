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


def test_read_publicacions_empty():
    response = client.get("/publicacions")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_create_publicacion():
    response = client.post("/publicacions", json={
    "id_vendedor": 1,
    "ml_item_id": "test_ml_item_id",
    "titulo": "test_titulo",
    "tipo_publicacion": "test_tipo_publicacion",
    "estado_publicacion": "test_estado_publicacion"
})
    assert response.status_code == 201
    assert response.json()["publicacion_id"] == 1


def test_read_publicacion():
    client.post("/publicacions", json={
    "id_vendedor": 1,
    "ml_item_id": "test_ml_item_id",
    "titulo": "test_titulo",
    "tipo_publicacion": "test_tipo_publicacion",
    "estado_publicacion": "test_estado_publicacion"
})
    response = client.get("/publicacions/1")
    assert response.status_code == 200
    assert response.json()["publicacion_id"] == 1


def test_update_publicacion():
    client.post("/publicacions", json={
    "id_vendedor": 1,
    "ml_item_id": "test_ml_item_id",
    "titulo": "test_titulo",
    "tipo_publicacion": "test_tipo_publicacion",
    "estado_publicacion": "test_estado_publicacion"
})
    response = client.put("/publicacions/1", json={
    "id_vendedor": "updated",
    "ml_item_id": "updated",
    "titulo": "updated",
    "tipo_publicacion": "updated",
    "estado_publicacion": "updated"
})
    assert response.status_code == 200


def test_delete_publicacion():
    client.post("/publicacions", json={
    "id_vendedor": 1,
    "ml_item_id": "test_ml_item_id",
    "titulo": "test_titulo",
    "tipo_publicacion": "test_tipo_publicacion",
    "estado_publicacion": "test_estado_publicacion"
})
    response = client.delete("/publicacions/1")
    assert response.status_code == 204
    response = client.get("/publicacions/1")
    assert response.status_code == 404


def test_create_publicacion_empty_body():
    response = client.post("/publicacions", json={})
    assert response.status_code == 422


def test_create_publicacion_invalid_types():
    response = client.post("/publicacions", json={
    "id_vendedor": "not_a_number",
    "ml_item_id": "test_ml_item_id",
    "titulo": "test_titulo",
    "tipo_publicacion": "test_tipo_publicacion",
    "estado_publicacion": "test_estado_publicacion"
})
    assert response.status_code == 422


def test_search_publicacions():
    # Create a record first
    client.post("/publicacions", json={
    "id_vendedor": 1,
    "ml_item_id": "test_ml_item_id",
    "titulo": "test_titulo",
    "tipo_publicacion": "test_tipo_publicacion",
    "estado_publicacion": "test_estado_publicacion"
})
    response = client.get("/publicacions?search=tes")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


def test_sort_publicacions_asc_desc():
    client.post("/publicacions", json={
    "id_vendedor": 1,
    "ml_item_id": "test_ml_item_id",
    "titulo": "test_titulo",
    "tipo_publicacion": "test_tipo_publicacion",
    "estado_publicacion": "test_estado_publicacion"
})
    response_asc = client.get("/publicacions?sort_by=id_publicacion&sort_desc=false")
    assert response_asc.status_code == 200
    response_desc = client.get("/publicacions?sort_by=id_publicacion&sort_desc=true")
    assert response_desc.status_code == 200


def test_pagination_publicacions():
    # Create 2 records
    client.post("/publicacions", json={
    "id_vendedor": 1,
    "ml_item_id": "test_ml_item_id",
    "titulo": "test_titulo",
    "tipo_publicacion": "test_tipo_publicacion",
    "estado_publicacion": "test_estado_publicacion"
})
    client.post("/publicacions", json={
    "id_vendedor": 1,
    "ml_item_id": "test_ml_item_id",
    "titulo": "test_titulo",
    "tipo_publicacion": "test_tipo_publicacion",
    "estado_publicacion": "test_estado_publicacion"
})
    response = client.get("/publicacions?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2


def test_get_publicacion_not_found():
    response = client.get("/publicacions/99999")
    assert response.status_code == 404


def test_delete_publicacion_not_found():
    response = client.delete("/publicacions/99999")
    assert response.status_code == 404


def test_update_publicacion_not_found():
    response = client.put("/publicacions/99999", json={
    "id_vendedor": "updated",
    "ml_item_id": "updated",
    "titulo": "updated",
    "tipo_publicacion": "updated",
    "estado_publicacion": "updated"
})
    assert response.status_code == 404


def test_sort_publicacions_invalid_field():
    response = client.get("/publicacions?sort_by=invalid_field_xyz")
    assert response.status_code == 200


def test_create_publicacion_extra_fields_rejected():
    response = client.post("/publicacions", json={
    "id_vendedor": 1,
    "ml_item_id": "test_ml_item_id",
    "titulo": "test_titulo",
    "tipo_publicacion": "test_tipo_publicacion",
    "estado_publicacion": "test_estado_publicacion",
    "_extra_field": "should_be_rejected"
})
    assert response.status_code == 422

