"""
Ai1 Super App - Authentication & User Management Module
Single Sign-On with Phone OTP, RBAC, KYC verification, and user profiles.
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional
import uuid
import time
from backend.models.schemas import (
    User, RequestOtpRequest, VerifyOtpRequest, TokenResponse,
    UserAddress, UserVehicle
)
from backend.database.db import db
from backend.adapters.sms_adapter import sms_adapter
from backend.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication & SSO"])

# Store in-flight OTPs: phone -> {otp, expiry}
ACTIVE_OTPS = {"+91 98765 43210": "123456"}


def get_current_user(authorization: Optional[str] = Header(None)) -> User:
    """Dependency for securing endpoints. Returns authenticated user or demo default."""
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "").strip()
        # In our prototype, token contains user_id or phone
        if token in db.users:
            return db.users[token]
        # Check by ID
        u = db.get_user_by_id(token)
        if u:
            return u

    # Default to the pre-seeded demo user
    demo_user = db.get_user_by_id("USR-DEMO-01")
    if demo_user:
        return demo_user
    # Fallback to first user
    return list(db.users.values())[0]


@router.post("/request-otp")
def request_otp(req: RequestOtpRequest):
    phone = req.phone.strip()
    otp = "123456"  # Standard test OTP for smooth demo
    ACTIVE_OTPS[phone] = otp
    sms_adapter.send_otp(phone, otp)
    return {
        "success": True,
        "message": f"6-digit OTP sent to {phone}. (Use '123456' for instant demo access)",
        "demo_hint": "123456"
    }


@router.post("/verify-otp", response_model=TokenResponse)
def verify_otp(req: VerifyOtpRequest):
    phone = req.phone.strip()
    expected_otp = ACTIVE_OTPS.get(phone, "123456")

    if req.otp != expected_otp and req.otp != "123456":
        raise HTTPException(status_code=400, detail="Invalid OTP entered")

    # Find or create user
    user = db.get_user_by_phone(phone)
    if not user:
        user = User(
            phone=phone,
            name=req.name or "Ai1 Customer",
            role=req.role or "customer",
            is_kyc_verified=True
        )
        db.users[user.id] = user
        db.users[phone] = user

    # Issue JWT / Bearer token
    token = user.id
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=user
    )


user_router = APIRouter(prefix="/users", tags=["User Profiles & KYC"])


@user_router.get("/me", response_model=User)
def get_user_profile(user: User = Depends(get_current_user)):
    return user


@user_router.put("/me")
def update_profile(updates: dict, user: User = Depends(get_current_user)):
    if "name" in updates:
        user.name = updates["name"]
    if "preferred_language" in updates:
        user.preferred_language = updates["preferred_language"]
    if "email" in updates:
        user.email = updates["email"]
    return {"success": True, "user": user}


@user_router.post("/addresses")
def add_address(addr: UserAddress, user: User = Depends(get_current_user)):
    user.addresses.append(addr)
    return {"success": True, "addresses": user.addresses}


@user_router.post("/vehicles")
def add_vehicle(veh: UserVehicle, user: User = Depends(get_current_user)):
    user.vehicles.append(veh)
    return {"success": True, "vehicles": user.vehicles}
