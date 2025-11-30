# app/api/v1/endpoints/products.py

from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_active_user
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.crud.crud_product import crud_product

router = APIRouter()


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a product for the current tenant.
    """
    product = crud_product.create_with_tenant(
        db,
        tenant_id=current_user.tenant_id,
        obj_in=product_in,
    )
    return product


@router.get("/", response_model=List[Product])
def list_products(
    skip: int = 0,
    limit: int = Query(100, le=1000),
    category: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    List products for the current tenant.

    Optional filters:
    - category: e.g. "Shirt"
    - gender: e.g. "Men"
    - (is_active default True)
    """
    products = crud_product.get_multi_by_tenant(
        db,
        tenant_id=current_user.tenant_id,
        skip=skip,
        limit=limit,
        category=category,
        gender=gender,
        is_active=True,
    )
    return products


@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get a single product by ID (scoped to current tenant).
    """
    product = crud_product.get(
        db,
        tenant_id=current_user.tenant_id,
        product_id=product_id,
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update a product (only fields provided are changed).
    """
    product = crud_product.get(
        db,
        tenant_id=current_user.tenant_id,
        product_id=product_id,
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product = crud_product.update(
        db,
        db_obj=product,
        obj_in=product_in,
    )
    return product


@router.delete("/{product_id}", response_model=Product)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Delete a product for the current tenant.
    """
    product = crud_product.remove(
        db,
        tenant_id=current_user.tenant_id,
        product_id=product_id,
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
