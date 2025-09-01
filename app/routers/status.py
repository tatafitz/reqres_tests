from fastapi import APIRouter

from app.data import users_db
from app.database.engine import check_availability
from app.models.users import ConnectionStatus

router = APIRouter()

@router.get("/status", response_model=ConnectionStatus)
def status():
    check_availability()
    return ConnectionStatus(database=True)

# @router.get("/")
# def root():
#     return {"message": "API is running"}