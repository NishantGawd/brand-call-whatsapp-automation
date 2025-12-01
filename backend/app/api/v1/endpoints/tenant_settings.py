# NEW FILE - API endpoints for tenant settings management
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, cast

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.tenant_settings import TenantSettings
from app.schemas.tenant_settings import (
    TenantSettingsResponse,
    TenantSettingsUpdate,
    TenantSettingsPublic,
    WhatsAppCredentialsUpdate,
    WebhookSecurityUpdate
)
from app.services.whatsapp_client import WhatsAppCloudAPIClient

router = APIRouter()


@router.get("/", response_model=TenantSettingsPublic)
async def get_tenant_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current tenant settings (hides sensitive data)"""
    settings = db.query(TenantSettings).filter(
        TenantSettings.tenant_id == cast(int, current_user.tenant_id)
    ).first()

    if not settings:
        # Create default settings
        settings = TenantSettings(tenant_id=cast(int, current_user.tenant_id))
        db.add(settings)
        db.commit()
        db.refresh(settings)

    # Convert to public response (hide tokens)
    return TenantSettingsPublic(
        id=cast(int, settings.id),
        tenant_id=cast(int, settings.tenant_id),
        thank_you_message=cast(str, settings.thank_you_message),
        include_catalog=cast(bool, settings.include_catalog),
        catalog_header_message=cast(str, settings.catalog_header_message),
        catalog_footer_message=cast(str, settings.catalog_footer_message),
        message_delay_seconds=cast(int, settings.message_delay_seconds),
        is_whatsapp_configured=cast(bool, settings.is_whatsapp_configured),
        has_webhook_secret=bool(cast(Optional[str], settings.webhook_secret_key)),
        is_active=cast(bool, settings.is_active)
    )


@router.put("/", response_model=TenantSettingsPublic)
async def update_tenant_settings(
    settings_update: TenantSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update message templates and automation settings"""
    settings = db.query(TenantSettings).filter(
        TenantSettings.tenant_id == cast(int, current_user.tenant_id)
    ).first()

    if not settings:
        settings = TenantSettings(tenant_id=cast(int, current_user.tenant_id))
        db.add(settings)

    # Update fields
    for field, value in settings_update.dict(exclude_unset=True).items():
        setattr(settings, field, value)

    db.commit()
    db.refresh(settings)

    return TenantSettingsPublic(
        id=cast(int, settings.id),
        tenant_id=cast(int, settings.tenant_id),
        thank_you_message=cast(str, settings.thank_you_message),
        include_catalog=cast(bool, settings.include_catalog),
        catalog_header_message=cast(str, settings.catalog_header_message),
        catalog_footer_message=cast(str, settings.catalog_footer_message),
        message_delay_seconds=cast(int, settings.message_delay_seconds),
        is_whatsapp_configured=cast(bool, settings.is_whatsapp_configured),
        has_webhook_secret=bool(cast(Optional[str], settings.webhook_secret_key)),
        is_active=cast(bool, settings.is_active)
    )


@router.post("/whatsapp-credentials")
async def update_whatsapp_credentials(
    credentials: WhatsAppCredentialsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update WhatsApp Cloud API credentials"""
    settings = db.query(TenantSettings).filter(
        TenantSettings.tenant_id == cast(int, current_user.tenant_id)
    ).first()

    if not settings:
        settings = TenantSettings(tenant_id=cast(int, current_user.tenant_id))
        db.add(settings)

    # Verify credentials before saving
    client = WhatsAppCloudAPIClient(
        phone_number_id=credentials.whatsapp_phone_number_id,
        access_token=credentials.whatsapp_access_token,
        business_account_id=credentials.whatsapp_business_account_id
    )

    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        health_check = loop.run_until_complete(client.check_health())
    finally:
        loop.close()

    if not health_check.get("success"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid WhatsApp credentials: {health_check.get('error')}"
        )

    # Save credentials
    setattr(settings, "whatsapp_phone_number_id", credentials.whatsapp_phone_number_id)
    setattr(settings, "whatsapp_business_account_id", credentials.whatsapp_business_account_id)
    setattr(settings, "whatsapp_access_token", credentials.whatsapp_access_token)
    setattr(settings, "whatsapp_webhook_verify_token", credentials.whatsapp_webhook_verify_token)
    setattr(settings, "is_whatsapp_configured", True)

    db.commit()

    return {
        "success": True,
        "message": "WhatsApp credentials saved and verified"
    }


@router.post("/webhook-secret")
async def generate_webhook_secret(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a new webhook secret key"""
    import secrets

    settings = db.query(TenantSettings).filter(
        TenantSettings.tenant_id == cast(int, current_user.tenant_id)
    ).first()

    if not settings:
        settings = TenantSettings(tenant_id=cast(int, current_user.tenant_id))
        db.add(settings)

    # Generate new secret
    setattr(settings, "webhook_secret_key", secrets.token_urlsafe(32))
    db.commit()

    return {
        "success": True,
        "webhook_secret": cast(str, settings.webhook_secret_key),
        "message": "Save this secret - it won't be shown again. Add it to your telephony webhook URL."
    }


@router.post("/test-whatsapp")
async def test_whatsapp_connection(
    phone_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a test WhatsApp message to verify setup"""
    settings = db.query(TenantSettings).filter(
        TenantSettings.tenant_id == cast(int, current_user.tenant_id)
    ).first()

    if not settings or not cast(bool, settings.is_whatsapp_configured):
        raise HTTPException(status_code=400, detail="WhatsApp not configured")

    client = WhatsAppCloudAPIClient(
        phone_number_id=cast(str, settings.whatsapp_phone_number_id),
        access_token=cast(str, settings.whatsapp_access_token)
    )

    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        result = loop.run_until_complete(
            client.send_text_message(
                to_phone=phone_number,
                message="🎉 Test message from WhatsApp Automation System! Your configuration is working correctly."
            )
        )
    finally:
        loop.close()

    if result.get("success"):
        return {
            "success": True,
            "message_id": result.get("message_id"),
            "message": f"Test message sent to {phone_number}"
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to send test message: {result.get('error_message')}"
        )


@router.post("/toggle-automation")
async def toggle_automation(
    enabled: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Enable or disable automation"""
    settings = db.query(TenantSettings).filter(
        TenantSettings.tenant_id == cast(int, current_user.tenant_id)
    ).first()

    if not settings:
        raise HTTPException(status_code=400, detail="Settings not configured")

    setattr(settings, "is_active", enabled)
    db.commit()

    return {
        "success": True,
        "is_active": cast(bool, settings.is_active),
        "message": f"Automation {'enabled' if enabled else 'disabled'}"
    }
