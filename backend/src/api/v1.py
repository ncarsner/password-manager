from typing import Any

from flask import Blueprint, jsonify, request

from ..config import Config
from ..models.vault import Vault
from ..services.crypto import CryptoService
from ..services.storage import StorageService

api_v1 = Blueprint("api_v1", __name__)
storage_service = StorageService()
crypto_service = CryptoService(key=Config.FERNET_KEY.encode())


@api_v1.route("/vaults", methods=["GET"])
def get_vaults() -> Any:
    """Retrieve all vaults."""
    vaults = storage_service.get_all_vaults()
    return jsonify(vaults), 200


@api_v1.route("/vaults", methods=["POST"])
def create_vault() -> Any:
    """Create a new vault."""
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Vault name is required"}), 400

    vault = Vault(name=data["name"])
    storage_service.save_vault(vault)
    return jsonify({"message": "Vault created successfully", "id": vault.id}), 201


@api_v1.route("/vaults/<int:vault_id>", methods=["GET"])
def get_vault(vault_id: int) -> Any:
    """Retrieve a specific vault by ID."""
    vault = storage_service.get_vault_by_id(vault_id)
    if vault is None:
        return jsonify({"error": "Vault not found"}), 404
    return jsonify(vault), 200


@api_v1.route("/vaults/<int:vault_id>", methods=["DELETE"])
def delete_vault(vault_id: int) -> Any:
    """Delete a vault."""
    success = storage_service.delete_vault(vault_id)
    if not success:
        return jsonify({"error": "Vault not found"}), 404
    return jsonify({"message": "Vault deleted successfully"}), 200


@api_v1.route("/vaults/<int:vault_id>/passwords", methods=["GET"])
def get_passwords(vault_id: int) -> Any:
    """Retrieve all credentials for a vault with passwords decrypted."""
    vault = storage_service.get_vault_by_id(vault_id)
    if not vault:
        return jsonify({"error": "Vault not found"}), 404

    entries = storage_service.get_passwords(vault_id)
    credentials = []
    for entry in entries:
        try:
            decrypted = crypto_service.decrypt(entry["password"])
            credentials.append(
                {
                    "id": entry["id"],
                    "domain": entry["domain"],
                    "username": entry["username"],
                    "password": decrypted,
                    "notes": entry["notes"],
                }
            )
        except Exception:
            credentials.append(
                {
                    "id": entry["id"],
                    "domain": entry["domain"],
                    "username": entry["username"],
                    "password": None,
                    "notes": entry["notes"],
                }
            )

    return jsonify(credentials), 200


@api_v1.route("/vaults/<int:vault_id>/passwords", methods=["POST"])
def add_password(vault_id: int) -> Any:
    """Add a new credential to a vault with the password encrypted."""
    vault = storage_service.get_vault_by_id(vault_id)
    if not vault:
        return jsonify({"error": "Vault not found"}), 404

    data = request.json
    if not data or "password" not in data:
        return jsonify({"error": "Password is required"}), 400

    raw_password: str = data["password"]
    if not (8 <= len(raw_password) <= 32):
        return jsonify({"error": "Password must be 8–32 characters"}), 400

    domain: str = data.get("domain", "")
    username: str = data.get("username", "")
    notes: str = data.get("notes", "")
    encrypted = crypto_service.encrypt(raw_password)
    password_id = storage_service.save_password(
        vault_id, domain, username, encrypted, notes
    )
    return jsonify({"message": "Credential added successfully", "id": password_id}), 201


@api_v1.route("/passwords/<int:password_id>", methods=["DELETE"])
def delete_password(password_id: int) -> Any:
    """Delete a specific password entry."""
    success = storage_service.delete_password(password_id)
    if not success:
        return jsonify({"error": "Password entry not found"}), 404
    return jsonify({"message": "Password deleted successfully"}), 200
