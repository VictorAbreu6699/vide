import os
import uuid

from fastapi import APIRouter, Depends, Form, UploadFile, File
from starlette.responses import JSONResponse

from src.Helpers.JWTHelper import JWTHelper
from src.Repositories.DatasetRepository import DatasetRepository

router = APIRouter(prefix="/datasets", tags=['Auth'])


@router.post("/", dependencies=[Depends(JWTHelper.validate_token)])
async def upload_file(
    name: str = Form(...), file: UploadFile = File(...), token: str = Depends(JWTHelper.get_token_from_header)
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

    DatasetRepository().create({"name": name, "path": file_path, "user_id": user.id})

    return JSONResponse(
        status_code=201,
        content={"message": "Arquivo enviado com sucesso!"}
    )
