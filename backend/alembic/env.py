# backend/alembic/env.py
from dotenv import load_dotenv
load_dotenv()
from app.models.business import Business

from logging.config import fileConfig
import os

from alembic import context
from sqlmodel import SQLModel
# 👇 Changed 'get_engine' to 'MASTER_ENGINE'
from app.core.db import MASTER_ENGINE
# This import is essential for autogenerate to find your models
from app import models

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# 👇 Use your models' metadata as the target
target_metadata = SQLModel.metadata
Business.metadata.schema = "public"

def run_migrations_offline():
    # This part is mostly for offline generation, we can leave it as is
    # but it's good practice to ensure it's correct.
    url = os.getenv("DATABASE_URL", MASTER_ENGINE.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # 👇 Use the imported MASTER_ENGINE
    with MASTER_ENGINE.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()