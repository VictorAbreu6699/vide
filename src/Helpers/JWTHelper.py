import os
from datetime import datetime, timedelta

from src.Helpers.CryptHelper import CryptHelper
import jwt


class JWTHelper:
    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        hashed_password = CryptHelper().decrypt(hashed_password)

        return hashed_password == plain_password

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str):
        try:
            payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token expirado")
            return None
        except jwt.InvalidTokenError:
            print("Token inválido")
            return None
