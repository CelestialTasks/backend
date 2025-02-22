from pydantic import BaseModel
from typing import Optional

# Project


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

# Project_User


class ProjectUserBase(BaseModel):
    project_id: int
    user_id: int


class ProjectUserCreate(ProjectUserBase):
    pass


class ProjectUser(ProjectUserBase):
    pass
