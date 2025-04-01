from pydantic import BaseModel, Field


class UserBase(BaseModel):
    user_id: str
    username: str
    email: str


class UserCreate(UserBase):
    id: int
    user_id: str = Field(..., alias="clerk_id")


class UserList(BaseModel):
    id: int
    username: str
    email: str


class ProjectCreate(BaseModel):
    name: str
    description: str
