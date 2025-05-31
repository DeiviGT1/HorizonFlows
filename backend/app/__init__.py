from app.core.db import engine
from app.models import *  # importa todos los modelos ya reexportados

def run():
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)
    print("✔ Tables created")

if __name__ == "__main__":
    run()