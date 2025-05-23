from typing import Optional

import numpy as np
from fastapi import APIRouter, Query
from starlette.responses import JSONResponse
from src.Repositories.CityRepository import CityRepository

router = APIRouter(prefix="/cities", tags=['Cities'])


@router.get("/get-cities")
def get_states(search: Optional[str] = Query(None)):
    data = CityRepository().get_all(search)
    data['duplicated'] = data['name'].duplicated(keep=False)

    data['name'] = np.where(
        data['duplicated'] == True,
        data['name'] + " (" + data['state_name'] + ")",
        data['name']
    )
    
    data = data.sort_values(by=['name'])

    return JSONResponse(
        status_code=200,
        content={"message": "Sucesso!", "data": data.to_dict(orient="records")}
    )
