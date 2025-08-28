from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# URL de la base de datos SQLite
SQLALCHEMY_DATABASE_URL = f"sqlite:///{settings.data_dir}/binance_logs.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Solo para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency para obtener sesión de BD"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crear todas las tablas"""
    Base.metadata.create_all(bind=engine)
