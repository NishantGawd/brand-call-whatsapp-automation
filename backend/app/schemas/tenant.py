from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TenantBase(BaseModel):
    name: str
    slug: str


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    setup_complete: bool | None = None
    is_active: bool | None = None


class TenantInDBBase(TenantBase):
    id: int
    is_active: bool
    setup_complete: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Tenant(TenantInDBBase):
    pass


class TenantInDB(TenantInDBBase):
    pass
