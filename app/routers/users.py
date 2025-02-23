from fastapi import APIRouter

from app.models import User

router = APIRouter(prefix="/users", tags=["users"])


# POST /users/ – Create a user
@router.post("/", response_model=User)
async def create_user():
    pass
