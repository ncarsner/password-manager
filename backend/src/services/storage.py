from __future__ import annotations

import sqlite3
from contextlib import closing
from typing import Any

from ..models.vault import Vault


class StorageService:
    """Service for handling data storage and retrieval using SQLite.

    Attributes:
        db_path: Path to the SQLite database file.
    """

    def __init__(self, db_path: str = "database.db") -> None:
        """Initialize the StorageService.

        Args:
            db_path: Path to the SQLite database. Defaults to "database.db".
        """
        self.db_path = db_path

    def _get_connection(self) -> Any:
        """Create and return a new database connection wrapper.

        Returns:
            A context manager for a sqlite3 Connection object.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return closing(conn)

    def save_vault(self, vault: Vault) -> int:
        """Save a vault to the database.

        Args:
            vault: The Vault instance to save.

        Returns:
            The ID of the saved vault.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO vaults (name) VALUES (?) ON CONFLICT(name) DO UPDATE SET name=name",
                (vault.name,),
            )
            conn.commit()
            if cursor.lastrowid:
                vault.id = cursor.lastrowid
                return vault.id

            # If no lastrowid (no insert), fetch existing
            cursor.execute("SELECT id FROM vaults WHERE name = ?", (vault.name,))
            row = cursor.fetchone()
            vault.id = row["id"]
            return vault.id

    def get_all_vaults(self) -> list[dict[str, Any]]:
        """Retrieve all vaults from the database.

        Returns:
            A list of dictionaries representing vaults.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM vaults")
            return [dict(row) for row in cursor.fetchall()]

    def get_vault_by_id(self, vault_id: int) -> dict[str, Any] | None:
        """Retrieve a single vault by its ID.

        Args:
            vault_id: The unique identifier of the vault.

        Returns:
            A dictionary representing the vault, or None if not found.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM vaults WHERE id = ?", (vault_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def save_password(
        self,
        vault_id: int,
        domain: str,
        username: str,
        encrypted_password: bytes,
        notes: str = "",
    ) -> int:
        """Save an encrypted credential to a specific vault.

        Args:
            vault_id: The ID of the vault.
            domain: The domain or service name (e.g. github.com).
            username: The username or email for the credential.
            encrypted_password: The encrypted password bytes.
            notes: Optional free-text notes. Defaults to empty string.

        Returns:
            The ID of the saved credential entry.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO passwords (vault_id, domain, username, password, notes)"
                " VALUES (?, ?, ?, ?, ?)",
                (vault_id, domain, username, encrypted_password, notes),
            )
            conn.commit()
            return cursor.lastrowid or 0

    def get_passwords(self, vault_id: int) -> list[dict[str, Any]]:
        """Retrieve all credentials for a specific vault.

        Args:
            vault_id: The ID of the vault.

        Returns:
            A list of dicts with keys: id, domain, username, password, notes.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, domain, username, password, notes"
                " FROM passwords WHERE vault_id = ?",
                (vault_id,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def update_password(
        self,
        password_id: int,
        domain: str | None = None,
        username: str | None = None,
        encrypted_password: bytes | None = None,
        notes: str | None = None,
    ) -> bool:
        """Update fields on an existing credential entry.

        Args:
            password_id: The ID of the credential to update.
            domain: New domain value, or None to leave unchanged.
            username: New username value, or None to leave unchanged.
            encrypted_password: New encrypted password bytes, or None to leave unchanged.
            notes: New notes value, or None to leave unchanged.

        Returns:
            True if a row was updated, False if not found or no fields given.
        """
        fields: list[str] = []
        values: list[Any] = []
        if domain is not None:
            fields.append("domain = ?")
            values.append(domain)
        if username is not None:
            fields.append("username = ?")
            values.append(username)
        if encrypted_password is not None:
            fields.append("password = ?")
            values.append(encrypted_password)
        if notes is not None:
            fields.append("notes = ?")
            values.append(notes)
        if not fields:
            return False
        values.append(password_id)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE passwords SET {', '.join(fields)} WHERE id = ?",  # noqa: S608
                values,
            )
            conn.commit()
            return bool(cursor.rowcount > 0)

    def delete_password(self, password_id: int) -> bool:
        """Delete a specific password entry.

        Args:
            password_id: The ID of the password to delete.

        Returns:
            True if a row was deleted, False otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
            conn.commit()
            return bool(cursor.rowcount > 0)

    def delete_vault(self, vault_id: int) -> bool:
        """Delete a vault and all its associated passwords.

        Args:
            vault_id: The ID of the vault to delete.

        Returns:
            True if the vault was deleted, False otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Failsafe: ensure cascade or manual delete
            cursor.execute("DELETE FROM vaults WHERE id = ?", (vault_id,))
            conn.commit()
            return bool(cursor.rowcount > 0)
