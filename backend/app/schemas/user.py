from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    role: str | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    role: str | None = "owner"
    tenant_id: int


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: str | None = None
    is_active: bool | None = None


class UserInDBBase(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    tenant_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
