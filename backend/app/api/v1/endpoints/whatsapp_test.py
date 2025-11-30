# app/api/v1/endpoints/whatsapp_test.py

from fastapi import APIRouter
from app.core.celery_app import celery_app
from app.schemas.whatsapp import WhatsAppTestRequest
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post("/test", summary="Send WhatsApp test message using Celery")
def send_test_whatsapp(payload: WhatsAppTestRequest):
    """
    Enqueue a WhatsApp test message via Celery.
    """
    # Using send_task to avoid direct function reference issues
    celery_app.send_task(
        "whatsapp.send_text",
        kwargs={
            "to": payload.to,
            "body": payload.body,
            "access_token": settings.WHATSAPP_DEFAULT_ACCESS_TOKEN or None,
            "phone_number_id": settings.WHATSAPP_DEFAULT_PHONE_NUMBER_ID or None,
        }
    )
    return {"status": "queued", "message": "WhatsApp send job queued via Celery."}
