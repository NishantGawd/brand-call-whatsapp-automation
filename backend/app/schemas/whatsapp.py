# app/schemas/whatsapp.py

from pydantic import BaseModel, Field


class WhatsAppTestRequest(BaseModel):
    to: str = Field(
        ...,
        json_schema_extra={"example": "whatsapp:+910000000000"}
    )
    body: str = Field(
        ...,
        json_schema_extra={"example": "Test message from Celery & FastAPI"}
    )
