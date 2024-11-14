import os
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.Helpers.CryptHelper import CryptHelper
import jwt
from dotenv import load_dotenv

class JWTHelper:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    load_dotenv()

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        hashed_password = CryptHelper().decrypt(hashed_password)

        return hashed_password == plain_password

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60)))
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

    @staticmethod
    def is_user_logged_in(token: str) -> bool:
        payload = JWTHelper.decode_access_token(token)
        # Retorna True se o token for válido, caso contrário False
        return payload is not None

    @staticmethod
    def validate_token(token: str = Depends(oauth2_scheme)):
        # Verifica se o usuário está logado
        if not JWTHelper.is_user_logged_in(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"}
            )
