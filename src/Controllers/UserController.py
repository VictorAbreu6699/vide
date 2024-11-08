from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from src.Repositories.UserRepository import UserRepository
from src.Requests.UserCreateRequest import UserCreateRequest

router = APIRouter()
templates = Jinja2Templates(directory="src/Templates")


@router.post("/users")
def store(request: UserCreateRequest):
    UserRepository().create(request.dict())

    return {"message": "Usuário criado com sucesso!"}
