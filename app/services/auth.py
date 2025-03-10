import os
from pathlib import Path
from typing import Annotated
import jwt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

from app.schemas import UserBase

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=dotenv_path)

CLERK_PUBLIC_KEY = os.getenv('CLERK_PUBLIC_KEY')
ALGORITHM = os.getenv('ALGORITHM')

security = HTTPBearer()


def decoder(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserBase:
    token = credentials.credentials
    try:
        token_data = jwt.decode(token, CLERK_PUBLIC_KEY, algorithms=ALGORITHM)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=403,
            detail="The token does not pass decoding or it is not from the Clerk service"
        )
    user_data = {"email": token_data.get("email"),
                 "clerk_id": token_data.get("user_id"),
                 "username": token_data.get("username"),
                 }
    if not all(user_data.values()):
        raise HTTPException(
            status_code=400,
            detail=f"The data from the token is incorrect,"
                   " some fields are missing, the token may be forged"
        )
    return UserBase(**user_data)


data_from_user = Annotated[UserBase, Depends(decoder)]
