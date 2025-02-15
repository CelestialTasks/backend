from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas import ProjectBase, ProjectCreate, Project, ProjectUpdate

router = APIRouter(prefix="/api/projects", tags=["projects"])


# Временное "хранилище" для проектов
projects_db: List[Project] = [
    Project(id=1, name="Project 1", description="Description 1", owner_id=1),
    Project(id=2, name="Project 2", description="Description 2", owner_id=2)
]


def get_project_index(project_id: int) -> int:
    for index, project in enumerate(projects_db):
        if project.id == project_id:
            return index
    return -1


# GET /projects – получение списка проектов
@router.get("/", response_model=List[Project])
async def get_projects():
    return projects_db


# GET /projects/{project_id} – получение конкретного проекта
@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: int):
    index = get_project_index(project_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects_db[index]


# POST /projects – создание нового проекта
@router.post("/", response_model=Project, status_code=201)
async def create_project(project: ProjectCreate):
    new_id = max([p.id for p in projects_db], default=0) + 1
    new_project = Project(id=new_id, **project.dict())
    projects_db.append(new_project)
    return new_project


# PATCH /projects/{project_id} – обновление проекта
@router.patch("/{project_id}", response_model=Project)
async def update_project(project_id: int, project_update: ProjectUpdate):
    index = get_project_index(project_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Project not found")
    current_project_data = projects_db[index].dict()
    update_data = project_update.dict(exclude_unset=True)
    updated_project_data = {**current_project_data, **update_data}
    updated_project = Project(**updated_project_data)
    projects_db[index] = updated_project
    return updated_project


# DELETE /projects/{project_id} – удаление проекта
@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: int):
    index = get_project_index(project_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Project not found")
    projects_db.pop(index)
    return None
