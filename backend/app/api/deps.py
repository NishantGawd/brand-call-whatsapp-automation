from typing import Generator, Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import verify_password
from app.db.session import get_db
from app.models.user import User as UserModel
from app.schemas.token import TokenPayload

settings = get_settings()

# HTTP Bearer auth scheme (for "Authorize" in Swagger)
bearer_scheme = HTTPBearer(auto_error=False)


# ---------- DB DEPENDENCY ----------

def get_db_dep() -> Generator:
    """Yield a SQLAlchemy DB session and close it afterwards."""
    yield from get_db()


DBSessionDep = Annotated[Session, Depends(get_db_dep)]


# ---------- USER HELPERS ----------

def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    """Return user by email or None."""
    return db.query(UserModel).filter(UserModel.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> Optional[UserModel]:
    """
    Verify user credentials.
    Return user if valid, None otherwise.
    """
    user = get_user_by_email(db, email=email)
    if not user:
        return None

    # Pylance thinks user.hashed_password is Column[str]; cast to str for type-checker
    hashed_password: str = getattr(user, "hashed_password")

    if not verify_password(password, hashed_password):
        return None

    return user


# ---------- CURRENT USER DEPENDENCY ----------

def get_current_user(
    db: DBSessionDep,
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)],
) -> UserModel:
    """
    Extract user from Bearer token.
    Expects header: Authorization: Bearer <token>
    """
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    if token_data.sub is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user_id = int(token_data.sub)
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


CurrentUserDep = Annotated[UserModel, Depends(get_current_user)]
