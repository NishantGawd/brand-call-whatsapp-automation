from sqlalchemy.orm import Session
from app.db import base  # noqa: F401

def init_db(db: Session) -> None:
    """
    Initialize database with required tables.
    This is called on application startup.
    """
    # Tables are created automatically by SQLAlchemy
    # This function can be used for initial data seeding if needed
    pass
