from typing import Annotated
import jwt

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas import UserBase

CLERK_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA93k1cCpSyCAeS0RUok7v
B+wtLpCOO5fiUvXTDbq8yA9f5lPcaIREVfJlEEC90/RS6bXX4iZ8LB479zibfa4L
LYF/SoLpWvKAx6R4S7xv4xeKQ4Ri6cDfpU4nH5REzNLZm8WVDYAqmjM30arURz2+
DHs4A7yaqCAXhPaPAPneL0CQjE4b32DDvjXXcTHnjEDz71MWwjTM6BKfUOak4x3A
beqryGLNiq2ebM5nun1Dxb5hI//L3vMfLHn9xErkZiDxs8TrvpA03C2O7ERjGh1z
lrNVIGFNOn1cKTpzNkBWwZME/hinZn0ls/IMnfdJnd29Q7iDIn43BZPb+FiJUFK7
RwIDAQAB
-----END PUBLIC KEY-----
"""
ALGORITHM = "RS256"

security = HTTPBearer()


def decoder(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserBase:
    token = credentials.credentials
    try:
        token_data = jwt.decode(token, CLERK_PUBLIC_KEY, algorithms=ALGORITHM)
    except jwt.PyJWTError:
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
