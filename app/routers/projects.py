from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ProjectCreate
from app.models import User
from app.services.auth import data_from_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", status_code=204)
def create_project(
        userdata: data_from_user,
        project_data: ProjectCreate,
        db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == userdata.user_id).all()
    print(user)

# here I am trying to understand how to implement the relationship
# between the project and the user before the project is created, in
# order to implement the many to many relationship
