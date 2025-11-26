from fastapi import APIRouter
from app.api.deps import CurrentUserDep
from app.schemas.user import User

router = APIRouter()


@router.get("/me", response_model=User)
def read_users_me(current_user: CurrentUserDep) -> User:
    """
    Get current logged-in user.
    """
    return current_user
