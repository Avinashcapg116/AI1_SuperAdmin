"""
Ai1 Super App - SMS & Notifications Adapter
Simulates Indian SMS Gateways (MSG91 / Gupshup / Kaleyra) with DLT template compliance.
"""

from typing import Dict, Any
import logging

logger = logging.getLogger("ai1.sms")


class SmsAdapter:
    def __init__(self):
        self.sent_messages = []

    def send_otp(self, phone: str, otp: str) -> Dict[str, Any]:
        # DLT registered template: "Your Ai1 verification code is {#var#}. Valid for 10 mins. Do not share."
        message = f"Your Ai1 verification code is {otp}. Valid for 10 mins. Do not share with anyone."
        self.sent_messages.append({"phone": phone, "message": message, "type": "OTP"})
        logger.info(f"[SMS Gateway] Dispatched to {phone}: {message}")
        return {
            "success": True,
            "phone": phone,
            "dlt_template_id": "DLT-AI1-OTP-1002",
            "status": "DELIVERED"
        }

    def send_transaction_alert(self, phone: str, amount: float, ref_id: str) -> Dict[str, Any]:
        message = f"Ai1 Alert: ₹{amount:.2f} debited from your Ai1 Wallet for ref {ref_id}. Balance updated."
        self.sent_messages.append({"phone": phone, "message": message, "type": "ALERT"})
        return {"success": True, "status": "DELIVERED"}


sms_adapter = SmsAdapter()
