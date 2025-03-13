import os
from pathlib import Path
from typing import Annotated
import jwt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from pydantic import ValidationError

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
    try:
        user = UserBase.parse_obj(token_data)
    except ValidationError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"The token data is invalid: {exc.errors()}"
        )
    return user


data_from_user = Annotated[UserBase, Depends(decoder)]
