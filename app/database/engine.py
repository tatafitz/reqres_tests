import os

from sqlalchemy.orm import Session
from sqlmodel import create_engine, SQLModel, text

# Значения по умолчанию для базы данных
DEFAULT_DATABASE_ENGINE = "postgresql://postgres:example@localhost:5432/postgres"
DEFAULT_POOL_SIZE = 10

database_engine = os.getenv("DATABASE_ENGINE", DEFAULT_DATABASE_ENGINE)
# Безопасное получение pool_size с обработкой некорректных значений
try:
    pool_size_str = os.getenv("DATABASE_POOL_SIZE", str(DEFAULT_POOL_SIZE))
    # Убираем все нечисловые символы (например, %)
    pool_size_str = ''.join(filter(str.isdigit, pool_size_str))
    pool_size = int(pool_size_str) if pool_size_str else DEFAULT_POOL_SIZE
except (ValueError, TypeError):
    pool_size = DEFAULT_POOL_SIZE

engine = create_engine(database_engine, pool_size=pool_size)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def check_availability():
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(e)