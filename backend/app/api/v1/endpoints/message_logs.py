# NEW FILE - API for viewing message history
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.message_log import MessageLog
from app.schemas.message_log import MessageLogResponse

router = APIRouter()


@router.get("/", response_model=List[MessageLogResponse])
async def get_message_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = None,
    phone: Optional[str] = None,
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get message history for the tenant"""
    query = db.query(MessageLog).filter(
        MessageLog.tenant_id == current_user.tenant_id,
        MessageLog.created_at >= datetime.utcnow() - timedelta(days=days)
    )

    if status:
        query = query.filter(MessageLog.status == status)

    if phone:
        query = query.filter(MessageLog.recipient_phone.contains(phone))

    messages = query.order_by(MessageLog.created_at.desc()).offset(skip).limit(limit).all()

    return messages


@router.get("/stats")
async def get_message_stats(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get message statistics"""
    since = datetime.utcnow() - timedelta(days=days)

    total = db.query(MessageLog).filter(
        MessageLog.tenant_id == current_user.tenant_id,
        MessageLog.created_at >= since
    ).count()

    sent = db.query(MessageLog).filter(
        MessageLog.tenant_id == current_user.tenant_id,
        MessageLog.created_at >= since,
        MessageLog.status == "sent"
    ).count()

    failed = db.query(MessageLog).filter(
        MessageLog.tenant_id == current_user.tenant_id,
        MessageLog.created_at >= since,
        MessageLog.status == "failed"
    ).count()

    return {
        "period_days": days,
        "total_messages": total,
        "sent": sent,
        "failed": failed,
        "success_rate": round((sent / total * 100), 2) if total > 0 else 0
    }
