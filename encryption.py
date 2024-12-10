from cryptography.fernet import Fernet

# Generate a key and instantiate a Fernet instance
key = Fernet.generate_key()
cipher_suite = Fernet(key)


def encrypt(data):
    if isinstance(data, str):
        data = data.encode()
    return cipher_suite.encrypt(data)


def decrypt(data):
    return cipher_suite.decrypt(data).decode()
