# backend/app/routers/onboarding.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from pydantic import BaseModel
from app.core.db import get_master_session, MASTER_ENGINE, settings
from app.models import Business
from alembic.config import Config
from alembic import command
from app.core.auth import require_role

router = APIRouter(
    prefix="/onboarding",
    tags=["onboarding"],
    dependencies=[Depends(require_role("admin"))]
)

class BusinessCreate(BaseModel):
    name: str
    slug: str

@router.post("/register")
def register_business(business_data: BusinessCreate, session: Session = Depends(get_master_session)):
    db_name = f"tenant_{business_data.slug.lower().replace('-', '_')}"

    # 1. Crear el registro en la tabla Business
    business = Business(name=business_data.name, slug=business_data.slug, db_name=db_name)
    session.add(business)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="El nombre o slug de la empresa ya existe.")

    # 2. Crear la nueva Base de Datos para el tenant
    try:
        with MASTER_ENGINE.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
    except Exception as e:
        # Si falla, deberíamos borrar el registro de business que acabamos de crear (rollback)
        raise HTTPException(status_code=500, detail=f"No se pudo crear la base de datos: {e}")

    # 3. Aplicar migraciones a la nueva BD
    alembic_cfg = Config("alembic.ini") # Asegúrate que alembic.ini está en la raíz
    alembic_cfg.set_main_option("sqlalchemy.url", settings.make_url(db_name))
    command.upgrade(alembic_cfg, "head")

    session.refresh(business)
    return business