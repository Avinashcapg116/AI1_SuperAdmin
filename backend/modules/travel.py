"""
Ai1 Super App - Travel Module (ixigo style)
Search and compare flights, trains with live PNR & seat availability, buses,
and trip itinerary builder that auto-adds cabs and travel insurance.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from backend.models.schemas import TravelBooking, TripItineraryRequest, User
from backend.modules.auth import get_current_user
from backend.database.db import db
from backend.adapters.travel_adapter import travel_adapter
from backend.adapters.payment_adapter import payment_adapter

router = APIRouter(prefix="/travel", tags=["Travel (Flights, Trains, Buses)"])


@router.get("/flights/search")
def search_flights(origin: str = "BLR", destination: str = "DEL", date: str = "Tomorrow"):
    return travel_adapter.search_flights(origin, destination, date)


@router.get("/trains/search")
def search_trains(origin: str = "SBC", destination: str = "MAS", date: str = "Tomorrow"):
    return travel_adapter.search_trains(origin, destination, date)


@router.get("/trains/pnr")
def check_pnr_status(pnr: str = Query("8423451290")):
    return travel_adapter.check_pnr_status(pnr)


@router.get("/buses/search")
def search_buses(origin: str = "BLR", destination: str = "MYSORE", date: str = "Tomorrow"):
    return travel_adapter.search_buses(origin, destination, date)


@router.post("/itinerary/build")
def build_and_book_itinerary(req: TripItineraryRequest, user: User = Depends(get_current_user)):
    res = travel_adapter.build_composite_itinerary(
        user_id=user.id,
        travel_type=req.travel_type,
        origin=req.origin,
        dest=req.destination,
        date=req.date,
        add_cab=req.add_airport_cab,
        add_insurance=req.add_travel_insurance
    )

    # Debit wallet
    pay_res = payment_adapter.debit_wallet(
        user_id=user.id,
        amount=res["total_fare"],
        module="travel",
        ref_id=res["booking_id"],
        description=f"Trip Bundle: {req.origin} to {req.destination}"
    )

    return {
        "success": True,
        "booking_details": res,
        "payment": pay_res
    }


@router.get("/bookings", response_model=List[TravelBooking])
def get_travel_bookings(user: User = Depends(get_current_user)):
    return [b for b in db.travel_bookings.values() if b.user_id == user.id]
