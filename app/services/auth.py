from typing import Annotated
import jwt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError

from app.schemas import UserBase

CLERK_PUBLIC_KEY = "pk_test_b3Blbi15YWstODguY2xlcmsuYWNjb3VudHMuZGV2JA"
ALGORITHM = "RS256"

security = HTTPBearer()


def decoder(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserBase:
    token = credentials.credentials
    try:
        token_data = jwt.decode(token, CLERK_PUBLIC_KEY, algorithms=ALGORITHM)
    except PyJWTError:
        raise HTTPException(
            status_code=403,
            detail="Токен не проходит декодирование или он не из сервиса Clerk"
        )
    user_data = {"email": token_data.get("email"),
                 "clerk_id": token_data.get("user_id"),
                 "username": token_data.get("username"),
                 }
    if not all(user_data.values()):
        raise HTTPException(
            status_code=400,
            detail=f"Данные из токена не корректные, отсутствуют"
                   " некоторые поля, токен может быть подделан"
        )
    return UserBase(**user_data)


data_from_user = Annotated[UserBase, Depends(decoder)]
