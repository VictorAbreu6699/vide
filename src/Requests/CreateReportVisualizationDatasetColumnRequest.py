from typing import List

from pydantic import BaseModel


class CreateReportVisualizationDatasetColumnRequest(BaseModel):
    name: str = None
    report_id: int = None
    field_id: List[int] = None
    field_value: List[int] = None
    visualization_id: int = None
