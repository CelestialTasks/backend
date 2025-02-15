from fastapi import FastAPI

from app.routers import projects

app = FastAPI(title="Task Manager API")

app.include_router(projects.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Task Manager API!"}
