from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError

from app.schemas import UserBase
from app.settings import settings

security = HTTPBearer()


def decoder(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserBase:
    token = credentials.credentials
    try:
        token_data = jwt.decode(
            token, settings.CLERK_PUBLIC_KEY, algorithms=settings.ALGORITHM
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=403,
            detail="The token does not pass decoding or it is not from the Clerk service",
        )
    try:
        user = UserBase.parse_obj(token_data)
    except ValidationError as exc:
        raise HTTPException(
            status_code=400, detail=f"The token data is invalid: {exc.errors()}"
        )
    return user


data_from_user = Annotated[UserBase, Depends(decoder)]
