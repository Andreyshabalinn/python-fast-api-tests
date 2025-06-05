from http import HTTPStatus
from typing import Iterable
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate

from app.models.test_user import User, UserCreate, UserUpdate
from app.database import users

router = APIRouter(prefix="/users")


@router.get("/", response_model=Page[User])
def get_users(page: int = 1)-> Iterable[User]:
    return paginate(users.get_users())

@router.get("/{user_id}")
def get_user_by_id(user_id: int) -> User:
    user = users.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", status_code=201)
def create_user(user: User) -> User:
    UserCreate.model_validate(user.model_dump(mode="json"))
    return users.create_user(user)

@router.patch("/{user_id}", status_code=200)
def update_user(user_id: int, user: User) -> User:
    UserUpdate.model_validate(user.model_dump(mode="json"))
    return users.update_user(user_id, user)

@router.delete("/{user_id}", status_code=200)
def delete_user(user_id: int):
    users.delete_user(user_id)