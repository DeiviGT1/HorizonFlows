"""
Gestión de motores multitenant p/ una DB por empresa
"""
from contextvars import ContextVar
from functools import lru_cache
from typing import Generator

from sqlmodel import SQLModel, Session, create_engine
from pydantic import BaseSettings

class Settings(BaseSettings):
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_user: str
    pg_password: str
    pg_master_db: str

    def make_url(self, db_name: str) -> str:
        return (
            f"postgresql+psycopg://{self.pg_user}:{self.pg_password}"
            f"@{self.pg_host}:{self.pg_port}/{db_name}"
        )

settings = Settings()

# ───────────────────────────────────────── master ────
MASTER_ENGINE = create_engine(settings.make_url(settings.pg_master_db), pool_pre_ping=True)

def get_master_session() -> Generator[Session, None, None]:
    with Session(MASTER_ENGINE) as session:
        yield session

# ───────────────────────────────────────── tenants ───
_current_engine: ContextVar[Session] = ContextVar("current_engine")

@lru_cache(maxsize=128)
def _tenant_engine(db_name: str):
    return create_engine(settings.make_url(db_name), pool_pre_ping=True)

def set_tenant(db_name: str) -> None:
    _current_engine.set(_tenant_engine(db_name))

def get_session() -> Generator[Session, None, None]:
    engine = _current_engine.get()
    with Session(engine) as session:
        yield session