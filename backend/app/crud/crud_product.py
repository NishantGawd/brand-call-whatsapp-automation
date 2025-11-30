# app/crud/crud_product.py

from typing import Optional, Sequence

from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct:
    def create_with_tenant(
        self,
        db: Session,
        *,
        tenant_id: int,
        obj_in: ProductCreate,
    ) -> Product:
        db_obj = Product(
            tenant_id=tenant_id,
            **obj_in.dict(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(
        self,
        db: Session,
        *,
        tenant_id: int,
        product_id: int,
    ) -> Optional[Product]:
        return (
            db.query(Product)
            .filter(
                Product.id == product_id,
                Product.tenant_id == tenant_id,
            )
            .first()
        )

    def get_multi_by_tenant(
        self,
        db: Session,
        *,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        gender: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> Sequence[Product]:
        query = db.query(Product).filter(Product.tenant_id == tenant_id)

        if category:
            # case-insensitive match
            query = query.filter(Product.category.ilike(category))

        if gender:
            query = query.filter(Product.gender.ilike(gender))

        if is_active is not None:
            query = query.filter(Product.is_active == is_active)

        return query.offset(skip).limit(limit).all()

    def update(
        self,
        db: Session,
        *,
        db_obj: Product,
        obj_in: ProductUpdate,
    ) -> Product:
        data = obj_in.dict(exclude_unset=True)
        for field, value in data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(
        self,
        db: Session,
        *,
        tenant_id: int,
        product_id: int,
    ) -> Optional[Product]:
        obj = self.get(db, tenant_id=tenant_id, product_id=product_id)
        if not obj:
            return None

        db.delete(obj)
        db.commit()
        return obj


crud_product = CRUDProduct()
