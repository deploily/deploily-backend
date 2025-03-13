from cryptography.fernet import Fernet


class FernetEncryptor:
    def __init__(self, key: str = None):
        """Initialize Fernet with a given key."""
        self.key = key or Fernet.generate_key()  # Generate a new key if none is provided

        if not isinstance(self.key, bytes):  # Ensure key is in bytes format
            raise ValueError("FERNET_KEY must be in bytes format!")

        self.fernet = Fernet(self.key)

    def encrypt(self, plain_text: str) -> str:
        """Encrypts a string."""
        print(f"##############################################{plain_text}")
        print(self.fernet.encrypt(plain_text.encode()).decode())
        return self.fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, encrypted_text: str) -> str:
        """Decrypts a string."""
        print(f"##############################################{encrypted_text}")
        print(self.fernet.decrypt(encrypted_text.encode()).decode())
        return self.fernet.decrypt(encrypted_text.encode()).decode()
