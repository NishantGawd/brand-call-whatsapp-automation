from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, tenants, products, automation_settings, calls, webhooks_calls, whatsapp_test

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tenants.router, prefix="/internal/tenants", tags=["tenants"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(automation_settings.router, prefix="/automation-settings", tags=["automation-settings"],)
api_router.include_router(calls.router, prefix="/calls", tags=["calls"])
api_router.include_router(webhooks_calls.router, prefix="/webhooks/calls", tags=["webhooks-calls"],)
api_router.include_router(whatsapp_test.router, prefix="/whatsapp-test", tags=["whatsapp-test"])
