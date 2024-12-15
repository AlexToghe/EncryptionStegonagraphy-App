from Crypto.Cipher import Salsa20
from Crypto.Random import get_random_bytes


class EncryptionManager:
    @staticmethod
    def encrypt_message(message):
        """Encrypts a message using Salsa20."""
        key = get_random_bytes(32)  # Generate a random 256-bit key
        cipher = Salsa20.new(key)
        cipher_text = cipher.encrypt(message.encode())
        return key, cipher.nonce, cipher_text

    @staticmethod
    def decrypt_message(key, nonce, cipher_text):
        """Decrypts a cipher text using Salsa20."""
        try:
            cipher = Salsa20.new(key, nonce=nonce)
            plain_text = cipher.decrypt(cipher_text)
            return plain_text.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")

