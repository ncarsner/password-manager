from __future__ import annotations

from cryptography.fernet import Fernet


class CryptoService:
    """Service for handling cryptographic operations.

    Uses Fernet (AES-128 in CBC mode with HMAC-SHA256) for symmetric encryption.
    """

    def __init__(self, key: bytes | None = None) -> None:
        """Initialize the CryptoService.

        Args:
            key: Optional encryption key. If not provided, a new one is generated.
        """
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.cipher = Fernet(self.key)

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypt a plaintext string.

        Args:
            plaintext: The string to encrypt.

        Returns:
            The encrypted ciphertext as bytes.
        """
        return self.cipher.encrypt(plaintext.encode())

    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypt a ciphertext.

        Args:
            ciphertext: The encrypted bytes to decrypt.

        Returns:
            The decrypted plaintext as a string.
        """
        return self.cipher.decrypt(ciphertext).decode()
