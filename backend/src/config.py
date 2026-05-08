import os
from typing import Any


class Config:
    """Application configuration."""

    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "a_default_secret_key"
    DATABASE_PATH: str = os.environ.get("DATABASE_PATH") or "database.db"
    DEBUG: bool = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")
    TESTING: bool = os.environ.get("TESTING", "False").lower() in ("true", "1", "t")

    @classmethod
    def to_dict(cls) -> dict[str, Any]:
        """Return config as a dictionary."""
        return {
            "SECRET_KEY": cls.SECRET_KEY,
            "DATABASE_PATH": cls.DATABASE_PATH,
            "DEBUG": cls.DEBUG,
            "TESTING": cls.TESTING,
        }
