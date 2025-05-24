from fastapi import FastAPI, Request, HTTPException
from typing import Dict

app = FastAPI()

# Мок-данные
users = [
    {"id": 1, "first_name": "George"},
    {"id": 2, "first_name": "Janet"},
]

resources = [
    {"id": 2, "name": "fuchsia rose"},
]

@app.get("/api/users")
def get_users(page: int = 1):
    return {"data": users}

@app.get("/api/users/{user_id}")
def get_user_by_id(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return {"data": user}
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/api/unknown/{resource_id}")
def get_resource(resource_id: int):
    for res in resources:
        if res["id"] == resource_id:
            return {"data": res}
    raise HTTPException(status_code=404, detail="Resource not found")

@app.post("/api/users", status_code=201)
async def create_user(request: Request):
    user_data: Dict = await request.json()
    return user_data
