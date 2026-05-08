import pytest
from backend.src.models.vault import Vault
from backend.src.services.crypto import CryptoService
from backend.src.services.storage import StorageService
from backend.src.config import Config
from backend.src.utils.helpers import validate_password, format_vault_name, sanitize_input

def test_config():
    conf = Config.to_dict()
    assert "SECRET_KEY" in conf
    assert "DATABASE_PATH" in conf
    assert conf["DATABASE_PATH"] == "database.db"

def test_vault_model():
    vault = Vault(name="My Vault", vault_id=1)
    assert vault.name == "My Vault"
    assert vault.id == 1
    vault.add_password("pass1")
    assert "pass1" in vault.get_passwords()
    vault.remove_password("pass1")
    assert "pass1" not in vault.get_passwords()
    assert "Vault(id=1, name=My Vault, passwords=[])" in repr(vault)

def test_crypto_service():
    # Test generation
    cs1 = CryptoService()
    text = "hello"
    encrypted = cs1.encrypt(text)
    assert cs1.decrypt(encrypted) == text
    
    # Test with existing key
    cs2 = CryptoService(key=cs1.key)
    assert cs2.decrypt(encrypted) == text

def test_helpers():
    assert validate_password("Pass1234") is True
    assert validate_password("short") is False
    assert validate_password("NoDigits") is False
    assert validate_password("12345678") is False
    
    assert format_vault_name("  my vault  ") == "My Vault"
    assert format_vault_name("") == "Untitled Vault"
    assert format_vault_name(None) == "Untitled Vault"
    
    assert sanitize_input("  test  ") == "test"
    assert sanitize_input(None) == ""
