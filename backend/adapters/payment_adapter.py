"""
Ai1 Super App - Payment Gateway & Wallet Adapter
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import uuid
from backend.database.db import db
from backend.models.schemas import WalletTransaction


class PaymentAdapter(ABC):
    @abstractmethod
    def create_upi_intent(self, vpa: str, amount: float, note: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def generate_dynamic_qr(self, amount: float, merchant_name: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def debit_wallet(self, user_id: str, amount: float, module: str, ref_id: str, description: str, coins_used: int = 0) -> Dict[str, Any]:
        pass

    @abstractmethod
    def credit_wallet(self, user_id: str, amount: float, module: str, ref_id: str, description: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def pay_utility_bill(self, user_id: str, category: str, biller: str, consumer_no: str, amount: float) -> Dict[str, Any]:
        pass


class MockUpiPaymentAdapter(PaymentAdapter):
    """
    Realistic India UPI & Wallet Simulator.
    Implements NPCI UPI specification with VPA resolution, BharatQR, and Ai1 Coins cashback.
    """

    def create_upi_intent(self, vpa: str, amount: float, note: str) -> Dict[str, Any]:
        txn_ref = f"UPI-{uuid.uuid4().hex[:12].upper()}"
        intent_uri = f"upi://pay?pa={vpa}&pn=Ai1Pay&am={amount:.2f}&cu=INR&tn={note}&tr={txn_ref}"
        return {
            "success": True,
            "transaction_ref": txn_ref,
            "vpa": vpa,
            "amount": amount,
            "intent_uri": intent_uri,
            "status": "INITIATED"
        }

    def generate_dynamic_qr(self, amount: float, merchant_name: str = "Ai1 Merchant") -> Dict[str, Any]:
        qr_id = f"QR-{uuid.uuid4().hex[:8].upper()}"
        merchant_vpa = "merchant.ai1@npci"
        qr_string = f"upi://pay?pa={merchant_vpa}&pn={merchant_name}&am={amount:.2f}&cu=INR&tr={qr_id}"
        return {
            "qr_id": qr_id,
            "merchant_name": merchant_name,
            "amount": amount,
            "qr_string": qr_string,
            "expires_in_seconds": 300
        }

    def debit_wallet(self, user_id: str, amount: float, module: str, ref_id: str, description: str, coins_used: int = 0) -> Dict[str, Any]:
        wallet = db.get_or_create_wallet(user_id)
        
        # Calculate effective cash debit considering 1 Coin = ₹1
        effective_amount = max(0.0, amount - float(coins_used))
        
        if wallet.ai1_coins < coins_used:
            return {"success": False, "error": "Insufficient Ai1 Coins"}

        if wallet.balance < effective_amount:
            return {
                "success": False,
                "error": f"Insufficient balance. Wallet has ₹{wallet.balance:.2f}, required ₹{effective_amount:.2f}"
            }

        # Deduct
        wallet.balance -= effective_amount
        wallet.ai1_coins -= coins_used

        # Award cashback: 5% of cash paid in Ai1 Coins
        coins_earned = int(effective_amount * 0.05)
        wallet.ai1_coins += coins_earned

        txn = WalletTransaction(
            wallet_id=wallet.id,
            type="debit",
            amount=effective_amount,
            coins_earned=coins_earned,
            coins_used=coins_used,
            reference_module=module,
            reference_id=ref_id,
            description=description,
            status="completed"
        )
        db.transactions.insert(0, txn)

        return {
            "success": True,
            "transaction_id": txn.id,
            "amount_debited": effective_amount,
            "coins_used": coins_used,
            "coins_earned": coins_earned,
            "remaining_balance": wallet.balance,
            "total_coins": wallet.ai1_coins
        }

    def credit_wallet(self, user_id: str, amount: float, module: str, ref_id: str, description: str) -> Dict[str, Any]:
        wallet = db.get_or_create_wallet(user_id)
        wallet.balance += amount

        txn = WalletTransaction(
            wallet_id=wallet.id,
            type="credit",
            amount=amount,
            coins_earned=0,
            coins_used=0,
            reference_module=module,
            reference_id=ref_id,
            description=description,
            status="completed"
        )
        db.transactions.insert(0, txn)

        return {
            "success": True,
            "transaction_id": txn.id,
            "amount_credited": amount,
            "new_balance": wallet.balance
        }

    def pay_utility_bill(self, user_id: str, category: str, biller: str, consumer_no: str, amount: float) -> Dict[str, Any]:
        wallet = db.get_or_create_wallet(user_id)
        if wallet.balance < amount:
            return {"success": False, "error": "Insufficient wallet balance"}

        ref_id = f"BBPS-{uuid.uuid4().hex[:10].upper()}"
        res = self.debit_wallet(
            user_id=user_id,
            amount=amount,
            module="bill_pay",
            ref_id=ref_id,
            description=f"{category.upper()} Bill - {biller} ({consumer_no})"
        )
        if not res["success"]:
            return res

        return {
            "success": True,
            "bbps_ref_id": ref_id,
            "category": category,
            "biller": biller,
            "consumer_no": consumer_no,
            "amount_paid": amount,
            "status": "SUCCESSFUL",
            "cashback_coins": res["coins_earned"]
        }


# Singleton instance
payment_adapter = MockUpiPaymentAdapter()
