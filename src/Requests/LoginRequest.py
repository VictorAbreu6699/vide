from typing import Union

from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str = None
    password: str = None
