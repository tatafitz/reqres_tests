from fastapi import APIRouter

from app.database.engine import check_availability
from app.models.app_status import AppStatus

router = APIRouter()

@router.get("/")
def root():
    return {"message": "API is running"}

@router.get("/status", response_model=AppStatus)
def status():
    check_availability()
    return AppStatus(database=check_availability())