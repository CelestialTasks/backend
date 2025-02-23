from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: int
    email: str
    token: str
