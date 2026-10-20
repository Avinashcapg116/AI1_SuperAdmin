"""
Ai1 Super App - Insurance Module
Health, motor, travel, term, and home insurance.
Multi-insurer quote comparison, instant paperless purchase with KYC,
policy vault, renewal reminders, and paperless claim initiation.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from backend.models.schemas import Policy, BuyPolicyRequest, ClaimRequest, User
from backend.modules.auth import get_current_user
from backend.database.db import db
from backend.adapters.insurance_adapter import insurance_adapter
from backend.adapters.payment_adapter import payment_adapter

router = APIRouter(prefix="/insurance", tags=["Insurance (Health, Motor, Travel)"])


@router.get("/quotes")
def get_insurance_quotes(type: str = Query("all")):
    return insurance_adapter.get_quotes(type)


@router.post("/buy", response_model=Policy)
def buy_insurance_policy(req: BuyPolicyRequest, user: User = Depends(get_current_user)):
    quote = db.insurance_quotes.get(req.quote_id)
    premium = quote["premium_annual"] if quote else 8940.0

    coins_to_use = 0
    if req.use_coins:
        wallet = db.get_or_create_wallet(user.id)
        coins_to_use = min(wallet.ai1_coins, int(premium))

    # Debit wallet
    pay_res = payment_adapter.debit_wallet(
        user_id=user.id,
        amount=premium,
        module="insurance",
        ref_id=f"INS-{req.quote_id}",
        description=f"Insurance Premium: {quote['plan_name'] if quote else 'Policy'}",
        coins_used=coins_to_use
    )
    if not pay_res["success"]:
        raise HTTPException(status_code=400, detail=pay_res["error"])

    issued = insurance_adapter.issue_policy(
        user_id=user.id,
        quote_id=req.quote_id,
        insured_name=req.insured_name,
        kyc_doc_id=req.insured_pan_or_aadhaar
    )

    policy = db.policies.get(issued["policy_id"])
    return policy


@router.get("/vault", response_model=List[Policy])
def get_policy_vault(user: User = Depends(get_current_user)):
    return [p for p in db.policies.values() if p.user_id == user.id]


@router.post("/claim")
def initiate_claim(req: ClaimRequest, user: User = Depends(get_current_user)):
    return insurance_adapter.file_claim(
        user_id=user.id,
        policy_id=req.policy_id,
        reason=req.claim_reason,
        amount=req.estimated_amount
    )
