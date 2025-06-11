# run_migrations.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlmodel import Session, select
from alembic.config import Config
from alembic import command

# Carga las variables de entorno (.env)
load_dotenv()

# Importaciones locales de tu app
from backend.app.models.business import Business
from backend.app.core.db import settings # Importa tu objeto settings

def upgrade_all_tenants():
    """
    Aplica las migraciones de Alembic a todas las bases de datos de los tenants.
    """
    master_url = settings.make_url(settings.postgres_db)
    master_engine = create_engine(master_url)

    # 1. Obtener la lista de todos los tenants de la BD maestra
    with Session(master_engine) as session:
        tenants = session.exec(select(Business)).all()
        if not tenants:
            print("No se encontraron tenants.")
            return

    # 2. Configurar Alembic una vez
    alembic_cfg = Config("alembic.ini")

    # 3. Iterar y aplicar migraciones a cada tenant
    for tenant in tenants:
        print(f">>> Migrando tenant: {tenant.name} (DB: {tenant.db_name})")
        tenant_url = settings.make_url(tenant.db_name)
        
        # Se establece dinámicamente la URL de la BD para esta ejecución de Alembic
        alembic_cfg.set_main_option("sqlalchemy.url", tenant_url)
        
        try:
            command.upgrade(alembic_cfg, "head")
            print(f"    ✅ Migración exitosa para {tenant.db_name}")
        except Exception as e:
            print(f"    ❌ Error al migrar {tenant.db_name}: {e}")

if __name__ == "__main__":
    upgrade_all_tenants()