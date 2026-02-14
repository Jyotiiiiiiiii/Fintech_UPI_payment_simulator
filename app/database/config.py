from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Database URL
DATABASE_URL = "sqlite:///./upi_system.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
