"""
Ai1 Super App - Travel Provider Adapter (ixigo style)
Handles flights, trains with live PNR, buses, and composite itinerary bundles.
"""

from typing import Dict, List, Any
import random
from backend.database.db import db
from backend.models.schemas import PnrStatus, TravelBooking


class TravelAdapter:
    """
    Unified Travel Engine.
    Simulates GDS flight inventory and Indian Railways IRCTC live PNR status.
    """

    def search_flights(self, origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
        # Filter or return flights
        return [f.model_dump() for f in db.flights]

    def search_trains(self, origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
        return [t.model_dump() for t in db.trains]

    def check_pnr_status(self, pnr: str) -> Dict[str, Any]:
        # Realistic 10-digit PNR simulation
        clean_pnr = pnr.strip()
        return {
            "pnr": clean_pnr,
            "train_number": "20608",
            "train_name": "Mysuru - MGR Chennai Central Vande Bharat",
            "date_of_journey": "Tomorrow",
            "from_station": "SBC (KSR Bengaluru)",
            "to_station": "MAS (MGR Chennai Central)",
            "boarding_point": "SBC",
            "reservation_upto": "MAS",
            "chart_prepared": True,
            "confirmation_probability": 98,
            "passengers": [
                {
                    "passenger_number": 1,
                    "booking_status": "CNF",
                    "current_status": "CNF",
                    "coach": "C4",
                    "berth": "42",
                    "berth_type": "Window"
                },
                {
                    "passenger_number": 2,
                    "booking_status": "CNF",
                    "current_status": "CNF",
                    "coach": "C4",
                    "berth": "43",
                    "berth_type": "Aisle"
                }
            ]
        }

    def search_buses(self, origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
        return [
            {
                "operator": "KSRTC Flybus (Direct Airport to Mysore)",
                "bus_type": "Multi-Axle Volvo AC Sleeper",
                "departure_time": "07:30 AM",
                "arrival_time": "11:00 AM",
                "price": 820.0,
                "rating": 4.8,
                "seats_available": 18
            },
            {
                "operator": "IntrCity SmartBus",
                "bus_type": "AC Sleeper (2+1)",
                "departure_time": "21:30",
                "arrival_time": "06:00 (+1 day)",
                "price": 1150.0,
                "rating": 4.7,
                "seats_available": 7
            }
        ]

    def build_composite_itinerary(self, user_id: str, travel_type: str, origin: str, dest: str, date: str, add_cab: bool, add_insurance: bool) -> Dict[str, Any]:
        base_fare = 5499.0 if travel_type == "flight" else 1450.0
        ticket_ref = f"6E-{random.randint(100, 999)}" if travel_type == "flight" else f"PNR-{random.randint(1000000000, 9999999999)}"

        cab_fare = 750.0 if add_cab else 0.0
        insurance_premium = 79.0 if add_insurance else 0.0
        total_fare = base_fare + cab_fare + insurance_premium

        booking = TravelBooking(
            user_id=user_id,
            travel_type=travel_type,
            title=f"{origin} to {dest} ({travel_type.title()})",
            origin=origin,
            destination=dest,
            date=date,
            total_fare=total_fare,
            ticket_or_pnr=ticket_ref,
            cab_addon_included=add_cab,
            insurance_addon_included=add_insurance,
            status="confirmed"
        )
        db.travel_bookings[booking.id] = booking

        return {
            "booking_id": booking.id,
            "ticket_or_pnr": ticket_ref,
            "total_fare": total_fare,
            "cab_addon_included": add_cab,
            "insurance_addon_included": add_insurance,
            "breakdown": {
                "base_fare": base_fare,
                "cab_pickup": cab_fare,
                "travel_insurance": insurance_premium
            },
            "status": "confirmed"
        }


travel_adapter = TravelAdapter()
