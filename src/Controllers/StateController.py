import os
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Form, UploadFile, File, Query
from starlette.responses import JSONResponse, FileResponse
from src.Helpers.JWTHelper import JWTHelper
from src.Helpers.ModelHelper import ModelHelper
from src.Repositories.DatasetColumnRepository import DatasetColumnRepository
from src.Repositories.DatasetRepository import DatasetRepository
from src.Repositories.ReportRepository import ReportRepository
from src.Repositories.StateRepository import StateRepository
from src.Services.DatasetService import DatasetService

router = APIRouter(prefix="/states", tags=['States'])


@router.get("/get-states")
def get_states(search: Optional[str] = Query(None)):
    data = StateRepository().get_all(search).to_dict(orient="records")

    return JSONResponse(
        status_code=200,
        content={"message": "Sucesso!", "data": data}
    )
