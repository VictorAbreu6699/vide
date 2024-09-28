from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.Controllers import HomeController

app = FastAPI()

# Configuração do diretório estático
app.mount("/static", StaticFiles(directory="src/Templates"), name="static")

# Adiciona os routers dos controladores à aplicação
app.include_router(HomeController.router)
