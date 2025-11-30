from typing import Optional

from pydantic import BaseModel, Field


class AutomationSettingsBase(BaseModel):
    enabled: bool = False
    delay_seconds: int = Field(
        default=60, ge=0, description="Delay after call ends before sending WhatsApp"
    )
    min_call_duration_seconds: int = Field(
        default=0, ge=0, description="Minimum call duration in seconds to trigger"
    )
    send_mode: str = Field(
        default="thank_you_and_full_catalog",
        description=(
            "Options: 'thank_you_only', "
            "'thank_you_and_full_catalog', "
            "'thank_you_and_filtered_catalog'"
        ),
    )
    include_categories: Optional[str] = Field(
        default=None,
        description=(
            "Comma-separated category names to include. "
            "Used when send_mode='thank_you_and_filtered_catalog'."
        ),
    )
    exclude_categories: Optional[str] = Field(
        default=None,
        description="Comma-separated category names to exclude from catalog.",
    )


class AutomationSettingsCreate(AutomationSettingsBase):
    pass


class AutomationSettingsUpdate(AutomationSettingsBase):
    # all fields optional for PATCH-like updates
    enabled: Optional[bool] = None
    delay_seconds: Optional[int] = Field(default=None, ge=0)
    min_call_duration_seconds: Optional[int] = Field(default=None, ge=0)
    send_mode: Optional[str] = None
    include_categories: Optional[str] = None
    exclude_categories: Optional[str] = None


class AutomationSettingsOut(AutomationSettingsBase):
    id: int
    tenant_id: int

    class Config:
        orm_mode = True
