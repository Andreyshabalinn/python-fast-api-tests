import dotenv
dotenv.load_dotenv(encoding='utf-8')
from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, paginate
from fastapi_pagination import add_pagination
from app.models.test_user import User

from app.database.engine import create_db_and_tables


from app.routers import status, users



app = FastAPI()

app.include_router(status.router)
app.include_router(users.router, prefix="/api")
create_db_and_tables()
add_pagination(app)