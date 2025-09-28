import dotenv

dotenv.load_dotenv()
import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.database.engine import create_db_and_tables
from app.routers import status, users

app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)
add_pagination(app)

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run("app.main:app", host="localhost", port=8002)
