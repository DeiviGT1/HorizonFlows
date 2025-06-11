# backend/app/__init__.py

from app.core.db import MASTER_ENGINE
from app.models import *

def run():
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=MASTER_ENGINE)
    print("✔ Tables created")

if __name__ == "__main__":
    run()