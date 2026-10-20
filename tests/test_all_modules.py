"""
Ai1 Super App - Comprehensive Automated Test Suite
Verifies all 9 core modules, external adapters, cross-module AI orchestrations,
and regulatory compliance constraints.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database.db import db

client = TestClient(app)


def test_01_system_health():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["city"] == "Bengaluru"


def test_02_auth_and_sso():
    # 1. Request OTP
    res = client.post("/api/v1/auth/request-otp", json={"phone": "+91 98765 43210"})
    assert res.status_code == 200
    assert res.json()["demo_hint"] == "123456"

    # 2. Verify OTP
    res = client.post("/api/v1/auth/verify-otp", json={"phone": "+91 98765 43210", "otp": "123456"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    assert token is not None

    # 3. Get profile
    res = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["name"] == "Arjun Sundaram"


def test_03_wallet_and_payments():
    # 1. Check wallet
    res = client.get("/api/v1/wallet")
    assert res.status_code == 200
    w = res.json()
    assert w["balance"] >= 2000.0
    assert w["ai1_coins"] >= 100

    # 2. Top-up
    res = client.post("/api/v1/wallet/top-up", json={"amount": 500.0, "payment_method": "upi"})
    assert res.status_code == 200
    assert res.json()["success"] is True

    # 3. UPI Pay
    res = client.post("/api/v1/wallet/upi-pay", json={
        "target_vpa_or_phone": "rahul@okaxis",
        "amount": 200.0,
        "note": "Lunch share",
        "mpin": "1234"
    })
    assert res.status_code == 200
    assert res.json()["success"] is True

    # 4. Utility Bill Payment
    res = client.post("/api/v1/wallet/bill-payment", json={
        "category": "electricity",
        "biller_name": "BESCOM Bengaluru",
        "consumer_number": "100293848",
        "amount": 450.0
    })
    assert res.status_code == 200
    assert res.json()["status"] == "SUCCESSFUL"


def test_04_quick_commerce():
    # 1. Check pincode
    res = client.get("/api/v1/qc/dark-stores/check-pincode?pincode=560038")
    assert res.status_code == 200
    assert res.json()["serviceable"] is True
    assert res.json()["eta_mins"] <= 15

    # 2. Browse products
    res = client.get("/api/v1/qc/products?category=dairy")
    assert res.status_code == 200
    assert len(res.json()) > 0

    # 3. Cart Checkout
    res = client.post("/api/v1/qc/cart/checkout", json={
        "pincode": "560038",
        "delivery_address": "Indiranagar 12th Main",
        "items": [
            {"product_id": "qc-milk-01", "product_name": "Amul Milk", "unit": "500ml", "price": 28.0, "quantity": 2, "subtotal": 56.0}
        ],
        "use_coins": False
    })
    assert res.status_code == 200
    order_id = res.json()["id"]

    # 4. Live Tracking
    res = client.get(f"/api/v1/qc/orders/{order_id}")
    assert res.status_code == 200
    assert res.json()["status"] == "out_for_delivery"


def test_05_ride_hailing():
    # 1. Ride Fare Estimate
    res = client.post("/api/v1/rides/estimate", json={
        "pickup_address": "Indiranagar",
        "pickup_lat": 12.9784,
        "pickup_lng": 77.6408,
        "drop_address": "MG Road",
        "drop_lat": 12.9756,
        "drop_lng": 77.6066
    })
    assert res.status_code == 200
    options = res.json()
    assert len(options) == 4
    assert options[0]["category"] == "bike"

    # 2. Book Ride
    res = client.post("/api/v1/rides/book", json={
        "category": "cab_prime",
        "pickup_address": "Indiranagar",
        "pickup_lat": 12.9784,
        "pickup_lng": 77.6408,
        "drop_address": "MG Road",
        "drop_lat": 12.9756,
        "drop_lng": 77.6066,
        "use_coins": False
    })
    assert res.status_code == 200
    ride = res.json()
    assert ride["status"] == "driver_assigned"

    # 3. Live Driver Tracking
    res = client.get(f"/api/v1/rides/{ride['id']}/live")
    assert res.status_code == 200
    assert res.json()["driver_lat"] is not None

    # 4. Trigger SOS
    res = client.post(f"/api/v1/rides/{ride['id']}/sos")
    assert res.status_code == 200
    assert res.json()["sos_status"] == "ACTIVE"


def test_06_home_services():
    # 1. Categories
    res = client.get("/api/v1/services/categories")
    assert res.status_code == 200
    assert len(res.json()) >= 4

    # 2. Items
    res = client.get("/api/v1/services/items")
    assert res.status_code == 200
    assert len(res.json()) >= 4

    # 3. Book Service
    res = client.post("/api/v1/services/book", json={
        "service_id": "srv-ac-foam",
        "scheduled_date": "Tomorrow",
        "time_slot": "10:00 AM - 12:00 PM",
        "address": "Indiranagar 100ft Road"
    })
    assert res.status_code == 200
    booking_id = res.json()["id"]

    # 4. Verify Start OTP
    res = client.post(f"/api/v1/services/bookings/{booking_id}/verify-otp?otp=5892")
    assert res.status_code == 200
    assert res.json()["status"] == "in_progress"


def test_07_mechanic_and_rsa():
    # 1. Packages
    res = client.get("/api/v1/mechanic/packages")
    assert res.status_code == 200
    assert len(res.json()) >= 2

    # 2. Emergency Breakdown SOS
    res = client.post("/api/v1/mechanic/breakdown-sos", json={
        "emergency_type": "flat_tyre",
        "vehicle_type": "car",
        "location_address": "Near Domlur Flyover",
        "lat": 12.9609,
        "lng": 77.6387
    })
    assert res.status_code == 200
    job = res.json()
    assert job["is_emergency_sos"] is True

    # 3. Approve Estimate
    res = client.post(f"/api/v1/mechanic/jobs/{job['id']}/approve-estimate")
    assert res.status_code == 200
    assert res.json()["status"] == "repairing"


def test_08_travel():
    # 1. Flight search
    res = client.get("/api/v1/travel/flights/search")
    assert res.status_code == 200
    assert len(res.json()) >= 3

    # 2. Train PNR check
    res = client.get("/api/v1/travel/trains/pnr?pnr=8423451290")
    assert res.status_code == 200
    pnr_data = res.json()
    assert pnr_data["pnr"] == "8423451290"
    assert pnr_data["confirmation_probability"] >= 90

    # 3. Composite Itinerary Build
    res = client.post("/api/v1/travel/itinerary/build", json={
        "travel_type": "flight",
        "origin": "BLR",
        "destination": "DEL",
        "date": "Tomorrow",
        "add_airport_cab": True,
        "add_travel_insurance": True
    })
    assert res.status_code == 200
    assert res.json()["booking_details"]["cab_addon_included"] is True


def test_09_insurance():
    # 1. Quotes
    res = client.get("/api/v1/insurance/quotes?type=health")
    assert res.status_code == 200
    quotes = res.json()
    assert len(quotes) >= 2

    # Top-up wallet to cover premium
    client.post("/api/v1/wallet/top-up", json={"amount": 10000.0, "payment_method": "upi"})

    # 2. Buy Policy
    res = client.post("/api/v1/insurance/buy", json={
        "quote_id": "INS-HLTH-HDFC",
        "insured_name": "Arjun Sundaram",
        "insured_pan_or_aadhaar": "ABCDE1234F"
    })
    assert res.status_code == 200
    policy = res.json()
    assert policy["insurer_name"] == "HDFC ERGO"
    assert policy["status"] == "active"

    # 3. Vault
    res = client.get("/api/v1/insurance/vault")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # 4. Cashless Claim
    res = client.post("/api/v1/insurance/claim", json={
        "policy_id": policy["id"],
        "hospital_or_garage": "Manipal Hospital Old Airport Rd",
        "incident_date": "2026-10-20",
        "estimated_amount": 25000.0,
        "claim_reason": "Emergency Daycare Procedure"
    })
    assert res.status_code == 200
    assert res.json()["status"] == "UNDER_EXAMINATION"


def test_10_ev_charging_realtime():
    # 1. Fetch stations with filters
    res = client.get("/api/v1/ev/stations?min_power=50.0")
    assert res.status_code == 200
    stations = res.json()
    assert len(stations) >= 2

    stn = stations[0]
    conn = stn["connectors"][0]

    # 2. Start Session
    res = client.post("/api/v1/ev/sessions/start", json={
        "station_id": stn["id"],
        "connector_id": conn["id"],
        "target_soc": 85
    })
    assert res.status_code == 200
    session_id = res.json()["session_id"]

    # 3. Live Telemetry
    res = client.get(f"/api/v1/ev/sessions/{session_id}/live")
    assert res.status_code == 200
    live = res.json()
    assert live["status"] == "charging"
    assert live["energy_delivered_kwh"] > 0

    # 4. Stop Session
    res = client.post("/api/v1/ev/sessions/stop", json={"session_id": session_id})
    assert res.status_code == 200
    assert res.json()["status"] == "completed"

    # 5. Reserve Connector (15-min lock)
    res = client.post("/api/v1/ev/reservations", json={
        "station_id": stn["id"],
        "connector_id": conn["id"],
        "hold_minutes": 15
    })
    assert res.status_code == 200
    assert res.json()["reservation"]["hold_minutes"] == 15

    # 6. EV Route Planner
    res = client.post("/api/v1/ev/route-planner", json={
        "origin": "Indiranagar",
        "destination": "Kempegowda International Airport",
        "current_battery_pct": 5
    })
    assert res.status_code == 200
    route = res.json()
    assert route["needs_charging_stop"] is True


def test_11_ai_assistant_multilingual_orchestration():
    # 1. Cross-Module: Cab to Airport + Travel Insurance
    res = client.post("/api/v1/assistant/chat", json={
        "message": "Book a cab to the airport and add travel insurance",
        "language": "en"
    })
    assert res.status_code == 200
    data = res.json()
    proposal = data["action_proposal"]
    assert proposal is not None
    assert proposal["action_type"] == "bundle_cab_and_insurance"
    assert proposal["total_cost"] == 929.0

    # 2. Confirm & Commit Action (Two-phase commit)
    res = client.post("/api/v1/assistant/confirm-action", json={
        "proposal_payload": proposal["payload"],
        "mpin_or_biometric": "1234"
    })
    assert res.status_code == 200
    assert res.json()["success"] is True

    # 3. Multilingual Intent in Hindi
    res = client.post("/api/v1/assistant/chat", json={
        "message": "दूध और ब्रेड ऑर्डर करो",
        "language": "hi"
    })
    assert res.status_code == 200
    assert res.json()["action_proposal"] is not None

    # 4. Multilingual Intent in Kannada
    res = client.post("/api/v1/assistant/chat", json={
        "message": "ನನಗೆ ವಿಮಾನ ನಿಲ್ದಾಣಕ್ಕೆ ಕ್ಯಾಬ್ ಬೇಕು",
        "language": "kn"
    })
    assert res.status_code == 200
    assert "ದೃಢೀಕರಿಸಿ" in res.json()["reply_text"] or "ಕ್ಯಾಬ್" in res.json()["reply_text"]


def test_12_partner_and_admin():
    # 1. Partner Dashboards (Rider, Driver, EV Operator)
    res = client.get("/api/v1/partner/dashboard?role=rider")
    assert res.status_code == 200
    assert res.json()["rating"] >= 4.5

    res = client.get("/api/v1/partner/dashboard?role=ev_operator")
    assert res.status_code == 200
    assert res.json()["uptime_pct"] >= 99.0

    # 2. Admin Metrics & Compliance
    res = client.get("/api/v1/admin/metrics")
    assert res.status_code == 200
    assert res.json()["platform_status"] == "OPERATIONAL"

    # 3. Audit Logs
    res = client.get("/api/v1/admin/audit-logs")
    assert res.status_code == 200
    assert len(res.json()) >= 4
