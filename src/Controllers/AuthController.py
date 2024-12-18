import re

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from src.Helpers.JWTHelper import JWTHelper
from src.Repositories.UserRepository import UserRepository
from src.Requests.LoginRequest import LoginRequest
from src.Requests.CreateAccountRequest import CreateAccountRequest

router = APIRouter(prefix="/auth", tags=['Auth'])


@router.post("/login")
def login(request: LoginRequest):
    user = UserRepository().get_by_email(request.email)
    if user is None:
        return JSONResponse(
            status_code=400,
            content={"message": "E-mail ou senha incorretos."}
        )

    login_validated = JWTHelper().verify_password(request.password, user.password)
    if not login_validated:
        return JSONResponse(
            status_code=400,
            content={"message": "E-mail ou senha incorretos."}
        )

    access_token = JWTHelper.create_access_token({"sub": user.email})

    return JSONResponse(
        status_code=200,
        content={"message": "Login realizado com sucesso!", "access_token": access_token, "token_type": "Bearer"}
    )


@router.get('/check-login-test', dependencies=[Depends(JWTHelper.validate_token)])
def test_login():
    return {'message': 'logado'}


@router.post("/create-account")
def store(request: CreateAccountRequest):

    if request.name is None or request.name == "":
        return JSONResponse(
            status_code=400,
            content={"message": "É obrigatorio inserir o Usuário"}
        )
    if request.email is None or request.email == "":
        return JSONResponse(
            status_code=400,
            content={"message": "É obrigatorio inserir o E-mail"}
        )
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', request.email):
        return JSONResponse(
            status_code=400,
            content={"message": "E-mail inválido"}
        )

    if request.password is None or request.password == "":
        return JSONResponse(
            status_code=400,
            content={"message": "É obrigatorio inserir a Senha"}
        )

    user = UserRepository().get_by_email(request.email)
    existing_user = user is not None
    if existing_user:
        return JSONResponse(
            status_code=400,
            content={"message": "E-mail já está em uso"}
        )
    try:
        UserRepository().create(request.dict())
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Erro interno ao realizar cadastro."}
        )

    return JSONResponse(
        status_code=201,
        content={"message": "Conta criada com sucesso!"}
    )
