"""
Ai1 Super App - System Configuration & Regulatory Compliance Settings
"""

from typing import List
from pydantic import BaseModel


class Settings(BaseModel):
    APP_NAME: str = "Ai1 Super App"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "ai1-india-super-app-secret-key-2026-production-ready"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    # Regulatory & Compliance Thresholds
    # RBI Master Directions on Prepaid Payment Instruments (PPI)
    RBI_MIN_KYC_WALLET_LIMIT: float = 10000.0   # Monthly cap for unverified min-detail wallet
    RBI_FULL_KYC_WALLET_LIMIT: float = 200000.0 # Cap for biometric/DigiLocker KYC wallet
    RBI_2FA_MANDATORY_ABOVE: float = 2000.0    # ₹2000+ requires mandatory MPIN / OTP

    # IRDAI Insurance E-Commerce Regulations
    IRDAI_FREE_LOOK_DAYS: int = 15             # 15 days mandatory cancellation & refund
    IRDAI_BROKER_LICENSE: str = "IRDAI/WBA/098/2026"

    # DPDP Act 2023 Compliance
    DPDP_CONSENT_VERSION: str = "v1.2-2026"
    DPDP_DATA_RETENTION_DAYS: int = 365

    # EV Charging Protocol Defaults
    EV_STATUS_STALENESS_MINUTES: int = 15      # Flag "status unknown" after 15m without heartbeat
    EV_RESERVATION_HOLD_MINUTES: int = 15     # Hold connector for 15 minutes before auto-release
    EV_NO_SHOW_FEE: float = 50.0               # ₹50 penalty if user does not plug in within 15 mins

    # Supported Indian Languages
    SUPPORTED_LANGUAGES: List[str] = ["en", "hi", "kn", "ta", "te"]


settings = Settings()
