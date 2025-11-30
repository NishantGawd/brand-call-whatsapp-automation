# app/services/whatsapp_client.py

from __future__ import annotations

import logging
import os
from typing import Optional, Dict, Any

import httpx

logger = logging.getLogger(__name__)


class WhatsAppClient:
    """
    Simple wrapper around the WhatsApp Cloud API.

    In this project we mainly care about:
    - Not crashing when credentials are missing.
    - Returning a structured result for logging and debugging.
    """

    def __init__(
        self,
        access_token: Optional[str] = None,
        phone_number_id: Optional[str] = None,
    ) -> None:
        # Read from env if not explicitly provided
        if access_token is None:
            access_token = os.getenv("WHATSAPP_DEFAULT_ACCESS_TOKEN", "")
        if phone_number_id is None:
            phone_number_id = os.getenv("WHATSAPP_DEFAULT_PHONE_NUMBER_ID", "")

        self.access_token: str = access_token.strip()
        self.phone_number_id: str = phone_number_id.strip()

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def send_text(self, to: str, body: str) -> Dict[str, Any]:
        """
        Send a simple WhatsApp text message.

        Returns a dict like:
        {
            "success": bool,
            "status_code": int | None,
            "error": str | None,
            "raw_response": str | None,
        }
        """

        # If credentials are missing, don't even try the HTTP call.
        if not self.access_token or not self.phone_number_id:
            logger.warning(
                "WhatsApp credentials not configured "
                "(access_token or phone_number_id missing). Skipping send."
            )
            return {
                "success": False,
                "status_code": None,
                "error": "WHATSAPP_NOT_CONFIGURED",
                "raw_response": None,
            }

        url = (
            f"https://graph.facebook.com/v17.0/"
            f"{self.phone_number_id}/messages"
        )

        payload: Dict[str, Any] = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": body},
        }

        try:
            logger.info("Sending WhatsApp text message to %s", to)
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                )

            logger.info(
                "WhatsApp API responded with status %s",
                response.status_code,
            )

            return {
                "success": response.is_success,
                "status_code": response.status_code,
                "error": None if response.is_success else "HTTP_ERROR",
                "raw_response": response.text,
            }

        except Exception as exc:  # noqa: BLE001
            logger.error("Error sending WhatsApp message: %s", exc, exc_info=True)
            return {
                "success": False,
                "status_code": None,
                "error": str(exc),
                "raw_response": None,
            }


def send_whatsapp_text(
    to: str,
    body: str,
    access_token: Optional[str] = None,
    phone_number_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function used by the Celery task.

    It just instantiates `WhatsAppClient` and calls `send_text`.
    """
    client = WhatsAppClient(
       access_token=access_token,
        phone_number_id=phone_number_id,
    )
    return client.send_text(to=to, body=body)
