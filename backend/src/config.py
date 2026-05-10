import os
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

load_dotenv()


def _load_or_create_fernet_key() -> str:
    """Load Fernet key from environment or generate and persist a new one.

    On first run, writes the generated key to .env so it survives restarts.
    Subsequent runs load the key from the env var FERNET_KEY.
    """
    key = os.environ.get("FERNET_KEY")
    if key:
        return key
    new_key = Fernet.generate_key().decode()
    env_path = Path(".env")
    if not env_path.exists():
        env_path.write_text("")
    set_key(str(env_path), "FERNET_KEY", new_key)
    os.environ["FERNET_KEY"] = new_key
    return new_key


class Config:
    """Application configuration."""

    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "a_default_secret_key"
    DATABASE_PATH: str = os.environ.get("DATABASE_PATH") or "database.db"
    DEBUG: bool = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")
    TESTING: bool = os.environ.get("TESTING", "False").lower() in ("true", "1", "t")
    FERNET_KEY: str = _load_or_create_fernet_key()

    @classmethod
    def to_dict(cls) -> dict[str, Any]:
        """Return config as a dictionary."""
        return {
            "SECRET_KEY": cls.SECRET_KEY,
            "DATABASE_PATH": cls.DATABASE_PATH,
            "DEBUG": cls.DEBUG,
            "TESTING": cls.TESTING,
        }
