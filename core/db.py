from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Use MySQL if provided, else fallback to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///smart_scheduler.db")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)

Base = declarative_base()


def init_db():
    """Create all tables"""
    from . import models  # noqa
    Base.metadata.create_all(bind=engine)
