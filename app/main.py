from fastapi import FastAPI

from app.database import engine
from app.routers import users
from app.models import Base

# TODO: remove this line when we switch to Postgre
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Task Manager API")
app.include_router(users.router)
