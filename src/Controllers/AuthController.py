from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates

from src.Helpers.JWTHelper import JWTHelper
from src.Repositories.UserRepository import UserRepository
from src.Requests.LoginRequest import LoginRequest
from src.Requests.UserCreateRequest import UserCreateRequest

router = APIRouter()
templates = Jinja2Templates(directory="src/Templates")


@router.post("/login")
def login(request: LoginRequest):
    user = UserRepository().get_by_email(request.email)
    if user is None:
        return {"message": "E-mail ou senha incorretos."}

    login_validated = JWTHelper().verify_password(request.password, user.password)
    if not login_validated:
        return {"message": "E-mail ou senha incorretos."}

    access_token = JWTHelper.create_access_token({"sub": user.email})

    return {"message": "Login realizado com sucesso!", "access_token": access_token, "token_type": "bearer"}


@router.get('/check-login-test', dependencies=[Depends(JWTHelper.validate_token)])
def test_login():
    return {'message': 'logado'}
