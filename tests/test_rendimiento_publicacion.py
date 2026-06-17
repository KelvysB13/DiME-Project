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


def test_read_rendimiento_publicacions_empty():
    response = client.get("/rendimiento_publicacions")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_create_rendimiento_publicacion():
    response = client.post("/rendimiento_publicacions", json={
    "id_publicacion": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "visitas": 1,
    "ventas": 1
})
    assert response.status_code == 201
    assert response.json()["rendimiento_publicacion_id"] == 1


def test_read_rendimiento_publicacion():
    client.post("/rendimiento_publicacions", json={
    "id_publicacion": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "visitas": 1,
    "ventas": 1
})
    response = client.get("/rendimiento_publicacions/1")
    assert response.status_code == 200
    assert response.json()["rendimiento_publicacion_id"] == 1


def test_update_rendimiento_publicacion():
    client.post("/rendimiento_publicacions", json={
    "id_publicacion": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "visitas": 1,
    "ventas": 1
})
    response = client.put("/rendimiento_publicacions/1", json={
    "id_publicacion": "updated",
    "fecha_captura": "updated",
    "fecha_inicio_periodo": "updated",
    "fecha_fin_periodo": "updated",
    "visitas": "updated",
    "ventas": "updated"
})
    assert response.status_code == 200


def test_delete_rendimiento_publicacion():
    client.post("/rendimiento_publicacions", json={
    "id_publicacion": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "visitas": 1,
    "ventas": 1
})
    response = client.delete("/rendimiento_publicacions/1")
    assert response.status_code == 204
    response = client.get("/rendimiento_publicacions/1")
    assert response.status_code == 404


def test_create_rendimiento_publicacion_empty_body():
    response = client.post("/rendimiento_publicacions", json={})
    assert response.status_code == 422


def test_create_rendimiento_publicacion_invalid_types():
    response = client.post("/rendimiento_publicacions", json={
    "id_publicacion": "not_a_number",
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "visitas": 1,
    "ventas": 1
})
    assert response.status_code == 422


def test_sort_rendimiento_publicacions_asc_desc():
    client.post("/rendimiento_publicacions", json={
    "id_publicacion": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "visitas": 1,
    "ventas": 1
})
    response_asc = client.get("/rendimiento_publicacions?sort_by=id_rendimiento_publi&sort_desc=false")
    assert response_asc.status_code == 200
    response_desc = client.get("/rendimiento_publicacions?sort_by=id_rendimiento_publi&sort_desc=true")
    assert response_desc.status_code == 200


def test_pagination_rendimiento_publicacions():
    # Create 2 records
    client.post("/rendimiento_publicacions", json={
    "id_publicacion": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "visitas": 1,
    "ventas": 1
})
    client.post("/rendimiento_publicacions", json={
    "id_publicacion": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "visitas": 1,
    "ventas": 1
})
    response = client.get("/rendimiento_publicacions?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2


def test_get_rendimiento_publicacion_not_found():
    response = client.get("/rendimiento_publicacions/99999")
    assert response.status_code == 404


def test_delete_rendimiento_publicacion_not_found():
    response = client.delete("/rendimiento_publicacions/99999")
    assert response.status_code == 404


def test_update_rendimiento_publicacion_not_found():
    response = client.put("/rendimiento_publicacions/99999", json={
    "id_publicacion": "updated",
    "fecha_captura": "updated",
    "fecha_inicio_periodo": "updated",
    "fecha_fin_periodo": "updated",
    "visitas": "updated",
    "ventas": "updated"
})
    assert response.status_code == 404


def test_sort_rendimiento_publicacions_invalid_field():
    response = client.get("/rendimiento_publicacions?sort_by=invalid_field_xyz")
    assert response.status_code == 200


def test_create_rendimiento_publicacion_extra_fields_rejected():
    response = client.post("/rendimiento_publicacions", json={
    "id_publicacion": 1,
    "fecha_captura": "test_fecha_captura",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "visitas": 1,
    "ventas": 1,
    "_extra_field": "should_be_rejected"
})
    assert response.status_code == 422

