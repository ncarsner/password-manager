from __future__ import annotations


class Vault:
    """Model representing a secure password vault.

    Attributes:
        name: The display name of the vault.
        id: Unique identifier for the vault (None if not yet persisted).
        passwords: List of passwords stored in this vault.
    """

    def __init__(self, name: str, vault_id: int | None = None) -> None:
        """Initialize a new Vault instance.

        Args:
            name: The name of the vault.
            vault_id: Optional unique identifier.
        """
        self.name = name
        self.id = vault_id
        self.passwords: list[str] = []

    def add_password(self, password: str) -> None:
        """Add a password to the vault.

        Args:
            password: The password string to add.
        """
        self.passwords.append(password)

    def remove_password(self, password: str) -> None:
        """Remove a password from the vault.

        Args:
            password: The password string to remove.
        """
        if password in self.passwords:
            self.passwords.remove(password)

    def get_passwords(self) -> list[str]:
        """Return the list of passwords in the vault.

        Returns:
            A list of password strings.
        """
        return self.passwords

    def __repr__(self) -> str:
        """Return a string representation of the vault.

        Returns:
            String description of the vault.
        """
        return f"Vault(id={self.id}, name={self.name}, passwords={self.passwords})"
