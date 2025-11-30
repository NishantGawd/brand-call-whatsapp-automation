from typing import Optional

from sqlalchemy.orm import Session

from app.models.automation_settings import AutomationSettings
from app.schemas.automation_settings import (
    AutomationSettingsCreate,
    AutomationSettingsUpdate,
)


class CRUDAutomationSettings:
    def get_by_tenant(self, db: Session, *, tenant_id: int) -> Optional[AutomationSettings]:
        return (
            db.query(AutomationSettings)
            .filter(AutomationSettings.tenant_id == tenant_id)
            .first()
        )

    def create_for_tenant(
        self,
        db: Session,
        *,
        tenant_id: int,
        obj_in: Optional[AutomationSettingsCreate] = None,
    ) -> AutomationSettings:
        data = obj_in.dict() if obj_in is not None else {}
        db_obj = AutomationSettings(tenant_id=tenant_id, **data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_or_create_default_for_tenant(
        self,
        db: Session,
        *,
        tenant_id: int,
    ) -> AutomationSettings:
        settings = self.get_by_tenant(db, tenant_id=tenant_id)
        if settings is None:
            settings = self.create_for_tenant(
                db,
                tenant_id=tenant_id,
                obj_in=AutomationSettingsCreate(),  # defaults
            )
        return settings

    def update_for_tenant(
        self,
        db: Session,
        *,
        tenant_id: int,
        obj_in: AutomationSettingsUpdate,
    ) -> AutomationSettings:
        settings = self.get_or_create_default_for_tenant(db, tenant_id=tenant_id)
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(settings, field, value)
        db.add(settings)
        db.commit()
        db.refresh(settings)
        return settings


automation_settings = CRUDAutomationSettings()
