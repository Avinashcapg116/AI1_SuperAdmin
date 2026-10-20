"""
Ai1 Super App - In-Memory & Storage Repository with Spatial Capabilities
"""

import math
from typing import Dict, List, Optional, Any
from backend.models.schemas import (
    User, Wallet, WalletTransaction, DarkStore, Product, Order,
    ServiceItem, ServiceBooking, Ride, MechanicPackage, MechanicJob,
    Flight, Train, TravelBooking, Policy, EvStation, EvConnector, EvSession,
    AuditLogEntry
)
from backend.database.seed_data import (
    SEED_DARK_STORES, SEED_PRODUCTS, SEED_EV_STATIONS, SEED_SERVICES,
    SEED_MECHANIC_PACKAGES, SEED_FLIGHTS, SEED_TRAINS, SEED_INSURANCE_QUOTES,
    SEED_DEFAULT_USER
)


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points on the earth in km."""
    R = 6371.0  # Earth's radius in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon / 2) * math.sin(dLon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


class Database:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.wallets: Dict[str, Wallet] = {}
        self.transactions: List[WalletTransaction] = []
        self.dark_stores: Dict[str, DarkStore] = {}
        self.products: Dict[str, Product] = {}
        self.orders: Dict[str, Order] = {}
        self.service_items: Dict[str, ServiceItem] = {}
        self.service_bookings: Dict[str, ServiceBooking] = {}
        self.rides: Dict[str, Ride] = {}
        self.mechanic_packages: Dict[str, MechanicPackage] = {}
        self.mechanic_jobs: Dict[str, MechanicJob] = {}
        self.flights: List[Flight] = []
        self.trains: List[Train] = []
        self.travel_bookings: Dict[str, TravelBooking] = {}
        self.insurance_quotes: Dict[str, Dict[str, Any]] = {}
        self.policies: Dict[str, Policy] = {}
        self.ev_stations: Dict[str, EvStation] = {}
        self.ev_sessions: Dict[str, EvSession] = {}
        self.ev_reservations: Dict[str, Dict[str, Any]] = {}
        self.audit_logs: List[AuditLogEntry] = []
        
        self.seed_database()

    def seed_database(self):
        # 1. Seed Default User
        user = User(**SEED_DEFAULT_USER)
        self.users[user.id] = user
        self.users[user.phone] = user  # Index by phone for fast lookup

        # 2. Seed Default Wallet
        wallet = Wallet(
            user_id=user.id,
            balance=3500.0,
            ai1_coins=250,
            upi_vpa="9876543210@ai1",
            kyc_level="full_kyc"
        )
        self.wallets[user.id] = wallet

        # 3. Seed Dark Stores & Products
        for ds in SEED_DARK_STORES:
            self.dark_stores[ds["id"]] = DarkStore(**ds)

        for prod in SEED_PRODUCTS:
            self.products[prod["id"]] = Product(**prod)

        # 4. Seed Home Services
        for srv in SEED_SERVICES:
            self.service_items[srv["id"]] = ServiceItem(**srv)

        # 5. Seed Mechanic Packages
        for mp in SEED_MECHANIC_PACKAGES:
            self.mechanic_packages[mp["id"]] = MechanicPackage(**mp)

        # 6. Seed Travel
        for f in SEED_FLIGHTS:
            self.flights.append(Flight(**f))
        for t in SEED_TRAINS:
            self.trains.append(Train(**t))

        # 7. Seed Insurance
        for q in SEED_INSURANCE_QUOTES:
            self.insurance_quotes[q["quote_id"]] = q

        # 8. Seed EV Stations
        for stn_data in SEED_EV_STATIONS:
            connectors = [EvConnector(**c) for c in stn_data["connectors"]]
            stn_copy = dict(stn_data)
            stn_copy["connectors"] = connectors
            stn = EvStation(**stn_copy)
            self.ev_stations[stn.id] = stn

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def get_user_by_phone(self, phone: str) -> Optional[User]:
        # Normalize phone
        clean_phone = phone.replace(" ", "").replace("-", "")
        for u in self.users.values():
            if u.phone.replace(" ", "").replace("-", "") == clean_phone:
                return u
        return None

    def get_or_create_wallet(self, user_id: str) -> Wallet:
        if user_id not in self.wallets:
            u = self.get_user_by_id(user_id)
            phone_num = u.phone if u else "user"
            clean_phone = phone_num.replace("+91", "").replace(" ", "")
            self.wallets[user_id] = Wallet(
                user_id=user_id,
                balance=2000.0,
                ai1_coins=100,
                upi_vpa=f"{clean_phone}@ai1"
            )
        return self.wallets[user_id]


db = Database()
