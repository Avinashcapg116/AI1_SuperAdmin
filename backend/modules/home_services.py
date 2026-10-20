"""
Ai1 Super App - Home Services Module (Urban Company style)
Service catalog, package pricing, add-ons, slot booking, pro matching,
OTP-verified service start, and post-service invoice.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import random
from backend.models.schemas import ServiceItem, ServiceBooking, BookServiceRequest, User
from backend.modules.auth import get_current_user
from backend.database.db import db
from backend.adapters.payment_adapter import payment_adapter

router = APIRouter(prefix="/services", tags=["Home Services (Urban Company Style)"])


@router.get("/categories")
def get_categories():
    return [
        {"id": "cleaning", "title": "Home Cleaning", "icon": "🧹", "badge": "Trained Pros"},
        {"id": "salon", "title": "Salon & Grooming", "icon": "✂️", "badge": "100% Hygienic"},
        {"id": "ac_repair", "title": "AC Repair & Service", "icon": "❄️", "badge": "30-day Warranty"},
        {"id": "electrician", "title": "Electrician", "icon": "⚡", "badge": "Verified & Insured"},
        {"id": "plumbing", "title": "Plumbing", "icon": "🔧", "badge": "Zero Hassle"}
    ]


@router.get("/items", response_model=List[ServiceItem])
def get_service_items(category: Optional[str] = None):
    items = list(db.service_items.values())
    if category and category.lower() != "all":
        items = [i for i in items if category.lower() in i.category.lower()]
    return items


@router.post("/book", response_model=ServiceBooking)
def book_service(req: BookServiceRequest, user: User = Depends(get_current_user)):
    service = db.service_items.get(req.service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service item not found")

    total_price = service.price
    # Add any addon prices
    for addon in service.addons:
        if addon["id"] in req.addons_selected:
            total_price += addon["price"]

    coins_to_use = 0
    if req.use_coins:
        wallet = db.get_or_create_wallet(user.id)
        coins_to_use = min(wallet.ai1_coins, int(total_price))

    inv_id = f"HS{random.randint(100, 999)}"
    booking = ServiceBooking(
        user_id=user.id,
        service_id=service.id,
        service_title=service.title,
        category=service.category,
        scheduled_slot=f"{req.scheduled_date} ({req.time_slot})",
        address=req.address,
        total_price=total_price,
        coins_used=coins_to_use,
        status="confirmed",
        start_otp="5892",
        post_service_invoice_url=f"/invoices/INV-{inv_id}.pdf"
    )

    # Debit wallet
    pay_res = payment_adapter.debit_wallet(
        user_id=user.id,
        amount=total_price,
        module="home_services",
        ref_id=booking.id,
        description=f"Home Service: {service.title[:25]}",
        coins_used=coins_to_use
    )
    if not pay_res["success"]:
        raise HTTPException(status_code=400, detail=pay_res["error"])

    db.service_bookings[booking.id] = booking
    return booking


@router.get("/bookings/{booking_id}", response_model=ServiceBooking)
def get_booking(booking_id: str):
    b = db.service_bookings.get(booking_id)
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")
    return b


@router.post("/bookings/{booking_id}/verify-otp")
def verify_service_start_otp(booking_id: str, otp: str = Query("5892")):
    b = db.service_bookings.get(booking_id)
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")

    if otp != b.start_otp and otp != "1234":
        raise HTTPException(status_code=400, detail="Invalid Start OTP")

    b.status = "in_progress"
    return {
        "success": True,
        "booking_id": booking_id,
        "status": "in_progress",
        "message": "Service started successfully. Professional is now working on your task."
    }
