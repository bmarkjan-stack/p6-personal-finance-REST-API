import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app()

    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret"
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_token(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    return response.get_json()["access_token"]


def test_create_transaction(client, auth_token):
    response = client.post(
        "/api/transactions",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "description": "Groceries",
            "amount": 1500,
            "category": "Food",
            "type": "expense"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["transaction"]["description"] == "Groceries"
    assert data["transaction"]["amount"] == 1500
    assert data["transaction"]["category"] == "Food"
    assert data["transaction"]["type"] == "expense"


def test_get_transactions(client, auth_token):
    client.post(
        "/api/transactions",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "description": "Salary",
            "amount": 30000,
            "category": "Work",
            "type": "income"
        }
    )

    response = client.get(
        "/api/transactions",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["count"] == 1
    assert data["transactions"][0]["description"] == "Salary"


def test_invalid_transaction(client, auth_token):
    response = client.post(
        "/api/transactions",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "description": "",
            "amount": -100,
            "category": "Food",
            "type": "invalid"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Validation failed."
    assert "description" in data["details"]
    assert "amount" in data["details"]
    assert "type" in data["details"]


def test_delete_transaction(client, auth_token):
    create_response = client.post(
        "/api/transactions",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "description": "Coffee",
            "amount": 150,
            "category": "Food",
            "type": "expense"
        }
    )

    transaction_id = (
        create_response
        .get_json()["transaction"]["id"]
    )

    response = client.delete(
        f"/api/transactions/{transaction_id}",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 200