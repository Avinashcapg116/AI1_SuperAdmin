"""
Ai1 Super App - Insurance Provider Adapter
Simulates leading Indian insurers (HDFC ERGO, ICICI Lombard, Star Health, Tata AIG)
with IRDAI compliance (15-day Free-Look, instant policy vault, paperless claims).
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import uuid
from backend.database.db import db
from backend.models.schemas import Policy


class InsuranceAdapter:
    def get_quotes(self, category: str) -> List[Dict[str, Any]]:
        clean_cat = category.lower()
        quotes = []
        for q in db.insurance_quotes.values():
            if clean_cat in ["all", ""] or q["type"] == clean_cat:
                quotes.append(q)
        return quotes

    def issue_policy(self, user_id: str, quote_id: str, insured_name: str, kyc_doc_id: str) -> Dict[str, Any]:
        quote = db.insurance_quotes.get(quote_id)
        if not quote:
            # Fallback quote
            quote = list(db.insurance_quotes.values())[0]

        now = datetime.utcnow()
        expiry = now + timedelta(days=365)
        free_look = now + timedelta(days=15)

        policy_no = f"POL-{quote['insurer_name'][:4].upper()}-{uuid.uuid4().hex[:6].upper()}"

        policy = Policy(
            user_id=user_id,
            policy_type=quote["type"],
            insurer_name=quote["insurer_name"],
            plan_name=quote["plan_name"],
            policy_number=policy_no,
            sum_insured=quote["cover_amount"],
            premium_paid=quote["premium_annual"],
            start_date=now.strftime("%Y-%m-%d"),
            expiry_date=expiry.strftime("%Y-%m-%d"),
            free_look_ends=free_look.strftime("%Y-%m-%d"),
            status="active"
        )
        db.policies[policy.id] = policy

        return {
            "success": True,
            "policy_id": policy.id,
            "policy_number": policy.policy_number,
            "insurer": policy.insurer_name,
            "plan_name": policy.plan_name,
            "sum_insured": policy.sum_insured,
            "premium_paid": policy.premium_paid,
            "free_look_period_days": 15,
            "free_look_ends": policy.free_look_ends,
            "status": "active",
            "message": "Policy issued instantly and added to your Ai1 Policy Vault."
        }

    def file_claim(self, user_id: str, policy_id: str, reason: str, amount: float) -> Dict[str, Any]:
        claim_id = f"CLM-{uuid.uuid4().hex[:8].upper()}"
        return {
            "claim_id": claim_id,
            "policy_id": policy_id,
            "estimated_amount": amount,
            "status": "UNDER_EXAMINATION",
            "tpa_assigned": "MediAssist Cashless Desk",
            "message": "Paperless cashless claim submitted. Cashless approval expected within 2 hours."
        }


insurance_adapter = InsuranceAdapter()
