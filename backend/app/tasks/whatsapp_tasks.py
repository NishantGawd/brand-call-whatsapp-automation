# COMPLETE REWRITE - Proper Celery tasks with async support
import asyncio
import logging
from datetime import datetime
from celery import shared_task
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.services.automation_service import AutomationService

logger = logging.getLogger(__name__)


def get_db_session() -> Session:
    """Create a new database session for the task"""
    return SessionLocal()


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True
)
def process_call_ended_automation(
    self,
    tenant_id: int,
    call_id: int,
    caller_phone: str
):
    """
    Celery task to process post-call automation.
    Sends thank you message and catalog via WhatsApp.
    """
    logger.info(f"Processing automation for tenant {tenant_id}, call {call_id}, phone {caller_phone}")

    db = get_db_session()

    try:
        service = AutomationService(db=db, tenant_id=tenant_id)

        # Run the async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(
                service.send_post_call_messages(
                    caller_phone=caller_phone,
                    call_id=call_id
                )
            )
        finally:
            loop.close()

        if result.get("success"):
            logger.info(
                f"Automation completed for call {call_id}: "
                f"{result.get('messages_sent')} messages sent"
            )
        else:
            logger.error(f"Automation failed for call {call_id}: {result.get('errors')}")

            # Retry if there were errors
            if result.get("errors") and self.request.retries < self.max_retries:
                raise Exception(f"Automation errors: {result.get('errors')}")

        return result

    except Exception as e:
        logger.error(f"Task failed for call {call_id}: {str(e)}")
        raise

    finally:
        db.close()


@celery_app.task
def send_test_whatsapp_message(tenant_id: int, phone_number: str, message: str):
    """Send a test WhatsApp message to verify configuration"""
    logger.info(f"Sending test message for tenant {tenant_id} to {phone_number}")

    db = get_db_session()

    try:
        service = AutomationService(db=db, tenant_id=tenant_id)

        if not service.whatsapp_client:
            return {"success": False, "error": "WhatsApp not configured"}

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(
                service.whatsapp_client.send_text_message(
                    to_phone=phone_number,
                    message=message
                )
            )
        finally:
            loop.close()

        return result

    finally:
        db.close()


@celery_app.task
def retry_failed_messages(tenant_id: int | None = None):
    """Retry sending failed messages"""
    from app.models.message_log import MessageLog

    db = get_db_session()

    try:
        query = db.query(MessageLog).filter(
            MessageLog.status == "failed",
            MessageLog.retry_count < MessageLog.max_retries
        )

        if tenant_id is not None:
            query = query.filter(MessageLog.tenant_id == tenant_id)

        failed_messages = query.all()

        logger.info(f"Found {len(failed_messages)} failed messages to retry")

        for msg in failed_messages:
            # Queue retry
            process_call_ended_automation.apply_async(
                args=[msg.tenant_id, msg.call_id, msg.recipient_phone],
                countdown=10
            )

            msg.retry_count = int(msg.retry_count) + 1
            db.commit()

        return {"retried": len(failed_messages)}

    finally:
        db.close()
