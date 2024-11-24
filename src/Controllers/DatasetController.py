import os
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Form, UploadFile, File, Query
from starlette.responses import JSONResponse, FileResponse
from src.Helpers.JWTHelper import JWTHelper
from src.Helpers.ModelHelper import ModelHelper
from src.Repositories.DatasetRepository import DatasetRepository

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

    # Cria a pasta storage/datasets, caso não exista.
    if not os.path.exists("storage/datasets"):
        os.makedirs("storage/datasets")
    # Salva o arquivo na pasta storage
    _, extension = os.path.splitext(file.filename)
    file_path = os.path.join("storage/datasets", uuid.uuid4().__str__() + extension)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    user = JWTHelper.get_user_from_token(token)

    DatasetRepository().create({
        "name": name, "description": description, "extension": extension, "path": file_path, "user_id": user.id
    })

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
