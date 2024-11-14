import os

from cryptography.fernet import Fernet


class CryptHelper:
    def __init__(self):
        """Inicia a classe CryptoHelper com uma chave do .env"""
        self.key = os.getenv("HASH_KEY")

        if not self.key:
            raise Exception('Váriavel de ambiente HASH_KEY não preenchida.')

        self.cipher = Fernet(self.key.encode())

    def encrypt(self, data: str) -> str:
        """Criptografa os dados (string) fornecidos e retorna a versão criptografada"""
        encoded_data = data.encode()  # Converte os dados em bytes
        encrypted_data = self.cipher.encrypt(encoded_data)
        return encrypted_data.decode()  # Retorna como string

    def decrypt(self, encrypted_data: str) -> str:
        """Descriptografa os dados criptografados e retorna o texto original"""
        encrypted_data_bytes = encrypted_data.encode()  # Converte os dados criptografados de volta para bytes
        decrypted_data = self.cipher.decrypt(encrypted_data_bytes)
        return decrypted_data.decode()  # Retorna o texto original
