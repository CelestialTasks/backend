from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: str
    username: str
    email: str


class UserCreate(UserBase):
    pass
