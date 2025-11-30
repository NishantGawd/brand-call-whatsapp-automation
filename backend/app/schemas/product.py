# app/schemas/product.py

from typing import Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., examples=["Men Formal Shirt"])
    category: Optional[str] = Field(None, examples=["Shirt"])
    gender: Optional[str] = Field(None, examples=["Men"])
    tags: Optional[str] = Field(
        None, examples=["men,shirt,formal"]
    )  # simple CSV, can refine later

    price: Optional[float] = Field(None, examples=[799.0])
    description: Optional[str] = Field(
        None,
        examples=["High-quality cotton formal shirt"],
    )
    image_url: Optional[str] = Field(
        None,
        examples=["https://example.com/images/men-shirt-1.jpg"],
    )
    is_active: Optional[bool] = True


class ProductCreate(ProductBase):
    """Payload for creating a product."""
    pass


class ProductUpdate(BaseModel):
    """Payload for updating a product (all fields optional)."""

    name: Optional[str] = None
    category: Optional[str] = None
    gender: Optional[str] = None
    tags: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class ProductInDBBase(ProductBase):
    id: int
    tenant_id: int

    class Config:
        orm_mode = True


class Product(ProductInDBBase):
    """Response model."""
    pass
