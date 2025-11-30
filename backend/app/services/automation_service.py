from __future__ import annotations

from typing import cast,Any, List
import logging

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.webhook_call import WebhookCall
from app.models.product import Product
from app.models.tenant_settings import TenantSettings
from app.tasks.whatsapp_tasks import send_whatsapp_text_task

logger = logging.getLogger(__name__)


def handle_call_automation(
    tenant_id: int,
    call_id: int,
    to_number: str,
) -> dict[str, Any]:
    """
    High-level automation handler called from the webhook endpoint.

    Steps:
    1. Load the WebhookCall record for this tenant & call_id.
    2. Check tenant automation settings (enabled + min duration).
    3. Select a small set of “top” products to recommend.
    4. Build a WhatsApp text message with these products.
    5. Enqueue a Celery task to send the WhatsApp message.

    Returns a small dict with information about the enqueued task
    (or why it was skipped).
    """

    db: Session = SessionLocal()
    try:
        # 1) Load call
        call: WebhookCall | None = (
            db.query(WebhookCall)
            .filter(
                WebhookCall.id == call_id,
                WebhookCall.tenant_id == tenant_id,
            )
            .first()
        )
        if not call:
            logger.warning(
                "handle_call_automation: no call found (tenant_id=%s, call_id=%s)",
                tenant_id,
                call_id,
            )
            return {"error": "call_not_found"}

        # 2) Load tenant settings
        settings: TenantSettings | None = (
            db.query(TenantSettings)
            .filter(TenantSettings.tenant_id == tenant_id)
            .first()
        )
        if not settings:
            logger.warning(
                "handle_call_automation: no tenant settings found (tenant_id=%s)",
                tenant_id,
            )
            return {"error": "tenant_settings_not_found"}

        enabled: bool = bool(getattr(settings, "enabled", False))
        if not enabled:
            logger.info(
                "handle_call_automation: automation disabled for tenant_id=%s",
                tenant_id,
            )
            return {"skipped": "automation_disabled"}

        min_duration: int = int(
            getattr(settings, "min_call_duration_seconds", 0) or 0
        )
        call_duration: int = int(
            getattr(call, "call_duration_seconds", 0) or 0
        )

        if call_duration < min_duration:
            logger.info(
                "handle_call_automation: call too short for automation "
                "(tenant_id=%s, call_id=%s, duration=%s, min=%s)",
                tenant_id,
                call_id,
                call_duration,
                min_duration,
            )
            return {"skipped": "call_duration_too_short"}

        # 3) Pick some products to recommend
        products: List[Product] = (
            db.query(Product)
            .filter(
                Product.tenant_id == tenant_id,
                Product.is_active.is_(True),
            )
            .order_by(Product.id.asc())
            .limit(3)
            .all()
        )

        # 4) Build WhatsApp message
        lines: list[str] = []
        lines.append("Thank you for calling us! 🙏")
        lines.append("Here are some of our popular items:")

        if not products:
            lines.append("")
            lines.append(
                "Our team will send you the full catalogue shortly."
            )
        else:
            for idx, p in enumerate(products, start=1):
                name = str(getattr(p, "name", "") or "")
                category = str(getattr(p, "category", "") or "")
                # Use getattr to avoid static-type complaints about Column[Decimal]
                price_value = float(getattr(p, "price", 0) or 0)
                lines.append(
                    f"{idx}. {name} ({category}) – ₹{price_value:,.2f}"
                )

            lines.append("")
            lines.append(
                "Reply with the product number if you'd like more details or photos."
            )

        message: str = "\n".join(lines)

        # Ensure WhatsApp format for the number
        to_formatted = to_number
        if to_formatted and not to_formatted.startswith("whatsapp:"):
            to_formatted = f"whatsapp:{to_formatted}"

        # 5) Queue Celery task
        async_result = cast(Any,send_whatsapp_text_task.delay)(
            to=to_formatted,
            body=message,
            access_token=None,        # real values wired later from env / settings
            phone_number_id=None,
        )

        logger.info(
            "handle_call_automation: Celery task enqueued "
            "(tenant_id=%s, call_id=%s, task_id=%s, to=%s)",
            tenant_id,
            call_id,
            async_result.id,
            to_formatted,
        )

        return {
            "task_id": async_result.id,
            "to": to_formatted,
            "preview": message[:200],
        }

    finally:
        db.close()
