from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_active_user
from app.crud.crud_call import call_crud
from app.schemas.call import CallOut

router = APIRouter()


@router.get("/", response_model=List[CallOut])
def list_my_calls(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    List calls for the current user's tenant, newest first.
    """
    calls = call_crud.list_for_tenant(db, tenant_id=current_user.tenant_id)
    return calls
