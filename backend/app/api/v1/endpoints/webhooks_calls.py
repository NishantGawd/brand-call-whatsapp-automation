# COMPLETE REWRITE - Removed JWT auth, added secret key verification
import hmac
import hashlib
import logging
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, Depends, Header, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.tenant import Tenant
from app.models.tenant_settings import TenantSettings
from app.models.call import Call
from app.models.webhook_call import WebhookCall
from app.schemas.webhook import CallEndedEvent, WebhookResponse
from app.tasks.whatsapp_tasks import process_call_ended_automation

logger = logging.getLogger(__name__)
router = APIRouter()


def verify_webhook_signature(
    payload: bytes,
    signature: str,
    secret_key: str,
    provider: str = "generic"
) -> bool:
    """Verify webhook signature from telephony provider"""
    if provider == "twilio":
        # Twilio uses HMAC-SHA1
        expected = hmac.new(
            secret_key.encode(),
            payload,
            hashlib.sha1
        ).hexdigest()
        return hmac.compare_digest(expected, signature)
    else:
        # Generic HMAC-SHA256
        expected = hmac.new(
            secret_key.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)


def normalize_call_status(status: str, provider: str) -> str:
    """Normalize call status from different providers"""
    status = status.lower()

    # Map to standard statuses
    if status in ["completed", "call-completed", "complete"]:
        return "completed"
    elif status in ["busy", "line-busy"]:
        return "busy"
    elif status in ["no-answer", "noanswer", "no_answer", "unanswered"]:
        return "no-answer"
    elif status in ["failed", "error", "call-failed"]:
        return "failed"
    elif status in ["canceled", "cancelled"]:
        return "canceled"
    else:
        return status


