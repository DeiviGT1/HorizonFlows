# app/core/database.py
from sqlmodel import create_engine, Session, SQLModel

# ▼▼▼ CONFIGURACIÓN PARA POSTGRESQL ▼▼▼

# Datos de conexión. Reemplaza con tus valores.
DB_USER = "owner"  # El usuario que creaste en pgAdmin
DB_PASSWORD = "postgres"
DB_HOST = "localhost" # 👈 ¡La IP local de tu máquina servidor!
DB_PORT = "5432" # Puerto por defecto de PostgreSQL
DB_NAME = "pos_tienda" # La base de datos que creaste

# Construye la URL de conexión
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """
    Para PostgreSQL, la base de datos ya debe existir.
    Esta función solo creará las tablas dentro de esa base de datos.
    """
    print("Verificando y creando tablas en la base de datos existente...")
    from app import models # Asegura que todos los modelos se carguen
    SQLModel.metadata.create_all(engine)
    print("¡Tablas creadas/verificadas con éxito!")