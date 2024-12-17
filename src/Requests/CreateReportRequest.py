from pydantic import BaseModel


class CreateReportRequest(BaseModel):
    name: str = None
    description: str = None
    dataset_id: int = None
