from fastapi.testclient import TestClient
from app.main import app
from app.routers.validate_password import DEFAULT_RULES

client = TestClient(app)


def test_get_rules():
    response = client.get("/api/v1/rules")

    assert response.status_code == 200
    data = response.json()

    assert data == DEFAULT_RULES


def test_validate_password():
    response = client.post("/api/v1/validate", json={"password": "Strong_Pass1"})
    assert response.status_code == 200
    assert response.json() == {"valid": True}


def test_validate_password_rules():
    response = client.post("/api/v1/validate/rules", json={"password": "weak_pass"})
    assert response.status_code == 200
    assert response.json() == {
        "rules": {
            "min_length": True,
            "require_uppercase": False,
            "require_lowercase": True,
            "require_digit": False,
            "require_underscore": True,
        },
    }
