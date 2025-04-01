from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserList
from app.services.auth import data_from_user

router = APIRouter(prefix="/users", tags=["users"])


# TODO: why we need return UserCreate
@router.post("/", response_model=UserCreate)
def create_user(userdata: data_from_user, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.clerk_id == userdata.user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        clerk_id=userdata.user_id, username=userdata.username, email=userdata.email
    )

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists")

    return new_user


@router.get("/", response_model=list[UserList])
def list_user(keyword: str = Query("", alias="search"), db: Session = Depends(get_db)):
    return db.query(User).filter(User.username.ilike(f"%{keyword}%")).all()
