from pydantic import BaseModel, EmailStr, field_validator

from src.Repositories.UserRepository import UserRepository


class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    # Verifica se o e-mail já está em uso
    @field_validator('email')
    def check_email_unique(cls, email: str):
        user = UserRepository().get_by_email(email)
        existing_user = user is not None
        if existing_user:
            raise ValueError('E-mail já está em uso')
        return email

    @field_validator("password")
    def password_min_length(cls, password: str):
        if len(password) < 8:
            raise ValueError("A senha deve conter pelo menos 8 caracteres.")
        return password
