from typing import Optional

from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse
from src.Helpers.JWTHelper import JWTHelper
from src.Helpers.ModelHelper import ModelHelper
from src.Repositories.DatasetRepository import DatasetRepository
from src.Repositories.ReportRepository import ReportRepository
from src.Requests.CreateReportRequest import CreateReportRequest

router = APIRouter(prefix="/reports", tags=['Reports'])


@router.get("/get-reports")
def get_reports(search: Optional[str] = Query(None)):
    data = ReportRepository().get_all(search).to_dict(orient="records")

    return JSONResponse(
        status_code=201,
        content={"message": "Sucesso!", "data": data}
    )


@router.get("/show-report/{report_id}")
async def show_report(report_id: int):
    # Verificando se o relatorio existe
    report = ReportRepository().get_by_id(report_id)
    if not report:
        return JSONResponse(
            status_code=404,
            content={"message": "Relátorio não encontrado!"}
        )
    report = ModelHelper.model_to_dict(report)

    return JSONResponse(
        status_code=200,
        content={"message": "Sucesso!", "data": report}
    )


@router.post("/", dependencies=[Depends(JWTHelper.validate_token)])
def create_report(request: CreateReportRequest, token: str = Depends(JWTHelper.get_token_from_header)):
    if request.name is None or request.name == "":
        return JSONResponse(
            status_code=400,
            content={"message": "É obrigatorio inserir o nome do relatório!"}
        )

    if request.description is None or request.description == "":
        return JSONResponse(
            status_code=400,
            content={"message": "É obrigatorio inserir a descrição!"}
        )

    if request.dataset_id is None or request.dataset_id == "":
        return JSONResponse(
            status_code=400,
            content={"message": "É obrigatorio inserir a fonte de dados!"}
        )

    dataset = DatasetRepository().get_by_id(request.dataset_id)
    if dataset is None:
        return JSONResponse(
            status_code=400,
            content={"message": "A fonte de dados informada é inválida!"}
        )

    user = JWTHelper.get_user_from_token(token)

    report = ReportRepository().create({
        "name": request.name, "description": request.description, "dataset_id": request.dataset_id, "user_id": user.id
    })

    return JSONResponse(
        status_code=201,
        content={"message": "Relátorio criado com sucesso!", "report_id": report.id}
    )


@router.put("/{report_id}", dependencies=[Depends(JWTHelper.validate_token)])
def create_report(report_id, request: CreateReportRequest, token: str = Depends(JWTHelper.get_token_from_header)):
    report = ReportRepository().get_by_id(report_id)

    if request.name is None or request.name == "":
        return JSONResponse(
            status_code=400,
            content={"message": "É obrigatorio inserir o nome do relatório!"}
        )

    if request.description is None or request.description == "":
        return JSONResponse(
            status_code=400,
            content={"message": "É obrigatorio inserir a descrição!"}
        )

    user = JWTHelper.get_user_from_token(token)

    if report.user_id != user.id:
        return JSONResponse(
            status_code=403,
            content={"message": "Somente o usuário que criou o relátorio pode edita-lo!"}
        )

    report = ReportRepository().update(report_id, {
        "name": request.name, "description": request.description
    })

    return JSONResponse(
        status_code=200,
        content={"message": "Relátorio atualizado com sucesso!"}
    )
