from clerk_backend_api import Clerk
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth import TranscriptedUser
from app.database import get_db
from app.models import User
from app.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["users"])

clerk = Clerk()


@router.post("/", response_model=UserCreate)
async def create_user(
    userdata: TranscriptedUser,
    db: AsyncSession = Depends(get_db)
):
    try:
        user_id = userdata.user_id
        username = userdata.username
        email = userdata.email

        new_user = User(id=user_id, username=username, email=email)
        db.add(new_user)
        await db.commit()

        return HTTPException(status_code=204)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
