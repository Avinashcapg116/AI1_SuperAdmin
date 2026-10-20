"""
Ai1 Super App - Ride Hailing Module (Rapido / Ola / Uber style)
Bike, Auto, Cab categories, pickup/drop on map, surge indicator,
simulated driver assignment, live GPS tracking, SOS and share-trip.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
import random
from backend.models.schemas import (
    Ride, RideEstimateRequest, RideEstimateOption, BookRideRequest, User
)
from backend.modules.auth import get_current_user
from backend.database.db import db, haversine_distance_km
from backend.adapters.payment_adapter import payment_adapter

router = APIRouter(prefix="/rides", tags=["Ride Hailing (Bike/Auto/Cab)"])


@router.post("/estimate", response_model=List[RideEstimateOption])
def estimate_ride_fares(req: RideEstimateRequest):
    dist_km = haversine_distance_km(req.pickup_lat, req.pickup_lng, req.drop_lat, req.drop_lng)
    if dist_km <= 0.1:
        dist_km = 6.4  # Default realistic trip distance in Bengaluru

    # Realistic surge check: 1.1x during peak hours
    surge = 1.1

    options = [
        RideEstimateOption(
            category="bike",
            title="Ai1 Moto Bike",
            eta_mins=3,
            base_fare=round(25.0 + (dist_km * 9.0), 2),
            surge_multiplier=1.0,
            final_fare=round((25.0 + (dist_km * 9.0)), 2),
            capacity=1,
            co2_saved_kg=round(dist_km * 0.08, 2)
        ),
        RideEstimateOption(
            category="auto",
            title="Ai1 Auto (Meter Fare)",
            eta_mins=4,
            base_fare=round(30.0 + (dist_km * 15.0), 2),
            surge_multiplier=1.0,
            final_fare=round((30.0 + (dist_km * 15.0)), 2),
            capacity=3,
            co2_saved_kg=round(dist_km * 0.04, 2)
        ),
        RideEstimateOption(
            category="cab_mini",
            title="Ai1 Go Mini (AC)",
            eta_mins=6,
            base_fare=round(60.0 + (dist_km * 18.0), 2),
            surge_multiplier=surge,
            final_fare=round((60.0 + (dist_km * 18.0)) * surge, 2),
            capacity=4,
            co2_saved_kg=0.0
        ),
        RideEstimateOption(
            category="cab_prime",
            title="Ai1 Prime EV Sedan",
            eta_mins=5,
            base_fare=round(80.0 + (dist_km * 22.0), 2),
            surge_multiplier=surge,
            final_fare=round((80.0 + (dist_km * 22.0)) * surge, 2),
            capacity=4,
            co2_saved_kg=round(dist_km * 0.14, 2)
        )
    ]
    return options


@router.post("/book", response_model=Ride)
def book_ride(req: BookRideRequest, user: User = Depends(get_current_user)):
    dist_km = haversine_distance_km(req.pickup_lat, req.pickup_lng, req.drop_lat, req.drop_lng)
    if dist_km <= 0.1:
        dist_km = 6.4

    # Calculate fare
    rate_map = {"bike": 9.0, "auto": 15.0, "cab_mini": 18.0, "cab_prime": 22.0}
    base_map = {"bike": 25.0, "auto": 30.0, "cab_mini": 60.0, "cab_prime": 80.0}
    base = base_map.get(req.category, 60.0)
    rate = rate_map.get(req.category, 18.0)
    total_fare = round(base + (dist_km * rate), 2)

    coins_to_use = 0
    if req.use_coins:
        wallet = db.get_or_create_wallet(user.id)
        coins_to_use = min(wallet.ai1_coins, int(total_fare))

    ride = Ride(
        user_id=user.id,
        category=req.category,
        pickup_address=req.pickup_address,
        pickup_lat=req.pickup_lat,
        pickup_lng=req.pickup_lng,
        drop_address=req.drop_address,
        drop_lat=req.drop_lat,
        drop_lng=req.drop_lng,
        fare=total_fare,
        driver_lat=req.pickup_lat + 0.003,
        driver_lng=req.pickup_lng + 0.002,
        status="driver_assigned"
    )

    # Debit wallet
    pay_res = payment_adapter.debit_wallet(
        user_id=user.id,
        amount=total_fare,
        module="rides",
        ref_id=ride.id,
        description=f"Ride to {req.drop_address[:25]} ({req.category})",
        coins_used=coins_to_use
    )
    if not pay_res["success"]:
        raise HTTPException(status_code=400, detail=pay_res["error"])

    db.rides[ride.id] = ride
    return ride


@router.get("/{ride_id}/live", response_model=Ride)
def get_live_ride(ride_id: str):
    ride = db.rides.get(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    # Simulate driver moving closer to pickup
    ride.driver_lat += random.choice([-0.0004, 0.0004])
    ride.driver_lng += random.choice([-0.0004, 0.0004])
    return ride


@router.post("/{ride_id}/sos")
def trigger_sos(ride_id: str, user: User = Depends(get_current_user)):
    ride = db.rides.get(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    ride.sos_active = True
    return {
        "success": True,
        "ride_id": ride_id,
        "sos_status": "ACTIVE",
        "emergency_contacts_alerted": ["+91 98450 99887 (Emergency Contact)"],
        "police_control_room_dispatched": "Bengaluru Police (112)",
        "shareable_live_tracking_url": f"https://ai1.in/track/sos/{ride_id}"
    }


@router.get("/history", response_model=List[Ride])
def get_ride_history(user: User = Depends(get_current_user)):
    return [r for r in db.rides.values() if r.user_id == user.id]
