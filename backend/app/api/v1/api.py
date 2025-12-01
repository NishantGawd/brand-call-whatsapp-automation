# Updated to include new tenant_settings router
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    tenants,
    products,
    calls,
    webhooks_calls,
    automation_settings,
    tenant_settings,
)

api_router = APIRouter()

# Authentication
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Users
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Tenants
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])

# Products (Catalog)
api_router.include_router(products.router, prefix="/products", tags=["products"])

# Calls
api_router.include_router(calls.router, prefix="/calls", tags=["calls"])

# Automation Settings (legacy)
api_router.include_router(
    automation_settings.router,
    prefix="/automation-settings",
    tags=["automation"]
)

# Tenant Settings (new - includes WhatsApp config)
api_router.include_router(
    tenant_settings.router,
    prefix="/tenant-settings",
    tags=["tenant-settings"]
)

# Webhooks (NO AUTH REQUIRED - uses secret key verification)
api_router.include_router(
    webhooks_calls.router,
    prefix="/webhooks",
    tags=["webhooks"]
)
