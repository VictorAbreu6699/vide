from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="src/Templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="reports/index.html"
    )


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(
        request=request, name="login/login.html"
    )


@router.get("/minha-conta")
def login(request: Request):
    return templates.TemplateResponse(
        request=request, name="login/myAccount.html"
    )


@router.get("/criar-conta")
def create_account(request: Request):
    return templates.TemplateResponse(
        request=request, name="login/createAccount.html"
    )


@router.get("/cadastro-dataset")
def store_datasets(request: Request):
    return templates.TemplateResponse(
        request=request, name="datasets/storeDataset.html"
    )


@router.get("/datasets")
def datasets(request: Request):
    return templates.TemplateResponse(
        request=request, name="datasets/index.html"
    )


@router.get("/cadastro-relatorio")
def store_report(request: Request):
    return templates.TemplateResponse(
        request=request, name="reports/storeReport.html"
    )


@router.get("/editar-relatorio/{report_id}")
def update_report(request: Request):
    return templates.TemplateResponse(
        request=request, name="reports/updateReport.html"
    )

@router.get("/editar-relatorio/visualizacoes/{report_id}")
def update_report(request: Request):
    return templates.TemplateResponse(
        request=request, name="reports/updateReportVisualization.html"
    )


@router.get("/relatorio")
def reports(request: Request):
    return templates.TemplateResponse(
        request=request, name="relatorio.html"
    )
