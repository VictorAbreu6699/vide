import locale
from typing import Optional

import numpy as np
from fastapi import APIRouter, Query
from starlette.responses import JSONResponse
from src.Repositories.CityRepository import CityRepository

router = APIRouter(prefix="/cities", tags=['Cities'])


@router.get("/get-cities")
def get_states(search: Optional[str] = Query(None), state_id: Optional[int] = Query(None)):
    data = CityRepository().get_all(search, state_id)
    data['duplicated'] = data['name'].duplicated(keep=False)

    data['name'] = np.where(
        data['duplicated'] == True,
        data['name'] + " (" + data['state_name'] + ")",
        data['name']
    )
    # Configura o locale para português do Brasil
    locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')

    # Função para usar o locale na ordenação
    data['sort_key'] = data['name'].apply(locale.strxfrm)

    # Ordena com base na chave normalizada
    data = data.sort_values(by='sort_key').drop(columns='sort_key')

    return JSONResponse(
        status_code=200,
        content={"message": "Sucesso!", "data": data.to_dict(orient="records")}
    )
