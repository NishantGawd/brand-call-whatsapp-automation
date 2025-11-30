from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db_dep, get_current_user
from app.models.user import User


def get_db() -> Generator[Session, None, None]:
    """
    Thin wrapper around app.api.deps.get_db_dep so that other modules
    can simply import get_db from app.core.deps.
    """
    # yield from passes through the generator from get_db_dep
    yield from get_db_dep()


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Thin wrapper around app.api.deps.get_current_user so that other modules
    can import get_current_active_user.
    """
    return current_user
