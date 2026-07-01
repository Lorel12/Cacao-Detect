"""
Configuration de test pour CacaoDetect Backend
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Client de test FastAPI"""
    return TestClient(app)


def test_health_check(client):
    """Tester l'endpoint de santé"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root(client):
    """Tester l'endpoint racine"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_docs_available(client):
    """Tester que la documentation est disponible"""
    response = client.get("/docs")
    assert response.status_code == 200


# Tests à développer
# - test_register
# - test_login
# - test_logout
# - test_diagnose
# - test_analyses_list
# - test_admin_stats
# etc.
