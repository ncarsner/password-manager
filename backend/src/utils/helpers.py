from __future__ import annotations


def validate_password(password: str) -> bool:
    """Validate a password based on security criteria.

    Args:
        password: The password string to validate.

    Returns:
        True if valid (length >= 8, has digit and alpha), False otherwise.
    """
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isalpha() for char in password):
        return False
    return True


def format_vault_name(name: str | None) -> str:
    """Format a vault name for display.

    Args:
        name: The raw vault name.

    Returns:
        A title-cased, trimmed name or "Untitled Vault" if empty.
    """
    return name.strip().title() if name else "Untitled Vault"


def sanitize_input(input_string: str | None) -> str:
    """Sanitize user input by trimming whitespace.

    Args:
        input_string: The raw input string.

    Returns:
        A trimmed string or empty string if None.
    """
    return input_string.strip() if input_string else ""
