from http import HTTPStatus
import json
from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, paginate
from fastapi_pagination import add_pagination

from models.test_user import User
from models.AppStatus import AppStatus

app = FastAPI()

# Мок-данные
users: list[User] = None

with open("test_users.json") as f:
    users = json.load(f)

@app.get("/api/healthcheck", status_code=HTTPStatus.OK)
def healthcheck()->AppStatus:
    return AppStatus(users=bool(users))

@app.get("/api/users", response_model=Page[User])
def get_users(page: int = 1)-> list[User]:
    return paginate(users)

@app.get("/api/users/{user_id}")
def get_user_by_id(user_id: int) -> User:
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/api/users", status_code=201)
async def create_user(user: User):
    return user


add_pagination(app)