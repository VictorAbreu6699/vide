from typing import List

from pydantic import BaseModel


class FiltersRequest(BaseModel):
    name: str
    report_id: int
