import os

from sqlmodel import Session, SQLModel, create_engine, text

engine = create_engine(
    os.getenv("DATABASE_ENGINE"), pool_size=int(os.getenv("DATABASE_POOL_SIZE"))
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def check_availability():
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(e)
        return False
