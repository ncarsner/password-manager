import sqlite3
from contextlib import closing
from typing import Any

from flask import Flask
from flask_cors import CORS

from .api.v1 import api_v1
from .config import Config


def init_db(db_path: str = "database.db") -> None:
    """Initialize the database schema if it doesn't exist.

    Args:
        db_path: Path to the SQLite database file.
    """
    with closing(sqlite3.connect(db_path)) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vaults (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vault_id INTEGER,
                password BLOB NOT NULL,
                FOREIGN KEY (vault_id) REFERENCES vaults (id) ON DELETE CASCADE
            )
        """
        )
        conn.commit()


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
init_db(app.config.get("DATABASE_PATH", "database.db"))

app.register_blueprint(api_v1, url_prefix="/api/v1")


@app.route("/")
def home() -> Any:
    """Home endpoint."""
    return "Welcome to the Password Manager API!"


if __name__ == "__main__":
    app.run(debug=True)
