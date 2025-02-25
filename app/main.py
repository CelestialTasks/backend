from fastapi import FastAPI

from app.database import engine
from app.routers import users
from app.models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")
app.include_router(users.router)
