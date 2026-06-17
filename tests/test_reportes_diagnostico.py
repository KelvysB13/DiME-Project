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


def test_read_reportes_diagnosticos_empty():
    response = client.get("/reportes_diagnosticos")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_create_reportes_diagnostico():
    response = client.post("/reportes_diagnosticos", json={
    "id_vendedor": 1,
    "fecha_generacion": "2024-01-15",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "resumen_ejecutivo": "test_resumen_ejecutivo",
    "plan_accion": "test_plan_accion"
})
    assert response.status_code == 201
    assert response.json()["reportes_diagnostico_id"] == 1


def test_read_reportes_diagnostico():
    client.post("/reportes_diagnosticos", json={
    "id_vendedor": 1,
    "fecha_generacion": "2024-01-15",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "resumen_ejecutivo": "test_resumen_ejecutivo",
    "plan_accion": "test_plan_accion"
})
    response = client.get("/reportes_diagnosticos/1")
    assert response.status_code == 200
    assert response.json()["reportes_diagnostico_id"] == 1


def test_update_reportes_diagnostico():
    client.post("/reportes_diagnosticos", json={
    "id_vendedor": 1,
    "fecha_generacion": "2024-01-15",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "resumen_ejecutivo": "test_resumen_ejecutivo",
    "plan_accion": "test_plan_accion"
})
    response = client.put("/reportes_diagnosticos/1", json={
    "id_vendedor": "updated",
    "fecha_generacion": "updated",
    "fecha_inicio_periodo": "updated",
    "fecha_fin_periodo": "updated",
    "plan_accion": "updated"
})
    assert response.status_code == 200


def test_delete_reportes_diagnostico():
    client.post("/reportes_diagnosticos", json={
    "id_vendedor": 1,
    "fecha_generacion": "2024-01-15",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "resumen_ejecutivo": "test_resumen_ejecutivo",
    "plan_accion": "test_plan_accion"
})
    response = client.delete("/reportes_diagnosticos/1")
    assert response.status_code == 204
    response = client.get("/reportes_diagnosticos/1")
    assert response.status_code == 404


def test_create_reportes_diagnostico_empty_body():
    response = client.post("/reportes_diagnosticos", json={})
    assert response.status_code == 422


def test_create_reportes_diagnostico_invalid_types():
    response = client.post("/reportes_diagnosticos", json={
    "id_vendedor": "not_a_number",
    "fecha_generacion": "2024-01-15",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "resumen_ejecutivo": "test_resumen_ejecutivo",
    "plan_accion": "test_plan_accion"
})
    assert response.status_code == 422


def test_search_reportes_diagnosticos():
    # Create a record first
    client.post("/reportes_diagnosticos", json={
    "id_vendedor": 1,
    "fecha_generacion": "2024-01-15",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "resumen_ejecutivo": "test_resumen_ejecutivo",
    "plan_accion": "test_plan_accion"
})
    response = client.get("/reportes_diagnosticos?search=tes")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


def test_sort_reportes_diagnosticos_asc_desc():
    client.post("/reportes_diagnosticos", json={
    "id_vendedor": 1,
    "fecha_generacion": "2024-01-15",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "resumen_ejecutivo": "test_resumen_ejecutivo",
    "plan_accion": "test_plan_accion"
})
    response_asc = client.get("/reportes_diagnosticos?sort_by=id_reporte&sort_desc=false")
    assert response_asc.status_code == 200
    response_desc = client.get("/reportes_diagnosticos?sort_by=id_reporte&sort_desc=true")
    assert response_desc.status_code == 200


def test_pagination_reportes_diagnosticos():
    # Create 2 records
    client.post("/reportes_diagnosticos", json={
    "id_vendedor": 1,
    "fecha_generacion": "2024-01-15",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "resumen_ejecutivo": "test_resumen_ejecutivo",
    "plan_accion": "test_plan_accion"
})
    client.post("/reportes_diagnosticos", json={
    "id_vendedor": 1,
    "fecha_generacion": "2024-01-15",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "resumen_ejecutivo": "test_resumen_ejecutivo",
    "plan_accion": "test_plan_accion"
})
    response = client.get("/reportes_diagnosticos?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2


def test_get_reportes_diagnostico_not_found():
    response = client.get("/reportes_diagnosticos/99999")
    assert response.status_code == 404


def test_delete_reportes_diagnostico_not_found():
    response = client.delete("/reportes_diagnosticos/99999")
    assert response.status_code == 404


def test_update_reportes_diagnostico_not_found():
    response = client.put("/reportes_diagnosticos/99999", json={
    "id_vendedor": "updated",
    "fecha_generacion": "updated",
    "fecha_inicio_periodo": "updated",
    "fecha_fin_periodo": "updated",
    "plan_accion": "updated"
})
    assert response.status_code == 404


def test_sort_reportes_diagnosticos_invalid_field():
    response = client.get("/reportes_diagnosticos?sort_by=invalid_field_xyz")
    assert response.status_code == 200


def test_create_reportes_diagnostico_extra_fields_rejected():
    response = client.post("/reportes_diagnosticos", json={
    "id_vendedor": 1,
    "fecha_generacion": "2024-01-15",
    "fecha_inicio_periodo": "2024-01-15",
    "fecha_fin_periodo": "2024-01-15",
    "resumen_ejecutivo": "test_resumen_ejecutivo",
    "plan_accion": "test_plan_accion",
    "_extra_field": "should_be_rejected"
})
    assert response.status_code == 422

