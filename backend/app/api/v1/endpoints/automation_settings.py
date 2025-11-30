from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_active_user
from app.crud.crud_automation_settings import automation_settings
from app.schemas.automation_settings import (
    AutomationSettingsOut,
    AutomationSettingsUpdate,
)

router = APIRouter()


@router.get("/me", response_model=AutomationSettingsOut)
def get_my_automation_settings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Get automation settings for the current user's tenant.
    Creates default row if missing.
    """
    settings = automation_settings.get_or_create_default_for_tenant(
        db, tenant_id=current_user.tenant_id
    )
    return settings


@router.put("/me", response_model=AutomationSettingsOut)
def update_my_automation_settings(
    payload: AutomationSettingsUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update automation settings for the current user's tenant.
    """
    settings = automation_settings.update_for_tenant(
        db,
        tenant_id=current_user.tenant_id,
        obj_in=payload,
    )
    return settings