@router.post("/call-ended/{tenant_slug}", response_model=WebhookResponse)
async def handle_call_ended_webhook(
    tenant_slug: str,
    request: Request,
    db: Session = Depends(get_db),
    x_webhook_signature: Optional[str] = Header(None),
    x_twilio_signature: Optional[str] = Header(None),
    secret: Optional[str] = Query(None)  # Alternative: pass secret as query param
):
    """
    Webhook endpoint for telephony providers to notify when a call ends.

    This endpoint does NOT require JWT authentication.
    Security is handled via:
    1. Webhook signature verification (if configured)
    2. Secret key in query parameter (simpler alternative)
    3. Tenant slug validation
    """

    # Get tenant by slug
    tenant = db.query(Tenant).filter(
        Tenant.slug == tenant_slug,
        Tenant.is_active == True
    ).first()

    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # Get tenant settings
    settings = db.query(TenantSettings).filter(
        TenantSettings.tenant_id == tenant.id
    ).first()

    if not settings:
        raise HTTPException(status_code=400, detail="Tenant settings not configured")

    # Verify webhook authenticity
    signature = x_webhook_signature or x_twilio_signature

    if settings.webhook_secret_key:
        webhook_secret_key_str = str(settings.webhook_secret_key)

        # If secret key is configured, verify it
        if secret:
            # Simple query param verification
            if secret != webhook_secret_key_str:
                logger.warning(f"Invalid webhook secret for tenant {tenant_slug}")
                raise HTTPException(status_code=401, detail="Invalid webhook secret")
        elif signature:
            # Signature-based verification
            body = await request.body()
            provider = "twilio" if x_twilio_signature else "generic"
            if not verify_webhook_signature(body, signature, webhook_secret_key_str, provider):
                logger.warning(f"Invalid webhook signature for tenant {tenant_slug}")
                raise HTTPException(status_code=401, detail="Invalid webhook signature")
        else:
            logger.warning(f"No webhook authentication provided for tenant {tenant_slug}")
            raise HTTPException(status_code=401, detail="Webhook authentication required")

    # Parse webhook payload
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        payload = await request.json()
    elif "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        payload = dict(form_data)
    else:
        payload = await request.json()

    logger.info(f"Received webhook for tenant {tenant_slug}: {payload}")

    # Determine provider and extract data
    provider = "generic"
    caller_phone = ""
    receiver_phone = ""
    call_sid = ""
    call_status = ""
    duration = None

    # Twilio format
    if "CallSid" in payload and "AccountSid" in payload:
        provider = "twilio"
        call_sid = str(payload.get("CallSid", ""))
        caller_phone = str(payload.get("From", payload.get("Caller", "")))
        receiver_phone = str(payload.get("To", payload.get("Called", "")))
        call_status_raw = payload.get("CallStatus", "")
        call_status = str(call_status_raw) if call_status_raw else ""
        call_duration_raw = payload.get("CallDuration")
        if call_duration_raw and str(call_duration_raw).isdigit():
            duration = int(call_duration_raw)

    # Exotel format
    elif "CallSid" in payload and "Status" in payload:
        provider = "exotel"
        call_sid = str(payload.get("CallSid", ""))
        caller_phone = str(payload.get("From", payload.get("CallFrom", "")))
        receiver_phone = str(payload.get("To", payload.get("CallTo", "")))
        status_raw = payload.get("Status", "")
        call_status = str(status_raw) if status_raw else ""
        dial_duration_raw = payload.get("DialCallDuration")
        if dial_duration_raw and str(dial_duration_raw).isdigit():
            duration = int(dial_duration_raw)

    # Generic format
    else:
        call_sid = str(payload.get("call_id", payload.get("call_sid", str(datetime.utcnow().timestamp()))))
        caller_phone = str(payload.get("caller", payload.get("from", payload.get("caller_phone", ""))))
        receiver_phone = str(payload.get("receiver", payload.get("to", payload.get("receiver_phone", ""))))
        status_raw = payload.get("status", "completed")
        call_status = str(status_raw) if status_raw else "completed"
        duration_raw = payload.get("duration", payload.get("duration_seconds"))
        if duration_raw and str(duration_raw).isdigit():
            duration = int(duration_raw)

    # Normalize status
    normalized_status = normalize_call_status(call_status, provider)

    # Log the webhook call
    webhook_log = WebhookCall(
        tenant_id=tenant.id,
        provider=provider,
        call_sid=call_sid,
        caller_phone=caller_phone,
        receiver_phone=receiver_phone,
        status=normalized_status,
        raw_payload=payload
    )
    db.add(webhook_log)
    db.commit()

    # Create call record
    call = Call(
        tenant_id=tenant.id,
        caller_phone=caller_phone,
        receiver_phone=receiver_phone,
        call_sid=call_sid,
        status=normalized_status,
        duration_seconds=duration,
        provider=provider,
        ended_at=datetime.utcnow()
    )
    db.add(call)
    db.commit()
    db.refresh(call)

    call_id_int = int(call.id) if call.id else None

    # Trigger automation only for completed calls
    automation_triggered = False

    is_whatsapp_configured = bool(settings.is_whatsapp_configured)
    is_settings_active = bool(settings.is_active)

    if normalized_status == "completed" and caller_phone:
        if is_whatsapp_configured and is_settings_active:
            # Queue the automation task
            delay_seconds = settings.message_delay_seconds or 5

            process_call_ended_automation.apply_async(
                args=[tenant.id, call_id_int, caller_phone],
                countdown=delay_seconds
            )

            automation_triggered = True
            logger.info(f"Queued automation for call {call_id_int}, delay: {delay_seconds}s")
        else:
            logger.info(f"Automation not configured/enabled for tenant {tenant.id}")
    else:
        logger.info(f"Call status '{normalized_status}' - automation not triggered")

    return WebhookResponse(
        success=True,
        message=f"Webhook processed for {provider}",
        call_id=call_id_int,
        automation_triggered=automation_triggered
    )


@router.get("/test/{tenant_slug}")
async def test_webhook_endpoint(
    tenant_slug: str,
    db: Session = Depends(get_db)
):
    """Test endpoint to verify webhook URL is accessible"""
    tenant = db.query(Tenant).filter(Tenant.slug == tenant_slug).first()

    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    settings = db.query(TenantSettings).filter(
        TenantSettings.tenant_id == tenant.id
    ).first()

    return {
        "status": "ok",
        "tenant": tenant_slug,
        "whatsapp_configured": settings.is_whatsapp_configured if settings else False,
        "automation_active": settings.is_active if settings else False,
        "webhook_url": f"/api/v1/webhooks/call-ended/{tenant_slug}",
        "message": "Webhook endpoint is accessible. Configure your telephony provider to POST to this URL."
    }
