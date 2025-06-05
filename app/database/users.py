from fastapi import HTTPException
from typing import Iterable
from sqlmodel import Session, select
from .engine import engine
from ..models.test_user import User

def get_user(user_id: int) -> User | None:
    with Session(engine) as session:
        return session.get(User, user_id)


def get_users()-> Iterable[User]:
    with Session(engine) as session:
        statement = select(User)
        return session.exec(statement).all()


def create_user(user: User)->User:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        print("Пользователь успешно создан")
        return user

def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()

def update_user(user_id: int, user_data: User) -> User | None:
    with Session(engine) as session:
        user_db = session.get(User, user_id)
        if not user_db:
            raise HTTPException(status_code=404, detail="User not found")
        updates = user_data.model_dump(exclude_unset=True)
        user_db.sqlmodel_update(updates)

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db


