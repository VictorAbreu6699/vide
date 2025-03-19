from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from src.Helpers.JWTHelper import JWTHelper
from src.Requests.CreateReportVisualizationDatasetColumnRequest import CreateReportVisualizationDatasetColumnRequest
from src.Services.ReportVisualizationService import ReportVisualizationService

router = APIRouter(prefix="/report-visualizations", tags=['Reports'])


@router.post("/", dependencies=[Depends(JWTHelper.validate_token)])
def create_report_visualization_dataset_columns(request: CreateReportVisualizationDatasetColumnRequest):
    if request.name is None or request.name == "":
        return JSONResponse(
            status_code=400,
            content={"message": "É obrigatorio inserir o nome do relatório!"}
        )

    ReportVisualizationService.store_report_visualization(request)

    return JSONResponse(
        status_code=201,
        content={"message": "Relátorio criado com sucesso!"}
    )
