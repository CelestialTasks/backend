from fastapi import FastAPI
from database import engine

from app.routers import projects
from models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API", prefix="/api")
app.include_router(projects.router)
