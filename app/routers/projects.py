from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ProjectCreate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", status_code=204)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    ...
