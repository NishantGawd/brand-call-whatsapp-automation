import json
from typing import List

from sqlalchemy.orm import Session

from app.models.call import Call
from app.schemas.call import CallWebhookIn


class CRUDCall:
    def list_for_tenant(self, db: Session, *, tenant_id: int) -> List[Call]:
        return (
            db.query(Call)
            .filter(Call.tenant_id == tenant_id)
            .order_by(Call.created_at.desc())
            .all()
        )

    def create_from_webhook(
        self,
        db: Session,
        *,
        tenant_id: int,
        data: CallWebhookIn,
        should_trigger_automation: bool,
    ) -> Call:
        raw_payload_str = (
            json.dumps(data.raw_payload) if data.raw_payload is not None else None
        )

        db_obj = Call(
            tenant_id=tenant_id,
            direction=data.direction,
            from_number=data.from_number,
            to_number=data.to_number,
            customer_number=data.customer_number,
            status=data.status,
            provider=data.provider,
            provider_call_id=data.provider_call_id,
            duration_seconds=data.duration_seconds,
            started_at=data.started_at,
            ended_at=data.ended_at,
            raw_payload=raw_payload_str,
            should_trigger_automation=should_trigger_automation,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


call_crud = CRUDCall()
