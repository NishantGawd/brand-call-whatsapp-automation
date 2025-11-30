# app/api/v1/endpoints/webhooks_calls.py

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import logging

from app.core.deps import get_db, get_current_active_user
from app.schemas.webhook import WebhookCallRequest
from app.models.webhook_call import WebhookCall
from app.models.tenant_settings import TenantSettings
from app.models.tenant import Tenant
from app.services.automation_service import handle_call_automation

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/calls/{tenant_slug}", status_code=status.HTTP_200_OK)
def receive_call_webhook(
    tenant_slug: str,
    payload: WebhookCallRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Receive normalized call event and decide whether to trigger automation.

    Steps:
    1. Resolve tenant from slug and check access.
    2. Load tenant automation settings.
    3. Save call into WebhookCall table.
    4. Evaluate automation conditions.
    5. If conditions pass, enqueue WhatsApp send via Celery.
    """
    logger.info("📥 Incoming call webhook for %s: %s", tenant_slug, payload.json())

    # 1) Resolve tenant from slug & check that the current user belongs to it
    tenant: Tenant | None = (
        db.query(Tenant)
        .filter(Tenant.slug == tenant_slug)
        .first()
    )
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found.",
        )

    if tenant.id != getattr(current_user, "tenant_id", None):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed for this tenant.",
        )

    # 2) Load tenant settings
    settings: TenantSettings | None = (
        db.query(TenantSettings)
        .filter(TenantSettings.tenant_id == tenant.id)
        .first()
    )
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant settings not configured.",
        )

    logger.debug("Tenant %s settings: %s", tenant.id, settings)

    # 3) Persist call in DB
    call = WebhookCall(
        caller_number=payload.from_number,
        call_status=payload.status,
        call_duration_seconds=int(payload.duration_seconds or 0),
        tenant_id=tenant.id,
    )
    db.add(call)
    db.commit()
    db.refresh(call)

    logger.info("📞 Call saved with ID=%s", getattr(call, "id", None))

    # Convert ORM attributes to plain Python types
    call_id: int = int(getattr(call, "id", 0) or 0)
    call_duration_seconds: int = int(
        getattr(call, "call_duration_seconds", 0) or 0
    )

    # 4) Evaluate automation conditions
    min_duration: int = int(
        getattr(settings, "min_call_duration_seconds", 0) or 0
    )
    duration_valid: bool = call_duration_seconds >= min_duration
    status_valid: bool = payload.status.lower() in {"completed", "answered", "done"}
    settings_enabled: bool = bool(getattr(settings, "enabled", False))

    logger.debug(
        "🔍 Conditions → enabled=%s, duration_valid=%s, status_valid=%s "
        "(min_duration=%s, call_duration=%s)",
        settings_enabled,
        duration_valid,
        status_valid,
        min_duration,
        call_duration_seconds,
    )

    if not (settings_enabled and duration_valid and status_valid):
        logger.info("❌ Automation conditions NOT met for call ID=%s", call_id)
        return {
            "message": "Webhook processed, no automation triggered",
            "call_id": call_id,
            "automation_triggered": False,
        }

    # Optional: mark on the ORM object (not persisted if no column exists)
    setattr(call, "should_trigger_automation", True)
    logger.info("⚡ Automation WILL be triggered for call ID=%s", call_id)

    # 5) Build WhatsApp recipient number
    # Prefer customer_number, fall back to from_number
    raw_to_number = payload.customer_number or payload.from_number
    to_number: str = str(raw_to_number)
    if to_number and not to_number.startswith("whatsapp:"):
        to_number = f"whatsapp:{to_number}"

    logger.debug("📤 Formatted WhatsApp number: %s", to_number)

    # 6) Trigger automation task via Celery
    try:
        tenant_id_int = int(getattr(tenant, "id", 0) or 0)

        automation_result = handle_call_automation(
            tenant_id=tenant_id_int,    # ✅ pass plain int ID
            call_id=call_id,
            to_number=to_number,
        )
        logger.info("🎯 Automation queued: %s", automation_result)
    except Exception as exc:
        logger.exception("🔥 Error triggering automation for call ID=%s", call_id)
        raise HTTPException(
            status_code=500,
            detail=f"Automation error: {exc}",
        )

    return {
        "message": "Webhook processed successfully",
        "call_id": call_id,
        "automation_triggered": True,
        "task": automation_result,
    }
