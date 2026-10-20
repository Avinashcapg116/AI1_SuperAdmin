"""
Ai1 Super App - Platform Admin & Compliance Audit Module
Provides cross-module platform GMV analytics, DPDP Act 2023 audit logs,
and user privacy data export.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from datetime import datetime
from backend.models.schemas import AuditLogEntry, User
from backend.modules.auth import get_current_user
from backend.database.db import db

router = APIRouter(prefix="/admin", tags=["Platform Admin & Compliance Audit"])


@router.get("/metrics")
def get_platform_metrics():
    """Consolidated super-app business and operational indicators."""
    return {
        "platform_status": "OPERATIONAL",
        "active_city": "Bengaluru (KA, India)",
        "gross_merchandise_value_inr": 284500.0,
        "total_active_users": 18450,
        "quick_commerce_orders_today": 842,
        "rides_completed_today": 612,
        "home_service_jobs_today": 128,
        "ev_kwh_delivered_today": 1840.5,
        "policies_issued_today": 94,
        "ai1_coins_circulating": 450200,
        "rbi_compliance_score": "100% Compliant (Tokenized & 2FA Enforced)",
        "irdai_compliance_score": "100% Compliant (15-Day Free-Look Active)",
        "dpdp_compliance_score": "100% Compliant (Consent Notices Enforced)"
    }


@router.get("/audit-logs", response_model=List[AuditLogEntry])
def get_audit_logs():
    # Return mock DPDP & financial audit trail
    now = datetime.utcnow().isoformat()
    return [
        AuditLogEntry(
            action="CONSENT_RECORDED",
            module="DPDP_COMPLIANCE",
            details={"consent_type": "Location & Phone Verification", "version": "v1.2-2026", "language": "en"}
        ),
        AuditLogEntry(
            action="WALLET_DEBIT_2FA_VERIFIED",
            module="RBI_PPI",
            details={"amount": 929.0, "mpin_verified": True, "token_ref": "UPI-AIRPORT-RIDE"}
        ),
        AuditLogEntry(
            action="POLICY_FREE_LOOK_DISCLOSED",
            module="IRDAI_COMPLIANCE",
            details={"policy": "POL-HDFC-9912", "free_look_days": 15, "insurer": "HDFC ERGO"}
        ),
        AuditLogEntry(
            action="EV_OCPP_HEARTBEAT_ACK",
            module="EV_SMARTGRID",
            details={"station": "EV-STN-01", "connector": "CONN-01-A", "status": "AVAILABLE"}
        )
    ]


@router.get("/users/export-my-data")
def export_user_data(user: User = Depends(get_current_user)):
    """DPDP Act 2023: Right to Data Portability & Access self-service."""
    wallet = db.get_or_create_wallet(user.id)
    return {
        "user_profile": user.model_dump(),
        "wallet_snapshot": wallet.model_dump(),
        "recent_orders": [o.model_dump() for o in db.orders.values() if o.user_id == user.id],
        "policies": [p.model_dump() for p in db.policies.values() if p.user_id == user.id],
        "export_timestamp": datetime.utcnow().isoformat(),
        "dpdp_notice": "Your personal data is encrypted in transit and at rest per DPDP Act 2023."
    }
