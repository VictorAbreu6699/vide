from typing import Union

from pydantic import BaseModel


class CreateAccountRequest(BaseModel):
    name: str = None
    email: str = None
    password: str = None
