"""
Database connection
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..utils import get_settings

settings = get_settings()

if settings.DATABASE_URL is None:
    engine = create_engine(
        "sqlite://",
        connect_args={
            "check_same_thread": False},
        poolclass=StaticPool)
else:
    engine = create_engine(
        settings.DATABASE_URL, connect_args={
            "check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
