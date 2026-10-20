"""
Ai1 Super App - Domain Data Models & Pydantic Schemas
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


# ==========================================
# 1. USER & AUTH
# ==========================================
class UserAddress(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    label: str = "Home"  # Home, Work, Other
    street: str
    city: str = "Bengaluru"
    pincode: str = "560001"
    lat: float = 12.9716
    lng: float = 77.5946
    is_default: bool = False


class UserVehicle(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    vehicle_number: str
    make: str
    model: str
    vehicle_type: str = "car"  # 2w, car, auto
    is_ev: bool = True
    battery_capacity_kwh: Optional[float] = 40.5
    supported_connectors: List[str] = ["CCS2", "Type 2"]


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    phone: str
    name: str = "Guest User"
    email: Optional[str] = None
    preferred_language: str = "en"  # en, hi, kn, ta, te
    role: str = "customer"  # customer, partner_rider, partner_driver, partner_pro, partner_mechanic, partner_ev, admin
    is_kyc_verified: bool = False
    mpin_set: bool = False
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    addresses: List[UserAddress] = []
    vehicles: List[UserVehicle] = []


class RequestOtpRequest(BaseModel):
    phone: str
    role: Optional[str] = "customer"


class VerifyOtpRequest(BaseModel):
    phone: str
    otp: str
    name: Optional[str] = None
    role: Optional[str] = "customer"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User


# ==========================================
# 2. WALLET & PAYMENTS
# ==========================================
class WalletTransaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    wallet_id: str
    type: str  # credit, debit, cashback, transfer
    amount: float
    coins_earned: int = 0
    coins_used: int = 0
    reference_module: str  # qc, rides, home_services, mechanic, travel, insurance, ev, upi, bill_pay
    reference_id: str
    description: str
    status: str = "completed"  # pending, completed, failed
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class Wallet(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    balance: float = 2500.0  # Starter seed balance for demo
    ai1_coins: int = 150     # 1 Coin = ₹1 redemption value
    upi_vpa: str             # e.g., "9876543210@ai1"
    is_frozen: bool = False
    kyc_level: str = "full_kyc"  # min_kyc, full_kyc


class TopUpRequest(BaseModel):
    amount: float
    payment_method: str = "upi"  # upi, netbanking, card


class UpiPayRequest(BaseModel):
    target_vpa_or_phone: str
    amount: float
    note: Optional[str] = "Ai1 UPI Payment"
    use_coins: bool = False
    mpin: Optional[str] = "1234"


class QrPayRequest(BaseModel):
    qr_data: str
    amount: float
    note: Optional[str] = "Ai1 Merchant QR Pay"
    use_coins: bool = False


class BillPayRequest(BaseModel):
    category: str  # mobile, electricity, fastag, dth, gas
    biller_name: str
    consumer_number: str
    amount: float
    use_coins: bool = False


# ==========================================
# 3. QUICK COMMERCE
# ==========================================
class DarkStore(BaseModel):
    id: str
    name: str
    pincode: str
    area: str
    lat: float
    lng: float
    is_active: bool = True
    delivery_eta_mins: int = 12


class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float
    mrp: float
    unit: str  # "500 ml", "1 kg", "Pack of 6"
    image_url: str
    in_stock: bool = True
    stock_count: int = 100
    rating: float = 4.8
    tags: List[str] = []


class OrderItem(BaseModel):
    product_id: str
    product_name: str
    unit: str
    price: float
    quantity: int
    subtotal: float


class CheckoutRequest(BaseModel):
    pincode: str = "560038"
    delivery_address: str
    items: List[OrderItem]
    coupon_code: Optional[str] = None
    use_coins: bool = False
    allow_substitutions: bool = True


class Order(BaseModel):
    id: str = Field(default_factory=lambda: "QC-" + str(uuid.uuid4())[:8].upper())
    user_id: str
    store_id: str
    items: List[OrderItem]
    subtotal: float
    delivery_fee: float = 0.0
    discount: float = 0.0
    coins_used: int = 0
    total_amount: float
    pincode: str
    delivery_address: str
    slot_eta_mins: int = 12
    rider_name: str = "Suresh Kumar"
    rider_phone: str = "+91 98450 11223"
    rider_lat: float = 12.9780
    rider_lng: float = 77.6400
    status: str = "out_for_delivery"  # placed, packed, out_for_delivery, delivered
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ==========================================
# 4. HOME SERVICES
# ==========================================
class ServiceItem(BaseModel):
    id: str
    title: str
    category: str  # cleaning, salon, ac_repair, plumbing, electrician, painting
    description: str
    duration_mins: int
    price: float
    rating: float = 4.9
    review_count: int = 1420
    image_url: str
    warranty_days: int = 30
    addons: List[Dict[str, Any]] = []


class BookServiceRequest(BaseModel):
    service_id: str
    scheduled_date: str
    time_slot: str  # "10:00 AM - 12:00 PM"
    address: str
    addons_selected: List[str] = []
    use_coins: bool = False


class ServiceBooking(BaseModel):
    id: str = Field(default_factory=lambda: "HS-" + str(uuid.uuid4())[:8].upper())
    user_id: str
    service_id: str
    service_title: str
    category: str
    scheduled_slot: str
    address: str
    total_price: float
    coins_used: int = 0
    status: str = "confirmed"  # confirmed, pro_assigned, in_progress, completed
    pro_name: str = "Rajesh Sharma (Urban Master Pro)"
    pro_phone: str = "+91 98765 43210"
    pro_rating: float = 4.92
    start_otp: str = "4821"
    post_service_invoice_url: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ==========================================
# 5. RIDE HAILING
# ==========================================
class RideEstimateOption(BaseModel):
    category: str  # bike, auto, cab_mini, cab_prime
    title: str
    eta_mins: int
    base_fare: float
    surge_multiplier: float = 1.0
    final_fare: float
    capacity: int
    co2_saved_kg: float = 0.0


class RideEstimateRequest(BaseModel):
    pickup_address: str
    pickup_lat: float
    pickup_lng: float
    drop_address: str
    drop_lat: float
    drop_lng: float


class BookRideRequest(BaseModel):
    category: str
    pickup_address: str
    pickup_lat: float
    pickup_lng: float
    drop_address: str
    drop_lat: float
    drop_lng: float
    use_coins: bool = False


class Ride(BaseModel):
    id: str = Field(default_factory=lambda: "RIDE-" + str(uuid.uuid4())[:8].upper())
    user_id: str
    category: str
    pickup_address: str
    pickup_lat: float
    pickup_lng: float
    drop_address: str
    drop_lat: float
    drop_lng: float
    fare: float
    surge_multiplier: float = 1.0
    driver_name: str = "Manjunath Gowda"
    driver_phone: str = "+91 94480 98765"
    vehicle_number: str = "KA 01 MJ 4242"
    vehicle_model: str = "Tata Nexon EV"
    driver_rating: float = 4.95
    driver_lat: float = 12.9730
    driver_lng: float = 77.5990
    otp: str = "7291"
    status: str = "driver_assigned"  # searching, driver_assigned, arrived, in_transit, completed
    sos_active: bool = False
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ==========================================
# 6. MECHANIC SOLUTIONS & RSA
# ==========================================
class MechanicPackage(BaseModel):
    id: str
    title: str
    vehicle_type: str  # car, bike
    includes: List[str]
    price: float
    duration_hours: int = 3


class BookMechanicRequest(BaseModel):
    package_id: str
    vehicle_number: str
    vehicle_model: str
    is_doorstep: bool = True
    address: str
    scheduled_date: str


class BreakdownSosRequest(BaseModel):
    emergency_type: str  # flat_tyre, battery_dead, towing, accident, engine_overheat
    vehicle_type: str
    location_address: str
    lat: float
    lng: float
    notes: Optional[str] = None


class MechanicJob(BaseModel):
    id: str = Field(default_factory=lambda: "MECH-" + str(uuid.uuid4())[:8].upper())
    user_id: str
    service_type: str
    is_emergency_sos: bool = False
    vehicle_model: str
    location_address: str
    technician_name: str = "Ramesh Babu (Certified Master Tech)"
    technician_phone: str = "+91 97400 33445"
    technician_lat: float = 12.9750
    technician_lng: float = 77.6010
    estimated_cost: float
    is_estimate_approved: bool = False
    status: str = "technician_dispatched"  # dispatched, inspecting, awaiting_approval, repairing, completed
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ==========================================
# 7. TRAVEL (ixigo Style)
# ==========================================
class Flight(BaseModel):
    flight_number: str
    airline: str  # IndiGo, Air India, Akasa
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    duration: str
    price: float
    refundable: bool = True
    seats_left: int = 5


class Train(BaseModel):
    train_number: str
    train_name: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    classes: List[Dict[str, Any]]  # [{"class": "3A", "price": 1450, "status": "AVAILABLE-42"}]


class PnrStatus(BaseModel):
    pnr: str
    train_number: str
    train_name: str
    date_of_journey: str
    from_station: str
    to_station: str
    passengers: List[Dict[str, Any]]
    chart_prepared: bool = False
    confirmation_probability: int = 95


class TravelBooking(BaseModel):
    id: str = Field(default_factory=lambda: "TRV-" + str(uuid.uuid4())[:8].upper())
    user_id: str
    travel_type: str  # flight, train, bus, hotel
    title: str
    origin: str
    destination: str
    date: str
    total_fare: float
    ticket_or_pnr: str
    cab_addon_included: bool = False
    insurance_addon_included: bool = False
    status: str = "confirmed"
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class TripItineraryRequest(BaseModel):
    travel_type: str
    origin: str
    destination: str
    date: str
    passengers: int = 1
    add_airport_cab: bool = True
    add_travel_insurance: bool = True


# ==========================================
# 8. INSURANCE
# ==========================================
class InsuranceQuote(BaseModel):
    quote_id: str
    type: str  # health, motor, travel, term, home
    insurer_name: str  # HDFC ERGO, ICICI Lombard, Star Health, Care
    plan_name: str
    cover_amount: float
    premium_annual: float
    key_features: List[str]
    cashless_hospitals_or_garages: int = 12000
    irda_claim_settlement_ratio: float = 98.6


class Policy(BaseModel):
    id: str = Field(default_factory=lambda: "POL-" + str(uuid.uuid4())[:8].upper())
    user_id: str
    policy_type: str
    insurer_name: str
    plan_name: str
    policy_number: str
    sum_insured: float
    premium_paid: float
    start_date: str
    expiry_date: str
    free_look_ends: str
    status: str = "active"  # active, claim_in_review, expired
    document_pdf_mock: str = "/docs/policy_certificate.pdf"


class BuyPolicyRequest(BaseModel):
    quote_id: str
    insured_name: str
    insured_pan_or_aadhaar: str
    use_coins: bool = False


class ClaimRequest(BaseModel):
    policy_id: str
    hospital_or_garage: str
    incident_date: str
    estimated_amount: float
    claim_reason: str


# ==========================================
# 9. REAL-TIME EV CHARGING
# ==========================================
class EvConnector(BaseModel):
    id: str
    connector_type: str  # CCS2, Type 2, CHAdeMO, Bharat DC-001, 3-pin 16A
    power_kw: float      # e.g., 60.0 (DC Fast), 22.0 (AC Type 2)
    current_type: str    # DC, AC
    status: str          # available, occupied, faulted, offline
    tariff_per_kwh: float = 18.5
    idle_fee_per_min: float = 2.0
    last_heartbeat: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class EvStation(BaseModel):
    id: str
    name: str
    operator_name: str  # Tata Power EZ Charge, Zeon, Jio-bp pulse, Ai1 FastGrid
    address: str
    pincode: str
    lat: float
    lng: float
    connectors: List[EvConnector]
    is_24x7: bool = True
    amenities: List[str] = ["Cafe", "Restroom", "Wi-Fi", "EV Lounge"]
    reliability_score: float = 98.4  # Percentage uptime / success
    last_status_update: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class EvSession(BaseModel):
    id: str = Field(default_factory=lambda: "EV-SES-" + str(uuid.uuid4())[:8].upper())
    user_id: str
    station_id: str
    station_name: str
    connector_id: str
    connector_type: str
    power_kw: float
    energy_delivered_kwh: float = 0.0
    current_power_kw: float = 0.0
    soc_current_pct: int = 28
    soc_target_pct: int = 85
    duration_mins: int = 0
    total_cost: float = 0.0
    status: str = "charging"  # charging, paused, completed, stopped
    started_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class StartSessionRequest(BaseModel):
    station_id: str
    connector_id: str
    target_soc: int = 80


class StopSessionRequest(BaseModel):
    session_id: str


class ReserveConnectorRequest(BaseModel):
    station_id: str
    connector_id: str
    hold_minutes: int = 15


class CrowdsourceReportRequest(BaseModel):
    station_id: str
    connector_id: Optional[str] = None
    is_working: bool
    rating: int = 5
    comment: Optional[str] = None


class EvRoutePlanRequest(BaseModel):
    origin: str
    destination: str
    current_battery_pct: int = 40
    vehicle_battery_capacity_kwh: float = 40.5
    range_full_km: float = 312.0


# ==========================================
# 10. AI ASSISTANT
# ==========================================
class ActionProposal(BaseModel):
    action_type: str  # "bundle_cab_and_insurance", "order_grocery", "pay_upi", "book_service"
    title: str
    description: str
    breakdown: List[Dict[str, Any]]
    total_cost: float
    requires_confirmation: bool = True
    payload: Dict[str, Any]


class AssistantChatRequest(BaseModel):
    message: str
    language: str = "en"  # en, hi, kn, ta, te
    context_module: Optional[str] = None


class AssistantChatResponse(BaseModel):
    reply_text: str
    language: str
    suggested_chips: List[str] = []
    action_proposal: Optional[ActionProposal] = None
    direct_screen_redirect: Optional[str] = None


class AssistantConfirmRequest(BaseModel):
    proposal_payload: Dict[str, Any]
    mpin_or_biometric: str = "1234"


class ProactiveSuggestion(BaseModel):
    id: str
    module: str
    title: str
    subtitle: str
    action_text: str
    action_route: str
    accent_badge: str


# ==========================================
# 11. AUDIT & ADMIN
# ==========================================
class AuditLogEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    user_id: Optional[str] = None
    action: str
    module: str
    details: Dict[str, Any]
    ip_address: str = "127.0.0.1"
