import pytest

from fastapi.testclient import TestClient

from main import app

@pytest.fixture

def client():

    return TestClient(app)

# --- Prueba la salud de la API ---

class TestHealth:

    def test_retorna_status_ok(self, client):

        response = client.get("/health")

        assert response.status_code == 200

        assert response.json()["status"] == "ok"

    def test_retorna_version_correcta(self, client):

        response = client.get("/health")

        assert response.json()["version"] == "1.0.0"

    def test_retorna_json(self, client):

        response = client.get("/health")

        assert response.headers["content-type"] == "application/json"

# --- Prueba la autenticación con Mercado Libre ---

class TestAuth:

    def test_login_retorna_auth_url(self, client):

        response = client.get("/auth/ml/login")

        assert response.status_code == 200

        assert "auth_url" in response.json()

    def test_callback_acepta_codigo(self, client):

        response = client.get("/auth/ml/callback?code=test123")

        assert response.status_code == 200

# --- Prueba las rutas de la API ---

class TestRutas:

    def test_ruta_inexistente_retorna_404(self, client):

        response = client.get("/ruta-inexistente")

        assert response.status_code == 404
