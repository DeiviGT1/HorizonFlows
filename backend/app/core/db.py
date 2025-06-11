# backend/app/core/db.py

from contextvars import ContextVar
from functools import lru_cache
from typing import Generator
import os

from sqlmodel import Session, create_engine
from pydantic import BaseSettings

# --- Configuración de la Conexión ---
# (Tu clase Settings y la creación de la URL es correcta)
class Settings(BaseSettings):
    pg_host: str = "localhost"
    pg_port: int = 5432
    postgres_user: str
    postgres_password: str
    postgres_db: str # Esta será la BD maestra

    def make_url(self, db_name: str) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.pg_host}:{self.pg_port}/{db_name}"
        )

settings = Settings()

# --- Motor de la Base de Datos Maestra ---
# Conectará a la BD principal que tiene la tabla de empresas
MASTER_ENGINE = create_engine(settings.make_url(settings.postgres_db), pool_pre_ping=True)

def get_master_session() -> Generator[Session, None, None]:
    with Session(MASTER_ENGINE) as session:
        yield session

# --- Lógica de Conexión por Tenant ---
# ContextVar almacenará el motor del tenant actual para esta petición específica
_current_tenant_engine = ContextVar("current_tenant_engine")

@lru_cache(maxsize=128)
def get_tenant_engine(db_name: str):
    """
    Crea y cachea un motor de SQLAlchemy por cada tenant.
    """
    return create_engine(settings.make_url(db_name), pool_pre_ping=True)

def set_tenant(db_name: str) -> None:
    """
    Llamado por el middleware para establecer el motor del tenant actual.
    """
    engine = get_tenant_engine(db_name)
    _current_tenant_engine.set(engine)

def get_session() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI que provee una sesión al motor del tenant actual.
    """
    try:
        engine = _current_tenant_engine.get()
        with Session(engine) as session:
            yield session
    except LookupError:
        raise RuntimeError("No se ha establecido el tenant para esta petición.")