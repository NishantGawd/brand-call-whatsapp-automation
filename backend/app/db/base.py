# Import all models here so Alembic can autogenerate migrations
from app.db.base_class import Base  # noqa: F401

from app.models.tenant import Tenant  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.product import Product  # noqa
from app.models.automation_settings import AutomationSettings
from app.models.call import Call
from app.models.webhook_call import WebhookCall
from app.models.tenant_settings import TenantSettings
