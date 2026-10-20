# 🇮🇳 Ai1 ("All in One") — India-First Super App

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.13-E92063?logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9.4-199900?logo=leaflet&logoColor=white)](https://leafletjs.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Compliance](https://img.shields.io/badge/Compliance-RBI%20|%20IRDAI%20|%20DPDP-success)](docs/compliance)

**Ai1** is an India-first super app that unifies **Quick Commerce, Home Services, Mobility, Travel, Payments, Insurance, and Real-Time EV Charging** on a single mobile-first platform, powered by an intelligent **Multilingual Voice & Chat AI Assistant**.

---

## 🌟 Key Highlights & Modules

| Module | Real-World Benchmark | What's Built & Working |
| :--- | :--- | :--- |
| **1. Quick Commerce** | Zepto / Blinkit / Instamart | Dark stores by pincode (Indiranagar, Koramangala, HSR, Whitefield), 10-15m promise, live rider GPS tracking, coupons, and 1-tap "Usual Basket" reordering. |
| **2. Ride Hailing** | Rapido / Ola / Uber | Bike, Auto, Cab Mini, and Prime EV Sedan; dynamic surge pricing; driver assignment simulation; live moving GPS marker; SOS alert & trip sharing. |
| **3. Real-Time EV Charging** | Tata Power / Zeon / Jio-bp | Interactive Leaflet/OSM map with live connector status (CCS2, Type 2, CHAdeMO, Bharat DC, 3-pin), power ratings (22kW-150kW), 15-min connector hold, remote start/stop session screen with live kWh meter, crowdsourced reports, and EV route planner. |
| **4. Home Services** | Urban Company | AC servicing, deep cleaning, electricians, salon; package add-ons; slot booking; pro matching; OTP-verified start; post-service digital invoice. |
| **5. Mechanic & RSA** | GoMechanic / ReadyAssist | Periodic car/bike servicing, doorstep repairs, and 1-tap Emergency Breakdown SOS (flat tyre, battery jumpstart, towing, overheating) with upfront estimate approval. |
| **6. Travel** | ixigo / MakeMyTrip | Flights search, IRCTC live train PNR status lookup (with coach/seat and confirmation probability), buses, and composite itinerary bundles (flight + cab + travel insurance). |
| **7. Insurance Vault** | PolicyBazaar / Acko | Health, motor, travel, term, and home insurance comparison; 1-click KYC buy flow; Policy Vault with 15-day IRDAI Free-Look countdown; paperless cashless claims. |
| **8. Payments & Wallet** | Paytm / PhonePe / GPay | RBI-compliant unified Ai1 Wallet, UPI transfer (`user@ai1`), BharatQR scan & pay, utility recharges (BESCOM, NHAI FASTag), and Ai1 Coins loyalty engine. |
| **9. Ai1 Voice Assistant** | Core Differentiator | Multilingual AI supporting **English, Hindi (हिंदी), Kannada (ಕನ್ನಡ), Tamil (தமிழ்), and Telugu (తెలుగు)** with Web Speech recognition, Indic NLU, proactive suggestions, and strict **Two-Phase Action Confirmation**. |
| **10. Role Apps & Admin** | Gig Economy & Operator | Role toggles for Delivery Riders, Cab Drivers, Home Pros, Emergency Mechanics, EV Station Operators, and Platform Admin with DPDP compliance audit log & data export. |

---

## 🚀 One-Command Local Startup

### Option A: Using the Launcher Script (Recommended)

```bash
cd /Users/avinashanilpathak/.gemini/antigravity/scratch/ai1
./start.sh
```

This single command will:
1. Verify the Python virtual environment and dependencies.
2. Execute the comprehensive 12-test automated verification suite.
3. Start the unified FastAPI server and PWA on **`http://localhost:8000`**.

### Option B: Using Docker Compose

```bash
docker compose up --build
```
Spins up PostgreSQL + PostGIS, Redis 7, and the Ai1 Super App container on port 8000.

---

## 🧭 Live Demo Script & Walkthrough

Once running, navigate to `http://localhost:8000`:

### 1. Test the AI Assistant Cross-Module Actions
Click the **"Ask Ai1"** floating button or enter queries in the top search bar:
- **Scenario A (Airport Cab + Travel Insurance)**:  
  *Query*: `"Book a cab to the airport and add travel insurance"`  
  *Behavior*: Generates a bundled action proposal combining an Ai1 Prime EV ride (₹850) and Tata AIG Domestic Travel Shield (₹79). Displays the itemized proposal card with a single "Confirm & Pay" button.
- **Scenario B (Groceries + FASTag Recharge)**:  
  *Query*: `"Order milk and bread and recharge my FASTag for 500"`  
  *Behavior*: Bundles an 11-minute grocery delivery with an instant NHAI FASTag wallet top-up.
- **Scenario C (EV Charger Hold + AC Home Servicing)**:  
  *Query*: `"Find a fast EV charger near Indiranagar and book an AC servicing slot for tomorrow"`  
  *Behavior*: Locks a 60kW CCS2 connector for 15 minutes at Indiranagar Metro and schedules a foam AC service pro for tomorrow morning.
- **Multilingual Support**: Switch the language dropdown to **हिंदी** or **ಕನ್ನಡ** and speak or type Indic instructions.

### 2. Test Quick Commerce (10-15m Delivery)
1. Select the **Quick Commerce** tab.
2. Click **"1-Tap Add Usual Basket"** (Milk + Whole Wheat Bread + Eggs).
3. Open Cart and click **"Confirm & Pay"**.
4. Observe the active delivery strip: Suresh Kumar is dispatched from the Indiranagar Dark Store with an 11-minute ETA.

### 3. Test Real-Time EV Charging & Route Planner
1. Select the **EV Charging** tab to open the interactive map of Bengaluru.
2. Click on the **Tata Power EZ Charge (Indiranagar Metro)** marker or card.
3. Click **"Start"** on the CCS2 (60 kW) connector.
4. Watch the live telemetry screen updating real-time kWh energy delivered, battery SoC %, and running tariff.
5. Click **"Stop Charging & Deduct from Wallet"** to complete the session.
6. Click **"🗺️ Route Planner"** to simulate an EV trip from Indiranagar to Kempegowda Airport with battery consumption calculations.

### 4. Test Ride Hailing with Surge & SOS
1. Select the **Ride Hailing** tab.
2. Click **"Get Fare Estimates"** to compare Bike (₹82), Auto (₹126), Go Mini (₹192), and Prime EV (₹242).
3. Book **Ai1 Prime EV**. A live driver card is assigned (Manjunath Gowda in a Tata Nexon EV, start OTP `7291`).
4. Click **"🚨 Emergency SOS"** to verify dispatch alerts to Bengaluru Police (112) and emergency contacts.

### 5. Test IRCTC Live Train PNR Lookup
1. Select the **Travel & PNR** tab.
2. Enter PNR `8423451290` and click **"Check"**.
3. Displays live status for the Mysuru-Chennai Vande Bharat with confirmed window berth in Coach C4 and 98% confirmation probability.

### 6. Test Partner Console & Platform Admin
1. Click the top role pill **"Role: Customer ▾"** to switch to the **Partner Console**.
2. Toggle between **Delivery Rider**, **Cab Driver**, and **EV Station Operator** (showing 99.4% uptime and 348.5 kWh energy dispensed).
3. Switch role again to **Platform Admin** to view the live GMV indicators, compliance scores, and click **"Export DPDP Data"** to download personal data per DPDP Act 2023.

---

## 🏛️ System Architecture

```
                                      ┌─────────────────────────────────────┐
                                      │   Ai1 Mobile-First PWA Client       │
                                      │  (Customer / Partner / Admin Views) │
                                      └──────────────────┬──────────────────┘
                                                         │ HTTP / WebSockets
                                      ┌──────────────────▼──────────────────┐
                                      │     FastAPI API Gateway & Router    │
                                      │     OpenAPI Swagger (/docs)         │
                                      └──────────────────┬──────────────────┘
                                                         │
               ┌─────────────────────────────────────────┼─────────────────────────────────────────┐
               │                                         │                                         │
    ┌──────────▼──────────┐                   ┌──────────▼──────────┐                   ┌──────────▼──────────┐
    │ Quick Commerce &    │                   │ Mobility & Realtime │                   │ Payments, Loyalty   │
    │ Home Services       │                   │ EV SmartGrid        │                   │ & Insurance Vault   │
    └──────────┬──────────┘                   └──────────┬──────────┘                   └──────────┬──────────┘
               │                                         │                                         │
               └─────────────────────────────────────────┼─────────────────────────────────────────┘
                                                         │
                                      ┌──────────────────▼──────────────────┐
                                      │    Cross-Module Async Event Bus     │
                                      │    (Two-Phase Action Protocol)      │
                                      └──────────────────┬──────────────────┘
                                                         │
       ┌───────────────────────────────┬─────────────────┴─────────────┬───────────────────────────────┐
       │                               │                               │                               │
┌──────▼──────┐                 ┌──────▼──────┐                 ┌──────▼──────┐                 ┌──────▼──────┐
│  Payments   │                 │ EV Charging │                 │    Travel   │                 │     SMS     │
│   Adapter   │                 │   Adapter   │                 │   Adapter   │                 │   Adapter   │
│ (UPI/Bharat)│                 │(OCPI/OCPP/  │                 │(GDS & IRCTC │                 │(DLT/Gupshup/│
│             │                 │ OpenCharge) │                 │     Sim)    │                 │    MSG91)   │
└─────────────┘                 └─────────────┘                 └─────────────┘                 └─────────────┘
```

---

## 🔌 Adapter Pattern & Production Migration Roadmap

All external integrations are strictly isolated behind abstract provider interfaces. Replacing mocks with production APIs requires updating only the adapter file:

| Adapter File | Mock Implementation | Real Production Target | Migration Steps |
| :--- | :--- | :--- | :--- |
| `backend/adapters/payment_adapter.py` | `MockUpiPaymentAdapter` | **Razorpay / PhonePe / NPCI UPI** | Swap `create_upi_intent` with PhonePe B2B Merchant API (`/v3/charge`) or Razorpay UPI intent SDK. |
| `backend/adapters/ev_charging_adapter.py` | `SimulatedChargingAdapter` | **OCPI 2.2.1 / OCPP 1.6J Central System** | Connect `OcppCentralSystemAdapter` to charger hardware WebSockets or bridge to operator OCPI hubs (Tata Power, Fortum). |
| `backend/adapters/map_adapter.py` | `OpenStreetMapLeafletAdapter` | **Google Maps / Mapbox APIs** | Inject `GOOGLE_MAPS_API_KEY` into `calculate_eta_and_distance` and Directions API. |
| `backend/adapters/travel_adapter.py` | `MockTravelProvider` | **Amadeus GDS & IRCTC Partner API** | Point `search_flights` to Amadeus Flight Offers Search API and `check_pnr_status` to IRCTC Connect API. |
| `backend/adapters/insurance_adapter.py` | `MockInsurerAggregator` | **HDFC ERGO & ICICI Lombard APIs** | Implement B2B insurance quote & policy issuance endpoints via insurer SOAP/REST gateways. |
| `backend/adapters/sms_adapter.py` | `SmsAdapter` | **Gupshup / MSG91 DLT Gateways** | Set `SMS_GATEWAY_AUTH_KEY` to dispatch real SMS with DLT-registered templates. |

---

## 📜 Data Source Licensing, Terms of Use & Attributions

Per system specifications, all third-party data specifications and schemas adhere to their respective licenses:

1. **Open Charge Map (OCM)**:
   - *License*: Open Database License (ODbL) v1.0.
   - *Attribution*: Station metadata schemas and global charging directories courtesy of [Open Charge Map](https://openchargemap.org).
2. **OpenStreetMap & Leaflet**:
   - *License*: Open Data Commons Open Database License (ODbL) by the OpenStreetMap Foundation (OSMF).
   - *Attribution*: Map tiles and geocoding courtesy of [© OpenStreetMap contributors](https://www.openstreetmap.org/copyright).
3. **Open Charge Point Interface (OCPI)**:
   - *Standard*: OCPI Protocol v2.2.1 maintained by the EVRoaming Foundation.
   - *Terms*: Open, royalty-free standard for roaming and real-time EVSE status updates.
4. **Open Charge Point Protocol (OCPP)**:
   - *Standard*: OCPP 1.6-J and OCPP 2.0.1 maintained by Open Charge Alliance (OCA).
   - *Terms*: Open, royalty-free protocol for charging hardware telemetry.
5. **National Payments Corporation of India (NPCI)**:
   - *Standard*: UPI Procedural Guidelines & BharatQR Specifications.
   - *Compliance*: Tokenization, two-factor authentication for transactions above ₹2,000, and daily settlement reconciliation.
6. **Digital Personal Data Protection (DPDP) Act 2023**:
   - *Compliance*: Multilingual consent notices, purpose limitation, right to grievance redressal, and self-service personal data export.

---

## 🧪 Automated Test Suite

Run the full test suite with:

```bash
cd /Users/avinashanilpathak/.gemini/antigravity/scratch/ai1
PYTHONPATH=. venv/bin/pytest tests/test_all_modules.py -v
```

**Coverage**:
- `test_01_system_health`: System status, Bengaluru default configuration
- `test_02_auth_and_sso`: Phone OTP login, demo OTP validation, profile management
- `test_03_wallet_and_payments`: Top-up, UPI P2P pay, BESCOM bill payment, Ai1 Coins
- `test_04_quick_commerce`: Pincode check, catalog, 12-min checkout, live rider tracking
- `test_05_ride_hailing`: Bike/Auto/Cab surge pricing, booking, live driver tracking, SOS
- `test_06_home_services`: Catalog, package pricing, slot booking, start OTP verification
- `test_07_mechanic_and_rsa`: Packages, breakdown SOS dispatch, estimate approval
- `test_08_travel`: Flight search, IRCTC PNR status, composite itinerary bundle
- `test_09_insurance`: Multi-insurer quotes, 1-click KYC policy buy, vault, cashless claim
- `test_10_ev_charging_realtime`: Bbox filtering, session start/telemetry/stop, 15m hold, route planner
- `test_11_ai_assistant_multilingual_orchestration`: Cross-module composite orchestration, 2-phase commit, Hindi & Kannada NLP
- `test_12_partner_and_admin`: Gig dashboards (rider, driver, EV operator), admin GMV, and audit trail
