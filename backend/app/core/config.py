from functools import lru_cache
from pydantic import BaseModel, field_validator
import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()


class Settings(BaseModel):
    PROJECT_NAME: str = "Brand Call → WhatsApp Automation"
    API_V1_STR: str = "/api/v1"

    # IMPORTANT: For dev, this points to your docker-compose Postgres
    DATABASE_URL: str = (
        os.getenv(
            "DATABASE_URL",
            "postgresql://devuser:devpassword@localhost:5432/brand_call_whatsapp_dev",
        )
    )

    # Auth / security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME_SUPER_SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )
    ALGORITHM: str = "HS256"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            if not v:
                return []
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return []


@lru_cache
def get_settings() -> Settings:
    return Settings()
