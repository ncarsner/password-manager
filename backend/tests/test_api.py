import os
import pytest
from flask.testing import FlaskClient
from backend.src.app import app, init_db


@pytest.fixture
def client() -> FlaskClient:
    """Fixture to provide a test client with a clean temporary database."""
    db_path = "test_database.db"
    # Ensure a fresh start
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Re-initialize for test
    init_db(db_path)
    
    # Configure app for testing
    app.config["TESTING"] = True
    
    # We need to ensure StorageService uses the test db
    # Since it's instantiated at module level in v1.py, we might need to monkeypatch it
    from backend.src.api.v1 import storage_service
    storage_service.db_path = db_path
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


def test_home(client: FlaskClient) -> None:
    """Test the home endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() == "Welcome to the Password Manager API!"


def test_create_and_get_vault(client: FlaskClient) -> None:
    """Test creating a vault and then retrieving it."""
    # Create
    resp = client.post("/api/v1/vaults", json={"name": "Test Vault"})
    assert resp.status_code == 201
    vault_id = resp.json["id"]
    
    # List
    resp = client.get("/api/v1/vaults")
    assert resp.status_code == 200
    assert any(v["name"] == "Test Vault" for v in resp.json)
    
    # Get by ID
    resp = client.get(f"/api/v1/vaults/{vault_id}")
    assert resp.status_code == 200
    assert resp.json["name"] == "Test Vault"


def test_vault_not_found(client: FlaskClient) -> None:
    """Test retrieving a non-existent vault."""
    resp = client.get("/api/v1/vaults/999")
    assert resp.status_code == 404


def test_password_management(client: FlaskClient) -> None:
    """Test adding, retrieving, and deleting passwords."""
    # Setup vault
    resp = client.post("/api/v1/vaults", json={"name": "Secure Vault"})
    vault_id = resp.json["id"]
    
    # Add password
    resp = client.post(f"/api/v1/vaults/{vault_id}/passwords", json={"password": "secret123"})
    assert resp.status_code == 201
    password_id = resp.json["id"]
    
    # Get passwords
    resp = client.get(f"/api/v1/vaults/{vault_id}/passwords")
    assert resp.status_code == 200
    assert any(p["password"] == "secret123" for p in resp.json)
    
    # Delete password
    resp = client.delete(f"/api/v1/passwords/{password_id}")
    assert resp.status_code == 200
    
    # Verify deleted
    resp = client.get(f"/api/v1/vaults/{vault_id}/passwords")
    assert not any(p["id"] == password_id for p in resp.json)


def test_delete_vault(client: FlaskClient) -> None:
    """Test deleting a vault."""
    resp = client.post("/api/v1/vaults", json={"name": "Delete Me"})
    vault_id = resp.json["id"]

    resp = client.delete(f"/api/v1/vaults/{vault_id}")
    assert resp.status_code == 200

    resp = client.get(f"/api/v1/vaults/{vault_id}")
    assert resp.status_code == 404


def test_create_vault_error(client: FlaskClient) -> None:
    """Test creating a vault with missing name."""
    resp = client.post("/api/v1/vaults", json={})
    assert resp.status_code == 400
    assert "error" in resp.json


def test_delete_non_existent_vault(client: FlaskClient) -> None:
    """Test deleting a vault that doesn't exist."""
    resp = client.delete("/api/v1/vaults/999")
    assert resp.status_code == 404


def test_add_password_vault_not_found(client: FlaskClient) -> None:
    """Test adding a password to a non-existent vault."""
    resp = client.post("/api/v1/vaults/999/passwords", json={"password": "foo"})
    assert resp.status_code == 404


def test_add_password_missing_data(client: FlaskClient) -> None:
    """Test adding a password with missing data."""
    resp = client.post("/api/v1/vaults", json={"name": "P-Vault"})
    vault_id = resp.json["id"]
    resp = client.post(f"/api/v1/vaults/{vault_id}/passwords", json={})
    assert resp.status_code == 400


def test_get_passwords_vault_not_found(client: FlaskClient) -> None:
    """Test getting passwords for a non-existent vault."""
    resp = client.get("/api/v1/vaults/999/passwords")
    assert resp.status_code == 404


def test_delete_password_not_found(client: FlaskClient) -> None:
    """Test deleting a non-existent password entry."""
    resp = client.delete("/api/v1/passwords/999")
    assert resp.status_code == 404


def test_create_duplicate_vault(client: FlaskClient) -> None:
    """Test creating a vault with a name that already exists."""
    client.post("/api/v1/vaults", json={"name": "Duplicate"})
    resp = client.post("/api/v1/vaults", json={"name": "Duplicate"})
    assert resp.status_code == 201
    assert "id" in resp.json


def test_decryption_failure(client: FlaskClient) -> None:
    """Test handling of decryption failure."""
    # Create vault and password
    resp = client.post("/api/v1/vaults", json={"name": "Bad Crypto"})
    vault_id = resp.json["id"]
    client.post(f"/api/v1/vaults/{vault_id}/passwords", json={"password": "secret"})

    # Monkeypatch crypto service with a new key to cause failure
    from backend.src.api.v1 import crypto_service
    from cryptography.fernet import Fernet
    original_cipher = crypto_service.cipher
    crypto_service.cipher = Fernet(Fernet.generate_key())

    try:
        resp = client.get(f"/api/v1/vaults/{vault_id}/passwords")
        assert resp.status_code == 200
        assert any("ERROR" in p["password"] for p in resp.json)
    finally:
        # Restore
        crypto_service.cipher = original_cipher
