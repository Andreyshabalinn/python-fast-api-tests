
from pydantic import BaseModel, EmailStr, HttpUrl
from fastapi_pagination import Page, paginate

class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl