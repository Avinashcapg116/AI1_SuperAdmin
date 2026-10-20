"""
Ai1 Super App - Partner App Module
Empowers gig partners: Delivery Riders, Cab/Auto Drivers, Home Service Pros,
Emergency Mechanics, and EV Station Operators.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, List
from backend.models.schemas import User
from backend.modules.auth import get_current_user
from backend.database.db import db

router = APIRouter(prefix="/partner", tags=["Partner Console (Gig Workers & Station Operators)"])


@router.get("/dashboard")
def get_partner_dashboard(role: str = Query("rider")):
    """Returns specific partner metrics based on active toggle."""
    if role == "rider":
        return {
            "role": "Quick Commerce Delivery Partner",
            "partner_name": "Suresh Kumar",
            "today_earnings": 1420.0,
            "deliveries_completed": 12,
            "rating": 4.92,
            "active_tasks": [
                {
                    "task_id": "TASK-QC-109",
                    "type": "Grocery Delivery",
                    "pickup_store": "Ai1 QuickStore Indiranagar",
                    "drop_address": "Flat 402, Prestige Palms, Indiranagar",
                    "payout": 65.0,
                    "distance_km": 1.4,
                    "status": "ready_for_pickup"
                }
            ]
        }
    elif role == "driver":
        return {
            "role": "Ai1 Mobility Driver Partner",
            "partner_name": "Manjunath Gowda",
            "vehicle": "KA 01 MJ 4242 (Tata Nexon EV)",
            "today_earnings": 2850.0,
            "trips_completed": 7,
            "driver_score": 98.4,
            "active_tasks": [
                {
                    "ride_id": "RIDE-8910",
                    "pickup": "Indiranagar 100ft Road",
                    "drop": "Kempegowda Airport",
                    "fare": 850.0,
                    "status": "navigating_to_pickup"
                }
            ]
        }
    elif role == "service_pro":
        return {
            "role": "Urban Home Master Pro",
            "partner_name": "Rajesh Sharma",
            "category": "AC Repair & Servicing",
            "today_earnings": 1800.0,
            "jobs_completed": 3,
            "rating": 4.95,
            "active_tasks": [
                {
                    "booking_id": "HS-4491",
                    "service": "Intense Foam-Jet AC Servicing",
                    "slot": "10:00 AM - 12:00 PM",
                    "customer_address": "12th Main, Indiranagar",
                    "payout": 420.0,
                    "status": "awaiting_start_otp"
                }
            ]
        }
    elif role == "mechanic":
        return {
            "role": "Emergency RSA Technician",
            "partner_name": "Ramesh Babu",
            "emergency_sos_dispatched": 4,
            "today_earnings": 3100.0,
            "active_tasks": [
                {
                    "job_id": "MECH-SOS-22",
                    "type": "Battery Jumpstart & Alternator Check",
                    "location": "Near Dell Ring Road, Domlur",
                    "estimated_arrival": "7 mins",
                    "payout": 350.0
                }
            ]
        }
    elif role == "ev_operator":
        return {
            "role": "EV Station CPO / Operator",
            "operator_name": "Ai1 FastGrid Bengaluru",
            "managed_stations": 4,
            "total_connectors": 11,
            "uptime_pct": 99.4,
            "energy_dispensed_today_kwh": 348.5,
            "revenue_today_inr": 6795.0,
            "stations_overview": [
                {"name": "Indiranagar Metro Hub", "uptime": 99.2, "active_sessions": 2, "faults": 0},
                {"name": "Forum South Mall Hub", "uptime": 98.7, "active_sessions": 3, "faults": 0},
                {"name": "HSR Sector 1 SuperHub", "uptime": 97.9, "active_sessions": 1, "faults": 0},
                {"name": "Airport NH 44 UltraGrid", "uptime": 99.8, "active_sessions": 2, "faults": 0}
            ]
        }

    return {"error": "Unknown partner role"}
