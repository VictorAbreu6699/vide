from starlette.staticfiles import StaticFiles
from src.Controllers import TemplateController, UserController, AuthController, DatasetController
from fastapi import FastAPI

app = FastAPI()

# Configuração do diretório estático
app.mount("/static", StaticFiles(directory="src/Templates"), name="static")

# Adiciona os routers dos controladores à aplicação
app.include_router(TemplateController.router)
app.include_router(UserController.router)
app.include_router(AuthController.router)
app.include_router(DatasetController.router)
