from fastapi import APIRouter

from app.routers import projects

api_router = APIRouter(prefix="/api")

api_router.include_router(projects.router, prefix="/projects", tags=["projects"])

# Пример подключения других роутеров:
# from app.routers import users
# api_router.include_router(users.router, prefix="/users", tags=["users"])
