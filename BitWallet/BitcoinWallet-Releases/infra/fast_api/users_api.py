from typing import Any
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from BitcoinWallet.core.errors import ExistsError
from BitcoinWallet.core.users import User
from BitcoinWallet.infra.fast_api.dependables import UserRepositoryDependable

user_api = APIRouter(tags=["Users"])


def extract_user_fields(user: User) -> dict[str, Any]:
    return {
        "API_key": user.API_key,
        "username": user.username,
        "password": user.password,
    }


class CreateUserRequest(BaseModel):
    username: str
    password: str


class UserItem(BaseModel):
    API_key: UUID
    username: str
    password: str


class UserItemEnvelope(BaseModel):
    user: UserItem


@user_api.post(
    "/users",
    status_code=201,
    response_model=UserItemEnvelope,
)
def create_user(
    request: CreateUserRequest, users: UserRepositoryDependable
) -> dict[str, Any] | JSONResponse:
    try:
        user = User(**request.model_dump())
        users.create(user)

        response_data = extract_user_fields(user)

        return {"user": response_data}
    except ExistsError:
        return JSONResponse(
            status_code=409,
            content={"message": "User already exists."},
        )
