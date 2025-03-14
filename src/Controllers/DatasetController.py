import os
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Form, UploadFile, File, Query
from starlette.responses import JSONResponse, FileResponse
from src.Helpers.JWTHelper import JWTHelper
from src.Helpers.ModelHelper import ModelHelper
from src.Repositories.DatasetRepository import DatasetRepository
from src.Repositories.ReportRepository import ReportRepository
from src.Services.DatasetService import DatasetService

router = APIRouter(prefix="/datasets", tags=['Datasets'])


@router.get("/get-datasets")
def get_datasets(search: Optional[str] = Query(None)):
    data = DatasetRepository().get_all(search).to_dict(orient="records")

    return JSONResponse(
        status_code=201,
        content={"message": "Sucesso!", "data": data}
    )


@router.get("/show-dataset/{dataset_id}")
async def show_dataset(dataset_id: int):
    # Verificando se o dataset existe
    dataset = DatasetRepository().get_by_id(dataset_id)
    if not dataset:
        return JSONResponse(
            status_code=404,
            content={"message": "Fonte de dados não encontrada!"}
        )
    dataset = ModelHelper.model_to_dict(dataset)

    return JSONResponse(
        status_code=201,
        content={"message": "Sucesso!", "data": dataset}
    )


@router.post("/", dependencies=[Depends(JWTHelper.validate_token)])
async def upload_file(
        name: str = Form(...), description: str = Form(...), file: UploadFile = File(...),
        token: str = Depends(JWTHelper.get_token_from_header)
):
    # Tipos de arquivos permitidos
    allowed_content_types = [
        "text/csv",  # Arquivo CSV
        "application/vnd.ms-excel",  # Arquivo XLS
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # Arquivo XLSX
    ]
    if file.content_type not in allowed_content_types:
        return JSONResponse(
            status_code=400,
            content={"message": "Tipo de arquivo não suportado."}
        )

    try:
        DatasetService.upload_file(name, description, file, token)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Erro ao enviar arquivo. Erro: " + str(e)}
        )

    return JSONResponse(
        status_code=201,
        content={"message": "Arquivo enviado com sucesso!"}
    )


@router.get("/download-file/{dataset_id}")
async def download_file(dataset_id: int):
    # Verificando se o dataset existe
    dataset = DatasetRepository().get_by_id(dataset_id)
    if not dataset:
        return JSONResponse(
            status_code=404,
            content={"message": "Fonte de dados não encontrada!"}
        )

    # Retorna o arquivo para download
    return FileResponse(
        path=dataset.path,
        filename=dataset.name + dataset.extension,
        media_type="application/octet-stream",
    )


@router.get("/get-dataset-columns/{report_id}")
async def get_dataset_columns(report_id: int):
    # Verificando se o relatorio existe
    report = ReportRepository().get_by_id(report_id)
    if not report:
        return JSONResponse(
            status_code=404,
            content={"message": "Relatório não encontrado!"}
        )
    dataset = DatasetRepository().get_by_id(report.dataset_id)
    dataset = ModelHelper.model_to_dict(dataset)

    return JSONResponse(
        status_code=201,
        content={"message": "Sucesso!", "data": dataset}
    )
