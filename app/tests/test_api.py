from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_rules():
    password = "Strong_Pass1"
    response = client.post("/api/v1/validate/rules", json={"password": password})

    assert response.status_code == 200
    data = response.json()

    assert "password" in data
    assert "rules" in data
    assert data["password"] == password

    rules = data["rules"]
    assert rules["min_length"] is True
    assert rules["require_uppercase"] is True
    assert rules["require_lowercase"] is True
    assert rules["require_digit"] is True
    assert rules["require_underscore"] is True


def test_validate_password():
    response = client.post("/api/v1/validate", json={"password": "Strong_Pass1"})
    assert response.status_code == 200
    assert response.json() == {"password": "Strong_Pass1", "valid": True}


def test_validate_password_rules():
    response = client.post("/api/v1/validate/rules", json={"password": "weakpass"})
    assert response.status_code == 200
    assert response.json() == {
        "password": "weakpass",
        "rules": {
            "min_length": True,
            "require_uppercase": False,
            "require_lowercase": True,
            "require_digit": False,
            "require_underscore": False,
        },
    }
