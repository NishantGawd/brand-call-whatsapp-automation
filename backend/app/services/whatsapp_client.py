# COMPLETE REWRITE - Full WhatsApp Cloud API client with media support
import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WhatsAppCloudAPIClient:
    """WhatsApp Cloud API Client with full media and catalog support"""

    BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(
        self,
        phone_number_id: str,
        access_token: str,
        business_account_id: Optional[str] = None
    ):
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.business_account_id = business_account_id
        self.messages_url = f"{self.BASE_URL}/{phone_number_id}/messages"
        self.media_url = f"{self.BASE_URL}/{phone_number_id}/media"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _format_phone_number(self, phone: str) -> str:
        """Ensure phone number is in correct format (no + prefix for API)"""
        phone = phone.strip().replace(" ", "").replace("-", "")
        if phone.startswith("+"):
            phone = phone[1:]
        return phone

    async def send_text_message(
        self,
        to_phone: str,
        message: str,
        preview_url: bool = False
    ) -> Dict[str, Any]:
        """Send a plain text message"""
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self._format_phone_number(to_phone),
            "type": "text",
            "text": {
                "preview_url": preview_url,
                "body": message
            }
        }

        return await self._send_request(payload)

    async def send_image_message(
        self,
        to_phone: str,
        image_url: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send an image message with optional caption"""
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self._format_phone_number(to_phone),
            "type": "image",
            "image": {
                "link": image_url
            }
        }

        if caption:
            payload["image"]["caption"] = caption

        return await self._send_request(payload)

    async def send_document_message(
        self,
        to_phone: str,
        document_url: str,
        filename: str,
        caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send a document (PDF catalog)"""
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self._format_phone_number(to_phone),
            "type": "document",
            "document": {
                "link": document_url,
                "filename": filename
            }
        }

        if caption:
            payload["document"]["caption"] = caption

        return await self._send_request(payload)

    async def send_template_message(
        self,
        to_phone: str,
        template_name: str,
        language_code: str = "en",
        components: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Send a pre-approved template message (required for first contact)"""
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self._format_phone_number(to_phone),
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }

        if components:
            payload["template"]["components"] = components

        return await self._send_request(payload)

    async def send_catalog_carousel(
        self,
        to_phone: str,
        products: List[Dict[str, Any]],
        header_text: Optional[str] = None,
        body_text: Optional[str] = None,
        footer_text: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Send product catalog as individual image messages
        Each product: {name, price, image_url, description}
        Returns list of API responses
        """
        responses = []
        to_phone = self._format_phone_number(to_phone)

        # Send header message if provided
        if header_text:
            response = await self.send_text_message(to_phone, header_text)
            responses.append(response)

        # Send each product as image with caption
        for idx, product in enumerate(products, 1):
            caption = f"*{idx}. {product.get('name', 'Product')}*\n"
            caption += f"Price: {product.get('price', 'Contact for price')}\n"
            if product.get('description'):
                caption += f"{product['description']}\n"
            if product.get('sku'):
                caption += f"SKU: {product['sku']}"

            if product.get('image_url'):
                response = await self.send_image_message(
                    to_phone,
                    product['image_url'],
                    caption.strip()
                )
            else:
                response = await self.send_text_message(to_phone, caption.strip())

            responses.append(response)

        # Send footer message if provided
        if footer_text:
            response = await self.send_text_message(to_phone, footer_text)
            responses.append(response)

        return responses

    async def send_interactive_list(
        self,
        to_phone: str,
        header_text: str,
        body_text: str,
        button_text: str,
        sections: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Send interactive list message for product selection"""
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self._format_phone_number(to_phone),
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": header_text
                },
                "body": {
                    "text": body_text
                },
                "action": {
                    "button": button_text,
                    "sections": sections
                }
            }
        }

        return await self._send_request(payload)

    async def _send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send request to WhatsApp API with error handling"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.messages_url,
                    headers=self._get_headers(),
                    json=payload
                )

                response_data = response.json()

                if response.status_code == 200:
                    logger.info(f"WhatsApp message sent successfully: {response_data}")
                    return {
                        "success": True,
                        "message_id": response_data.get("messages", [{}])[0].get("id"),
                        "response": response_data
                    }
                else:
                    error = response_data.get("error", {})
                    logger.error(f"WhatsApp API error: {error}")
                    return {
                        "success": False,
                        "error_code": error.get("code"),
                        "error_message": error.get("message"),
                        "response": response_data
                    }

        except httpx.TimeoutException:
            logger.error("WhatsApp API request timed out")
            return {
                "success": False,
                "error_message": "Request timed out",
                "response": None
            }
        except Exception as e:
            logger.error(f"WhatsApp API request failed: {str(e)}")
            return {
                "success": False,
                "error_message": str(e),
                "response": None
            }

    async def check_health(self) -> Dict[str, Any]:
        """Check if credentials are valid"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.BASE_URL}/{self.phone_number_id}",
                    headers=self._get_headers()
                )

                if response.status_code == 200:
                    return {"success": True, "data": response.json()}
                else:
                    return {"success": False, "error": response.json()}

        except Exception as e:
            return {"success": False, "error": str(e)}
