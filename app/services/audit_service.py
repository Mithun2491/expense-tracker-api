# app/services/audit_service.py
from sqlalchemy.orm import Session
from ..models.audit_log import AuditLog
from typing import Optional, Dict, Any

def create_audit_log(db: Session, *, user_id: Optional[int], action: str, target_type: str, target_id: Optional[int]=None, data: Optional[Dict[str, Any]]=None):
    log = AuditLog(user_id=user_id, action=action, target_type=target_type, target_id=target_id, data=data or {})
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
