from pydantic import BaseModel


class UserBase(BaseModel):
    clerk_id: str
    username: str
    email: str


class UserCreate(UserBase):
    pass
