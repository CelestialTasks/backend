from fastapi import FastAPI

from app.routers import projects

app = FastAPI(title="Task Manager API", root_path="/api")

app.include_router(projects.router)
