import dotenv
from pathlib import Path

# # Загружаем переменные окружения из .env
# env_path = Path(__file__).parent.parent / ".env"
# dotenv.load_dotenv(env_path)
dotenv.load_dotenv()

import sys
import os


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.routers import status, users
import uvicorn
from app.database.engine import create_db_and_tables
app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)
add_pagination(app)



if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run("app.main:app", host="localhost", port=8002)