import os
import asyncio
from jose import jwt, JWTError
from clerk_backend_api import Clerk

from fastapi import APIRouter

from app.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["users"])

SECRET_KEY = '1'
ALGORITHM = 'HS256'


async def main():
    async with Clerk(
        bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
    ) as clerk:
        email = await clerk.email_addresses.get_async(email_address_id="email_address_id_example")

        assert email is not None


# POST /users/ – Create a user
@router.post("/", status_code=204)
async def create_user(user: UserCreate):
    try:
        payload = jwt.decode(user.token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        pass
