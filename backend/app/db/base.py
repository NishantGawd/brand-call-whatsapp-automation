# Import all models here so Alembic can autogenerate migrations
from app.db.base_class import Base  # noqa: F401

from app.models.tenant import Tenant  # noqa: F401
from app.models.user import User  # noqa: F401
