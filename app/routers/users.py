from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.services.auth import data_from_user
from app.database import get_db
from app.models import User
from app.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserCreate)
def create_user(
    userdata: data_from_user,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.clerk_id == userdata.clerk_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        clerk_id=userdata.clerk_id,
        username=userdata.username,
        email=userdata.email
    )

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists")

    return new_user
