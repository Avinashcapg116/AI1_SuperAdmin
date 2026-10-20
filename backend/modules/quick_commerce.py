"""
Ai1 Super App - Quick Commerce Module (Zepto / Instamart style)
Dark store inventory by pincode, 10-15 min ETA promise, cart checkout, coupons,
live rider GPS tracking, and "usual basket" replenishment.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import random
from backend.models.schemas import Product, Order, CheckoutRequest, User
from backend.modules.auth import get_current_user
from backend.database.db import db
from backend.adapters.payment_adapter import payment_adapter

router = APIRouter(prefix="/qc", tags=["Quick Commerce (10-15m)"])


@router.get("/dark-stores/check-pincode")
def check_pincode(pincode: str = Query("560038")):
    clean_pin = pincode.strip()
    for store in db.dark_stores.values():
        if store.pincode == clean_pin:
            return {
                "serviceable": True,
                "store_name": store.name,
                "area": store.area,
                "eta_mins": store.delivery_eta_mins,
                "free_delivery_above": 99.0
            }
    # Return default serviceable Indiranagar store for demo
    default_store = db.dark_stores["DS-BLR-01"]
    return {
        "serviceable": True,
        "store_name": default_store.name,
        "area": "Bengaluru Metro Area",
        "eta_mins": 12,
        "free_delivery_above": 99.0
    }


@router.get("/products", response_model=List[Product])
def get_products(category: Optional[str] = None, search: Optional[str] = None):
    prods = list(db.products.values())
    if category and category.lower() != "all":
        prods = [p for p in prods if category.lower() in p.category.lower()]
    if search:
        s = search.lower()
        prods = [p for p in prods if s in p.name.lower() or any(s in tag for tag in p.tags)]
    return prods


@router.get("/usual-basket")
def get_usual_basket():
    """Smart replenishment recommendation based on user past habits."""
    return {
        "basket_title": "Your Usual Morning Essentials",
        "total_items": 3,
        "savings": 22.0,
        "items": [
            {"product_id": "qc-milk-01", "name": "Amul Taaza Milk (500 ml)", "quantity": 2, "price": 28.0},
            {"product_id": "qc-bread-01", "name": "Whole Wheat Bread (350 g)", "quantity": 1, "price": 55.0},
            {"product_id": "qc-eggs-01", "name": "Fresh White Eggs (6 pcs)", "quantity": 1, "price": 52.0}
        ],
        "estimated_total": 163.0
    }


@router.post("/cart/checkout", response_model=Order)
def checkout_cart(req: CheckoutRequest, user: User = Depends(get_current_user)):
    if not req.items:
        raise HTTPException(status_code=400, detail="Cart cannot be empty")

    subtotal = sum(i.price * i.quantity for i in req.items)
    delivery_fee = 0.0 if subtotal >= 99.0 else 15.0
    discount = 0.0

    if req.coupon_code and req.coupon_code.upper() in ["FIRST10", "AI1SUPER"]:
        discount = round(subtotal * 0.10, 2)

    total_amount = max(0.0, subtotal + delivery_fee - discount)

    # Use coins if chosen
    coins_to_use = 0
    if req.use_coins:
        wallet = db.get_or_create_wallet(user.id)
        coins_to_use = min(wallet.ai1_coins, int(total_amount))

    order = Order(
        user_id=user.id,
        store_id="DS-BLR-01",
        items=req.items,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        discount=discount,
        coins_used=coins_to_use,
        total_amount=total_amount,
        pincode=req.pincode,
        delivery_address=req.delivery_address,
        slot_eta_mins=12,
        status="out_for_delivery"
    )

    # Debit wallet
    pay_res = payment_adapter.debit_wallet(
        user_id=user.id,
        amount=total_amount,
        module="quick_commerce",
        ref_id=order.id,
        description=f"Quick Commerce Order ({len(req.items)} items)",
        coins_used=coins_to_use
    )
    if not pay_res["success"]:
        raise HTTPException(status_code=400, detail=pay_res["error"])

    db.orders[order.id] = order
    return order


@router.get("/orders/{order_id}", response_model=Order)
def get_order_tracking(order_id: str):
    order = db.orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Simulate slight rider movement towards destination
    order.rider_lat += random.choice([-0.0005, 0.0005])
    order.rider_lng += random.choice([-0.0005, 0.0005])
    return order
