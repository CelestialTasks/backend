from fastapi import APIRouter, HTTPException, Query
from typing import List

from app.schemas import ProjectCreate, Project, ProjectUpdate, ProjectUser, ProjectUserCreate

router = APIRouter(prefix="/projects", tags=["projects"])


# Временное "хранилище" для проектов
projects_db: List[Project] = [
    Project(id=1, name="Project 1", description="Description 1", owner_id=1),
    Project(id=2, name="Project 2", description="Description 2", owner_id=2)
]
project_users_db: List[ProjectUser] = []


def get_project_index(project_id: int) -> int:
    for index, project in enumerate(projects_db):
        if project.id == project_id:
            return index
    return -1


# GET /projects – getting a list of projects
@router.get("/", response_model=List[Project])
async def get_projects():
    return projects_db


# GET /projects/{project_id} – obtaining a specific project
@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: int):
    index = get_project_index(project_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects_db[index]


# POST /projects – creating a new project
@router.post("/", response_model=Project, status_code=201)
async def create_project(project: ProjectCreate):
    new_id = max([p.id for p in projects_db], default=0) + 1
    new_project = Project(id=new_id, **project.dict())
    projects_db.append(new_project)
    return new_project


# PATCH /projects/{project_id} – project update
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


# DELETE /projects/{project_id} – project delete
@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: int):
    index = get_project_index(project_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Project not found")
    projects_db.pop(index)
    return None


# POST /api/project_user/ — create a new connection
@router.post("/", response_model=ProjectUser, status_code=201)
async def create_project_user(association: ProjectUserCreate):
    for assoc in project_users_db:
        if assoc.project_id == association.project_id and assoc.user_id == association.user_id:
            raise HTTPException(status_code=400, detail="Association already exists")
    new_assoc = ProjectUser(**association.dict())
    project_users_db.append(new_assoc)
    return new_assoc


# GET /api/project_user/?project_id=<id> — get a list of connections by project ID
@router.get("/", response_model=List[ProjectUser])
async def get_project_users(project_id: int = Query(..., description="ID of the project")):
    associations = [assoc for assoc in project_users_db if assoc.project_id == project_id]
    return associations


# DELETE /api/project_user/{project_id}/{user_id} — delete connection
@router.delete("/{project_id}/{user_id}", status_code=204)
async def delete_project_user(project_id: int, user_id: int):
    for index, assoc in enumerate(project_users_db):
        if assoc.project_id == project_id and assoc.user_id == user_id:
            project_users_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Association not found")
