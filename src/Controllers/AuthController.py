import re

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from src.Helpers.JWTHelper import JWTHelper
from src.Helpers.ModelHelper import ModelHelper
from src.Repositories.UserRepository import UserRepository
from src.Requests.LoginRequest import LoginRequest
from src.Requests.CreateAccountRequest import CreateAccountRequest
from src.Requests.UpdateAccountRequest import UpdateAccountRequest

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


@router.post("/logout", dependencies=[Depends(JWTHelper.validate_token)])
def logout(token: str = Depends(JWTHelper.get_token_from_header)):
    JWTHelper.add_token_to_blacklist(token)

    return JSONResponse(
        status_code=200,
        content={"message": "Logout realizado com sucesso!"}
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


@router.post("/update-account", dependencies=[Depends(JWTHelper.validate_token)])
def update(request: UpdateAccountRequest, token: str = Depends(JWTHelper.get_token_from_header)):
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

    user_data = request.dict()
    if request.password is not None and request.password == "":
        user_data.pop("password")

    user = JWTHelper.get_user_from_token(token)
    user_email = UserRepository().get_by_email(request.email)
    # valida se o e-mail ja está em uso, e valida se é igual ou diferente ao e-mail do usuário que está sendo atualizado
    email_exists = user_email is not None and user_email.id != user.id

    if email_exists:
        return JSONResponse(
            status_code=400,
            content={"message": "E-mail já está em uso por outro usuário"}
        )
    try:
        UserRepository().update(user.id, user_data)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Erro interno ao realizar atualização."}
        )

    return JSONResponse(
        status_code=201,
        content={"message": "Conta atualizada com sucesso!"}
    )


@router.get("/show-logged-user", dependencies=[Depends(JWTHelper.validate_token)])
def show_logged_user(token: str = Depends(JWTHelper.get_token_from_header)):
    try:
        user = JWTHelper.get_user_from_token(token)
        if user is None:
            return JSONResponse(
                status_code=404,
                content={"message": "Usuário não encontrado!"}
            )

        user_dict = ModelHelper.model_to_dict(user)

        user_dict.pop("password")

        return JSONResponse(
            status_code=200,
            content={"message": "Conta atualizada com sucesso!", "data": user_dict}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Erro interno ao buscar dados do usuário."}
        )