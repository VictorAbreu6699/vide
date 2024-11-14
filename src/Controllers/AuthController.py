from fastapi import APIRouter
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
    login_validated = JWTHelper().verify_password(user.password, request.password)
    if not login_validated:
        return {"message": "E-mail ou senha incorretos."}

    token = JWTHelper.create_access_token()

    return {"message": "Login realizado com sucesso!", "token": token}
