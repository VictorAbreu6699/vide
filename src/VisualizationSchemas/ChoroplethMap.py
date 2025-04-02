from pydantic import BaseModel


class ChoroplethMap(BaseModel):
    sickness: str = None
    latitude: float
    longitude: float
    city_name: str
    cases: int
