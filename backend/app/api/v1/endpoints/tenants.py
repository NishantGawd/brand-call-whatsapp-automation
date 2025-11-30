from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_dep
from app.models.tenant import Tenant as TenantModel
from app.schemas.tenant import Tenant, TenantCreate

router = APIRouter()


@router.post("/", response_model=Tenant, status_code=status.HTTP_201_CREATED)
def create_tenant(
    tenant_in: TenantCreate,
    db: Session = Depends(get_db_dep),
) -> TenantModel:
    existing = (
        db.query(TenantModel)
        .filter(
            (TenantModel.slug == tenant_in.slug)
            | (TenantModel.name == tenant_in.name)
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant with same name or slug already exists",
        )

    tenant = TenantModel(
        name=tenant_in.name,
        slug=tenant_in.slug,
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


@router.get("/", response_model=list[Tenant])
def list_tenants(
    db: Session = Depends(get_db_dep),
) -> list[TenantModel]:
    tenants = db.query(TenantModel).order_by(TenantModel.created_at.desc()).all()
    return tenants
