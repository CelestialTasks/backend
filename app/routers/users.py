from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth import data_from_user
from app.database import get_db
from app.models import User
from app.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserCreate)
async def create_user(
    userdata: data_from_user,
    db: AsyncSession = Depends(get_db)
):
    try:
        clerk_id = userdata.clerk_id
        username = userdata.username
        email = userdata.email

        new_user = User(clerk_id=clerk_id, username=username, email=email)
        db.add(new_user)
        await db.commit()

        return HTTPException(status_code=204)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
