from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, tenants

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tenants.router, prefix="/internal/tenants", tags=["tenants"])
