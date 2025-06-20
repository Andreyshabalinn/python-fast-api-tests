from http import HTTPStatus
from fastapi import APIRouter
from app.database.engine import check_availability

from app.models.AppStatus import AppStatus
# from app.database import users_db

router = APIRouter()


@router.get("/api/healthcheck", status_code=HTTPStatus.OK)
def healthcheck()->AppStatus:
    
    return AppStatus(database=check_availability())