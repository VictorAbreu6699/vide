from typing import Optional

from fastapi import APIRouter, Query
from starlette.responses import JSONResponse
from src.Repositories.VisualizationRepository import VisualizationRepository

router = APIRouter(prefix="/visualizations", tags=['Visualizations'])


@router.get("/get-visualizations")
def get_visualizations(search: Optional[str] = Query(None)):
    data = VisualizationRepository().get_all(search).to_dict(orient="records")

    return JSONResponse(
        status_code=200,
        content={"message": "Sucesso!", "data": data}
    )


@router.get("/get-visualization-fields/{visualization_id}")
def get_visualization_fields(visualization_id: int):
    data = VisualizationRepository().get_visualization_fields(visualization_id)

    return JSONResponse(
        status_code=200,
        content={"message": "Sucesso!", "data": data.to_dict(orient='records')}
    )
