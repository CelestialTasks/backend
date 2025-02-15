from pydantic import BaseModel
from typing import Optional


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None