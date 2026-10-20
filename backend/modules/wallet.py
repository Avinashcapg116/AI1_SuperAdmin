"""
Ai1 Super App - Payments & Wallet Module (Paytm/PhonePe style)
Unified wallet, UPI pay, Bharat QR, utility bill payments, and Ai1 Coins loyalty engine.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from backend.models.schemas import (
    Wallet, WalletTransaction, TopUpRequest, UpiPayRequest,
    QrPayRequest, BillPayRequest, User
)
from backend.modules.auth import get_current_user
from backend.database.db import db
from backend.adapters.payment_adapter import payment_adapter
from backend.config import settings

router = APIRouter(prefix="/wallet", tags=["Ai1 Wallet & Payments"])


@router.get("", response_model=Wallet)
def get_wallet(user: User = Depends(get_current_user)):
    return db.get_or_create_wallet(user.id)


@router.post("/top-up")
def top_up_wallet(req: TopUpRequest, user: User = Depends(get_current_user)):
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    res = payment_adapter.credit_wallet(
        user_id=user.id,
        amount=req.amount,
        module="wallet",
        ref_id=f"TOPUP-{int(req.amount)}",
        description=f"Wallet Top-Up via {req.payment_method.upper()}"
    )
    return res


@router.post("/upi-pay")
def pay_via_upi(req: UpiPayRequest, user: User = Depends(get_current_user)):
    # 2FA Check per RBI guidelines for large amounts
    if req.amount >= settings.RBI_2FA_MANDATORY_ABOVE and req.mpin != "1234":
        raise HTTPException(status_code=403, detail="Invalid UPI MPIN")

    coins_to_use = 0
    if req.use_coins:
        wallet = db.get_or_create_wallet(user.id)
        coins_to_use = min(wallet.ai1_coins, int(req.amount))

    res = payment_adapter.debit_wallet(
        user_id=user.id,
        amount=req.amount,
        module="upi",
        ref_id=f"UPI-{req.target_vpa_or_phone}",
        description=f"Paid to {req.target_vpa_or_phone}: {req.note}",
        coins_used=coins_to_use
    )
    if not res["success"]:
        raise HTTPException(status_code=400, detail=res["error"])

    return res


@router.post("/scan-qr")
def pay_via_qr(req: QrPayRequest, user: User = Depends(get_current_user)):
    coins_to_use = 0
    if req.use_coins:
        wallet = db.get_or_create_wallet(user.id)
        coins_to_use = min(wallet.ai1_coins, int(req.amount))

    res = payment_adapter.debit_wallet(
        user_id=user.id,
        amount=req.amount,
        module="qr_pay",
        ref_id="BHARAT-QR-SCAN",
        description=f"QR Merchant Payment ({req.note})",
        coins_used=coins_to_use
    )
    if not res["success"]:
        raise HTTPException(status_code=400, detail=res["error"])

    return res


@router.post("/bill-payment")
def pay_utility_bill(req: BillPayRequest, user: User = Depends(get_current_user)):
    res = payment_adapter.pay_utility_bill(
        user_id=user.id,
        category=req.category,
        biller=req.biller_name,
        consumer_no=req.consumer_number,
        amount=req.amount
    )
    if not res["success"]:
        raise HTTPException(status_code=400, detail=res.get("error", "Bill payment failed"))

    return res


@router.get("/transactions", response_model=List[WalletTransaction])
def get_transactions(user: User = Depends(get_current_user)):
    wallet = db.get_or_create_wallet(user.id)
    return [t for t in db.transactions if t.wallet_id == wallet.id]


@router.get("/rewards")
def get_rewards(user: User = Depends(get_current_user)):
    wallet = db.get_or_create_wallet(user.id)
    return {
        "ai1_coins": wallet.ai1_coins,
        "coin_rupee_value": 1.0,
        "active_scratchcards": [
            {"id": "SC-01", "title": "50 Ai1 Coins on First Quick Commerce Order", "status": "unlocked"},
            {"id": "SC-02", "title": "₹100 Cashback on EV Fast Charging", "status": "claimed"}
        ],
        "referral_code": "AI1SUPER",
        "terms": "Ai1 Coins can be redeemed 1:1 on any grocery, ride, repair, or EV charge."
    }
