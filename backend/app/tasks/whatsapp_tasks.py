from __future__ import annotations

from typing import Any, Optional
import logging

from celery import shared_task

from app.services.whatsapp_client import WhatsAppClient

logger = logging.getLogger(__name__)


@shared_task(name="whatsapp.send_text")
def send_whatsapp_text_task(
    to: str,
    body: str,
    access_token: Optional[str] = None,
    phone_number_id: Optional[str] = None,
) -> dict[str, Any]:
    """
    Celery task that actually sends a WhatsApp text message.

    - `to`  : full WhatsApp recipient, e.g. "whatsapp:+911234567890"
    - `body`: text of the message
    - `access_token` / `phone_number_id`:
        Optional overrides; if None, WhatsAppClient will fall back to
        environment / settings configuration.

    Returns a dict with either the HTTP API response or an error description.
    """

    logger.info("🔹 Celery Task Triggered → Sending WhatsApp: %s", to)

    client = WhatsAppClient(
        access_token=access_token,
        phone_number_id=phone_number_id,
    )

    try:
        result = client.send_text(to=to, body=body)
        logger.info("📩 WhatsApp Send Result → %s", result)
        return result
    except Exception as exc:
        logger.exception("Error sending WhatsApp message via Celery")
        return {"error": str(exc)}
