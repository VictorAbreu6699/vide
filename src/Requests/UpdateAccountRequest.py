from typing import Union

from pydantic import BaseModel


class UpdateAccountRequest(BaseModel):
    name: str = None
    email: str = None
    password: str = None
