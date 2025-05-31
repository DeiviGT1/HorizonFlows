from sqlmodel import SQLModel, Session, create_engine
from functools import lru_cache
import os

@lru_cache
def get_engine():
    db_url = os.getenv("DATABASE_URL")
    return create_engine(db_url, echo=True)   # echo=True para ver SQL en logs

engine = get_engine()

def get_session():
    with Session(engine) as session:
        yield session