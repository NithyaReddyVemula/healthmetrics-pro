import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.environ["DATABASE_URL"]
USE_SQLITE = DATABASE_URL.startswith("sqlite")

engine_kwargs = {"pool_pre_ping": True} if not USE_SQLITE else {}
engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def apply_sqlite_patch():
    """Patch table names for SQLite compatibility (schemas not supported)."""
    if USE_SQLITE:
        for _table in Base.metadata.tables.values():
            if _table.schema:
                _table.name = f"{_table.schema}.{_table.name}"
                _table.schema = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
