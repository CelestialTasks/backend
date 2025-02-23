from fastapi import APIRouter, HTTPException, Query
from typing import List

from app.models import Project
from app.schemas import ProjectCreate, Project, ProjectUpdate, ProjectUser, ProjectUserCreate

router = APIRouter(prefix="/projects", tags=["projects"])

