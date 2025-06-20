import time
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse
from src.Helpers.JWTHelper import JWTHelper
from src.Repositories.ReportVisualizationRepository import ReportVisualizationRepository
from src.Requests.CreateReportVisualizationDatasetColumnRequest import CreateReportVisualizationDatasetColumnRequest
from src.Requests.UpdateReportVisualizationDatasetColumnRequest import UpdateReportVisualizationDatasetColumnRequest
from src.Services.ReportVisualizationService import ReportVisualizationService

router = APIRouter(prefix="/report-visualizations", tags=['Reports'])


@router.post("/", dependencies=[Depends(JWTHelper.validate_token)])
def create_report_visualization_dataset_columns(request: CreateReportVisualizationDatasetColumnRequest):
    if request.name is None or request.name == "":
        return JSONResponse(
            status_code=400,
            content={"message": "É obrigatorio inserir o nome da visualização!"}
        )

    ReportVisualizationService.store_report_visualization(request)

    return JSONResponse(
        status_code=201,
        content={"message": "Vinculo de visualização com relátorio criada com sucesso!"}
    )


@router.get("/{report_id}")
def get_report_visualizations(report_id: int):
    data = ReportVisualizationRepository().get_by_report_id(report_id)

    return JSONResponse(
        status_code=200,
        content={"message": "Sucesso!", "data": data.to_dict(orient="records")}
    )


@router.get("/get_report_visualizations_to_edit/{report_visualization_id}")
def get_report_visualizations_to_edit(report_visualization_id: int):
    report_visualization = ReportVisualizationRepository().get_report_visualizations_to_edit(report_visualization_id)

    return JSONResponse(
        status_code=200,
        content={"message": "Sucesso!", "data": report_visualization}
    )


@router.put("/{report_visualization_id}", dependencies=[Depends(JWTHelper.validate_token)])
def update_report_visualization_dataset_columns(
        report_visualization_id: int, request: UpdateReportVisualizationDatasetColumnRequest
):
    if request.name is None or request.name == "":
        return JSONResponse(
            status_code=400,
            content={"message": "É obrigatorio inserir o nome da visualização!"}
        )

    ReportVisualizationService.edit_report_visualization(report_visualization_id, request)

    return JSONResponse(
        status_code=201,
        content={"message": "Vinculo de visualização com relátorio editado com sucesso!"}
    )


@router.delete("/{report_visualization_id}", dependencies=[Depends(JWTHelper.validate_token)])
def delete_report_visualization_dataset_columns(report_visualization_id: int):
    ReportVisualizationService.delete_report_visualization(report_visualization_id)

    return JSONResponse(
        status_code=201,
        content={"message": "Vinculo de visualização com relátorio excluido com sucesso!"}
    )


@router.get("/get_report_visualizations_to_build_report/{report_id}")
def get_report_visualizations_to_build_report(
    report_id: int,
    year: Optional[str] = Query(None),
    sickness: Optional[str] = Query(None),
    state_id: Optional[int] = Query(None),
    city_id: Optional[int] = Query(None)
):
    df_report_visualizations = ReportVisualizationService.get_report_visualizations_to_build_report(
        report_id=report_id,
        year=year,
        sickness=sickness,
        state_id=state_id,
        city_id=city_id
    )

    return JSONResponse(
        status_code=200,
        content={"message": "Sucesso!", "data": df_report_visualizations.to_dict(orient="records")}
    )
