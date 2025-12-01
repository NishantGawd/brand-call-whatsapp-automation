# COMPLETE REWRITE - Proper automation flow with real credentials
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.tenant_settings import TenantSettings
from app.models.automation_settings import AutomationSettings
from app.models.product import Product
from app.models.call import Call
from app.models.message_log import MessageLog
from app.services.whatsapp_client import WhatsAppCloudAPIClient

logger = logging.getLogger(__name__)


class AutomationService:
    """Handles the complete post-call automation flow"""

    def __init__(self, db: Session, tenant_id: int):
        self.db = db
        self.tenant_id = tenant_id
        self._tenant_settings: Optional[TenantSettings] = None
        self._automation_settings: Optional[AutomationSettings] = None
        self._whatsapp_client: Optional[WhatsAppCloudAPIClient] = None

    @property
    def tenant_settings(self) -> Optional[TenantSettings]:
        if self._tenant_settings is None:
            self._tenant_settings = self.db.query(TenantSettings).filter(
                TenantSettings.tenant_id == self.tenant_id
            ).first()
        return self._tenant_settings

    @property
    def automation_settings(self) -> Optional[AutomationSettings]:
        if self._automation_settings is None:
            self._automation_settings = self.db.query(AutomationSettings).filter(
                AutomationSettings.tenant_id == self.tenant_id
            ).first()
        return self._automation_settings

    @property
    def whatsapp_client(self) -> Optional[WhatsAppCloudAPIClient]:
        if self._whatsapp_client is None and self.tenant_settings:
            if self.tenant_settings.is_whatsapp_configured:
                self._whatsapp_client = WhatsAppCloudAPIClient(
                    phone_number_id=self.tenant_settings.whatsapp_phone_number_id,
                    access_token=self.tenant_settings.whatsapp_access_token,
                    business_account_id=self.tenant_settings.whatsapp_business_account_id
                )
        return self._whatsapp_client

    def is_automation_enabled(self) -> bool:
        """Check if automation is properly configured and enabled"""
        if not self.tenant_settings:
            logger.warning(f"No tenant settings found for tenant {self.tenant_id}")
            return False

        if not self.tenant_settings.is_whatsapp_configured:
            logger.warning(f"WhatsApp not configured for tenant {self.tenant_id}")
            return False

        if not self.tenant_settings.is_active:
            logger.warning(f"Tenant settings inactive for tenant {self.tenant_id}")
            return False

        if self.automation_settings and not self.automation_settings.is_enabled:
            logger.warning(f"Automation disabled for tenant {self.tenant_id}")
            return False

        return True

    def get_catalog_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get active products for catalog"""
        products = self.db.query(Product).filter(
            Product.tenant_id == self.tenant_id,
            Product.is_active == True
        ).limit(limit).all()

        return [
            {
                "id": p.id,
                "name": p.name,
                "price": f"₹{p.price}" if p.price else "Contact for price",
                "description": p.description,
                "image_url": p.image_url,
                "sku": p.sku
            }
            for p in products
        ]

    def create_message_log(
        self,
        recipient_phone: str,
        message_type: str,
        message_content: Optional[str] = None,
        call_id: Optional[int] = None,
        media_url: Optional[str] = None
    ) -> MessageLog:
        """Create a message log entry"""
        log = MessageLog(
            tenant_id=self.tenant_id,
            call_id=call_id,
            recipient_phone=recipient_phone,
            message_type=message_type,
            message_content=message_content,
            media_url=media_url,
            status="pending"
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def update_message_log(
        self,
        log_id: int,
        status: str,
        whatsapp_message_id: Optional[str] = None,
        error_message: Optional[str] = None,
        api_response: Optional[Dict] = None
    ):
        """Update message log with result"""
        log = self.db.query(MessageLog).filter(MessageLog.id == log_id).first()
        if log:
            log.status = status
            log.whatsapp_message_id = whatsapp_message_id
            log.error_message = error_message
            log.api_response = api_response
            if status == "sent":
                log.sent_at = datetime.utcnow()
            self.db.commit()

    async def send_post_call_messages(
        self,
        caller_phone: str,
        call_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Main method: Send thank you message + catalog after call ends
        """
        if not self.is_automation_enabled():
            return {
                "success": False,
                "error": "Automation not enabled or configured"
            }

        if not self.whatsapp_client:
            return {
                "success": False,
                "error": "WhatsApp client not initialized"
            }

        results = {
            "success": True,
            "messages_sent": 0,
            "errors": [],
            "message_ids": []
        }

        settings = self.tenant_settings

        try:
            # Step 1: Send thank you message
            thank_you_log = self.create_message_log(
                recipient_phone=caller_phone,
                message_type="text",
                message_content=settings.thank_you_message,
                call_id=call_id
            )

            thank_you_result = await self.whatsapp_client.send_text_message(
                to_phone=caller_phone,
                message=settings.thank_you_message
            )

            if thank_you_result.get("success"):
                self.update_message_log(
                    log_id=thank_you_log.id,
                    status="sent",
                    whatsapp_message_id=thank_you_result.get("message_id"),
                    api_response=thank_you_result.get("response")
                )
                results["messages_sent"] += 1
                results["message_ids"].append(thank_you_result.get("message_id"))
            else:
                self.update_message_log(
                    log_id=thank_you_log.id,
                    status="failed",
                    error_message=thank_you_result.get("error_message"),
                    api_response=thank_you_result.get("response")
                )
                results["errors"].append(f"Thank you message failed: {thank_you_result.get('error_message')}")

            # Step 2: Send catalog if enabled
            if settings.include_catalog:
                products = self.get_catalog_products()

                if products:
                    catalog_log = self.create_message_log(
                        recipient_phone=caller_phone,
                        message_type="catalog",
                        message_content=f"Catalog with {len(products)} products",
                        call_id=call_id
                    )

                    catalog_results = await self.whatsapp_client.send_catalog_carousel(
                        to_phone=caller_phone,
                        products=products,
                        header_text=settings.catalog_header_message,
                        footer_text=settings.catalog_footer_message
                    )

                    # Count successful sends
                    successful = sum(1 for r in catalog_results if r.get("success"))
                    results["messages_sent"] += successful

                    if successful == len(catalog_results):
                        self.update_message_log(
                            log_id=catalog_log.id,
                            status="sent",
                            api_response={"total_products": len(products), "sent": successful}
                        )
                    else:
                        failed = len(catalog_results) - successful
                        self.update_message_log(
                            log_id=catalog_log.id,
                            status="partial",
                            error_message=f"{failed} of {len(catalog_results)} messages failed"
                        )
                        results["errors"].append(f"Catalog: {failed} messages failed")

            # Update call record if provided
            if call_id:
                call = self.db.query(Call).filter(Call.id == call_id).first()
                if call:
                    call.automation_triggered = True
                    call.automation_triggered_at = datetime.utcnow()
                    self.db.commit()

            return results

        except Exception as e:
            logger.error(f"Error in send_post_call_messages: {str(e)}")
            results["success"] = False
            results["errors"].append(str(e))
            return results


def get_automation_service(db: Session, tenant_id: int) -> AutomationService:
    """Factory function to create automation service"""
    return AutomationService(db=db, tenant_id=tenant_id)
