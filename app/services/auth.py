from typing import Annotated
from clerk_backend_api import Clerk

from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

from app.schemas import UserBase

HeaderBearerAccessTokenSchema = OAuth2PasswordBearer(tokenUrl='token')


def transcript_of_the_incoming_token(
        access_token_encoded: Annotated[str, Depends(HeaderBearerAccessTokenSchema)],
) -> str:
    return access_token_encoded


def extract_data_from_the_incoming_token(
    access_token_encoded: Annotated[str, Depends(transcript_of_the_incoming_token)]
) -> UserBase:
    with Clerk(bearer_auth=access_token_encoded) as clerk:
        user_data = clerk.users.get_user_from_token(access_token_encoded)

    return UserBase(
        user_id=user_data["user_id"],
        email=user_data["email"],
        username=user_data["username"]
    )

# async def get_user_by_access_token_decoded(
#     access_token_decoded: Annotated[UserBase, Depends(extract_access_token_decoded)]
# ) -> User:
#     # todo: get user from db
#     return await User.__tablename__.


TranscriptedUser = Annotated[UserBase, Depends(extract_data_from_the_incoming_token)]
