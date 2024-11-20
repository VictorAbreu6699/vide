from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="src/Templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(
        request=request, name="login/login.html"
    )


@router.get("/criar-conta")
def login(request: Request):
    return templates.TemplateResponse(
        request=request, name="login/createAccount.html"
    )


@router.get("/cadastro-dataset")
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="datasets/index.html"
    )


@router.get("/relatorio")
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="relatorio.html"
    )
