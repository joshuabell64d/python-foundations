import os
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Default to local SQLite database if DATABASE_URL isn't set
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./enterprise_risk.db"
)

# SQLite requires 'check_same_thread: False'. Postgres does not use this connect_args setting.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


def get_db() -> Generator:
    """Dependency that yields a database session per request and closes it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()