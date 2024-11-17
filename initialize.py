from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

# Gerar a chave Fernet
key = Fernet.generate_key()

# Carregar ou criar o arquivo .env
load_dotenv()

# Definir a chave no arquivo .env
set_key(".env", "HASH_KEY", key.decode())

print("Chave Criptografia gerada")
