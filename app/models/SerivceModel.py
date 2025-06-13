from utils.base_session import BaseSession
from config import Server
from app.models.test_user import User, UserCreate, UserUpdate
from fastapi import APIRouter, HTTPException
from app.database import users
from fastapi_pagination import Page, paginate


class ServiceModel:
    def __init__(self, env):
        self.session = BaseSession(base_url=Server(env).service)

    def get_users(self, page, size):
        return self.session.get(f"users/?page={page}&size={size}")

    def get_user_id(self, user_id: int):
        return self.session.get(f"users/{user_id}")
        

    def create_user(self, user: UserCreate):
        return self.session.post(f"users", json=user)
        

    def update_user(self, user_id: int, user: UserUpdate):
        return self.session.patch(f"users/{user_id}", json=user)

    def delete_user(self, user_id: int):
        return self.session.delete(f"users/{user_id}")
