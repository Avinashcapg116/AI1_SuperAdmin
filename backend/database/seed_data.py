"""
Ai1 Super App - Realistic Seed Dataset (Bengaluru Focused)
"""

from typing import Dict, List, Any

# Dark Stores in Bengaluru
SEED_DARK_STORES = [
    {
        "id": "DS-BLR-01",
        "name": "Ai1 QuickStore - Indiranagar",
        "pincode": "560038",
        "area": "Indiranagar 100ft Road",
        "lat": 12.9784,
        "lng": 77.6408,
        "is_active": True,
        "delivery_eta_mins": 11
    },
    {
        "id": "DS-BLR-02",
        "name": "Ai1 QuickStore - Koramangala",
        "pincode": "560034",
        "area": "Koramangala 4th Block",
        "lat": 12.9345,
        "lng": 77.6245,
        "is_active": True,
        "delivery_eta_mins": 14
    },
    {
        "id": "DS-BLR-03",
        "name": "Ai1 QuickStore - HSR Layout",
        "pincode": "560102",
        "area": "HSR Sector 2",
        "lat": 12.9116,
        "lng": 77.6389,
        "is_active": True,
        "delivery_eta_mins": 10
    },
    {
        "id": "DS-BLR-04",
        "name": "Ai1 QuickStore - Whitefield",
        "pincode": "560066",
        "area": "ITPL Main Road",
        "lat": 12.9698,
        "lng": 77.7500,
        "is_active": True,
        "delivery_eta_mins": 15
    }
]

# Quick Commerce Products
SEED_PRODUCTS = [
    {
        "id": "qc-milk-01",
        "name": "Amul Taaza Homogenised Toned Milk",
        "category": "Dairy & Breakfast",
        "price": 28.0,
        "mrp": 30.0,
        "unit": "500 ml",
        "image_url": "🥛",
        "in_stock": True,
        "stock_count": 85,
        "rating": 4.9,
        "tags": ["dairy", "milk", "daily"]
    },
    {
        "id": "qc-bread-01",
        "name": "The Health Factory 100% Whole Wheat Bread",
        "category": "Dairy & Breakfast",
        "price": 55.0,
        "mrp": 60.0,
        "unit": "350 g",
        "image_url": "🍞",
        "in_stock": True,
        "stock_count": 40,
        "rating": 4.8,
        "tags": ["bread", "wheat", "breakfast"]
    },
    {
        "id": "qc-eggs-01",
        "name": "Farm Fresh White Eggs (Pack of 6)",
        "category": "Dairy & Breakfast",
        "price": 52.0,
        "mrp": 65.0,
        "unit": "6 pcs",
        "image_url": "🥚",
        "in_stock": True,
        "stock_count": 120,
        "rating": 4.9,
        "tags": ["eggs", "protein", "breakfast"]
    },
    {
        "id": "qc-veg-potato",
        "name": "Fresh Tender Potatoes",
        "category": "Fresh Vegetables",
        "price": 38.0,
        "mrp": 45.0,
        "unit": "1 kg",
        "image_url": "🥔",
        "in_stock": True,
        "stock_count": 200,
        "rating": 4.7,
        "tags": ["vegetables", "staple"]
    },
    {
        "id": "qc-veg-onion",
        "name": "Nashik Red Onions",
        "category": "Fresh Vegetables",
        "price": 42.0,
        "mrp": 50.0,
        "unit": "1 kg",
        "image_url": "🧅",
        "in_stock": True,
        "stock_count": 190,
        "rating": 4.8,
        "tags": ["vegetables", "onion"]
    },
    {
        "id": "qc-snack-chai",
        "name": "Wagh Bakri Premium Spiced Tea (Chai)",
        "category": "Snacks & Munchies",
        "price": 140.0,
        "mrp": 155.0,
        "unit": "250 g",
        "image_url": "☕",
        "in_stock": True,
        "stock_count": 60,
        "rating": 4.9,
        "tags": ["chai", "tea"]
    },
    {
        "id": "qc-snack-biscuit",
        "name": "Parle-G Gold Biscuits (Family Pack)",
        "category": "Snacks & Munchies",
        "price": 40.0,
        "mrp": 45.0,
        "unit": "1 kg",
        "image_url": "🍪",
        "in_stock": True,
        "stock_count": 95,
        "rating": 4.9,
        "tags": ["biscuits", "snacks"]
    },
    {
        "id": "qc-oil-ghee",
        "name": "Nandini Pure Cow Ghee (Karnataka Dairy)",
        "category": "Atta, Rice & Oils",
        "price": 320.0,
        "mrp": 340.0,
        "unit": "500 ml",
        "image_url": "🧈",
        "in_stock": True,
        "stock_count": 50,
        "rating": 5.0,
        "tags": ["ghee", "nandini", "dairy"]
    }
]

# Real-Time EV Charging Stations (Bengaluru)
SEED_EV_STATIONS = [
    {
        "id": "EV-STN-01",
        "name": "Tata Power EZ Charge - Indiranagar Metro",
        "operator_name": "Tata Power",
        "address": "Opposite Indiranagar Metro Station, CMH Road, Bengaluru",
        "pincode": "560038",
        "lat": 12.9783,
        "lng": 77.6387,
        "is_24x7": True,
        "amenities": ["Metro Access", "Cafe Coffee Day", "Restroom", "Air/Water"],
        "reliability_score": 99.2,
        "last_status_update": "Just now",
        "connectors": [
            {
                "id": "CONN-01-A",
                "connector_type": "CCS2",
                "power_kw": 60.0,
                "current_type": "DC",
                "status": "available",
                "tariff_per_kwh": 19.5,
                "idle_fee_per_min": 2.5,
                "last_heartbeat": "30s ago"
            },
            {
                "id": "CONN-01-B",
                "connector_type": "CCS2",
                "power_kw": 60.0,
                "current_type": "DC",
                "status": "occupied",
                "tariff_per_kwh": 19.5,
                "idle_fee_per_min": 2.5,
                "last_heartbeat": "12s ago"
            },
            {
                "id": "CONN-01-C",
                "connector_type": "Type 2",
                "power_kw": 22.0,
                "current_type": "AC",
                "status": "available",
                "tariff_per_kwh": 14.0,
                "idle_fee_per_min": 1.0,
                "last_heartbeat": "45s ago"
            }
        ]
    },
    {
        "id": "EV-STN-02",
        "name": "Zeon Fast Charger Hub - Forum South Mall",
        "operator_name": "Zeon Charging",
        "address": "Basement 2, Forum Mall, Hosur Road, Koramangala",
        "pincode": "560034",
        "lat": 12.9348,
        "lng": 77.6110,
        "is_24x7": True,
        "amenities": ["Mall Food Court", "Covered Parking", "Security", "Cinema"],
        "reliability_score": 98.7,
        "last_status_update": "1 min ago",
        "connectors": [
            {
                "id": "CONN-02-A",
                "connector_type": "CCS2",
                "power_kw": 120.0,
                "current_type": "DC Fast",
                "status": "available",
                "tariff_per_kwh": 22.0,
                "idle_fee_per_min": 3.0,
                "last_heartbeat": "15s ago"
            },
            {
                "id": "CONN-02-B",
                "connector_type": "CCS2",
                "power_kw": 120.0,
                "current_type": "DC Fast",
                "status": "available",
                "tariff_per_kwh": 22.0,
                "idle_fee_per_min": 3.0,
                "last_heartbeat": "20s ago"
            },
            {
                "id": "CONN-02-C",
                "connector_type": "CHAdeMO",
                "power_kw": 50.0,
                "current_type": "DC",
                "status": "available",
                "tariff_per_kwh": 18.0,
                "idle_fee_per_min": 2.0,
                "last_heartbeat": "1m ago"
            }
        ]
    },
    {
        "id": "EV-STN-03",
        "name": "Jio-bp pulse SuperHub - HSR Sector 1",
        "operator_name": "Jio-bp pulse",
        "address": "27th Main Rd, HSR Layout Sector 1, Bengaluru",
        "pincode": "560102",
        "lat": 12.9150,
        "lng": 77.6520,
        "is_24x7": True,
        "amenities": ["Wild Bean Cafe", "Car Vacuum", "Restroom", "24x7 Staff"],
        "reliability_score": 97.9,
        "last_status_update": "2 mins ago",
        "connectors": [
            {
                "id": "CONN-03-A",
                "connector_type": "CCS2",
                "power_kw": 60.0,
                "current_type": "DC",
                "status": "occupied",
                "tariff_per_kwh": 18.9,
                "idle_fee_per_min": 2.0,
                "last_heartbeat": "10s ago"
            },
            {
                "id": "CONN-03-B",
                "connector_type": "Bharat DC-001",
                "power_kw": 15.0,
                "current_type": "DC Slow",
                "status": "available",
                "tariff_per_kwh": 13.5,
                "idle_fee_per_min": 1.0,
                "last_heartbeat": "40s ago"
            },
            {
                "id": "CONN-03-C",
                "connector_type": "3-pin 16A (2-Wheelers)",
                "power_kw": 3.3,
                "current_type": "AC",
                "status": "available",
                "tariff_per_kwh": 11.0,
                "idle_fee_per_min": 0.5,
                "last_heartbeat": "1m ago"
            }
        ]
    },
    {
        "id": "EV-STN-04",
        "name": "Ai1 UltraGrid - Kempegowda Airport Highway",
        "operator_name": "Ai1 FastGrid",
        "address": "NH 44, Near Toll Plaza, Devanahalli, Bengaluru",
        "pincode": "560300",
        "lat": 13.1986,
        "lng": 77.7066,
        "is_24x7": True,
        "amenities": ["Airport Transit Lounge", "High-speed Wi-Fi", "Showers", "Diner"],
        "reliability_score": 99.8,
        "last_status_update": "Just now",
        "connectors": [
            {
                "id": "CONN-04-A",
                "connector_type": "CCS2",
                "power_kw": 150.0,
                "current_type": "DC Ultra",
                "status": "available",
                "tariff_per_kwh": 23.5,
                "idle_fee_per_min": 3.5,
                "last_heartbeat": "5s ago"
            },
            {
                "id": "CONN-04-B",
                "connector_type": "CCS2",
                "power_kw": 150.0,
                "current_type": "DC Ultra",
                "status": "available",
                "tariff_per_kwh": 23.5,
                "idle_fee_per_min": 3.5,
                "last_heartbeat": "8s ago"
            }
        ]
    }
]

# Home Services (Urban Company Style)
SEED_SERVICES = [
    {
        "id": "srv-ac-foam",
        "title": "Intense Foam-Jet AC Servicing (Split)",
        "category": "AC Repair & Service",
        "description": "Deep foam cleaning of indoor & outdoor coils, gas check, filter sanitization.",
        "duration_mins": 60,
        "price": 599.0,
        "rating": 4.91,
        "review_count": 8420,
        "image_url": "❄️",
        "warranty_days": 30,
        "addons": [
            {"id": "add-gas", "name": "Freon Gas Leak Fix & Refill", "price": 1499.0},
            {"id": "add-anti", "name": "Anti-Rust Protective Coating", "price": 299.0}
        ]
    },
    {
        "id": "srv-home-deep",
        "title": "Complete 2BHK Deep Cleaning",
        "category": "Home Cleaning",
        "description": "Single-disc scrubbing machine, tile regrouting, kitchen degreasing & 2 bathroom sterilization.",
        "duration_mins": 240,
        "price": 2499.0,
        "rating": 4.88,
        "review_count": 4120,
        "image_url": "🧹",
        "warranty_days": 7,
        "addons": [
            {"id": "add-balc", "name": "Balcony High-Pressure Wash", "price": 349.0},
            {"id": "add-sofa", "name": "Sofa Shampooing (3 Seater)", "price": 699.0}
        ]
    },
    {
        "id": "srv-electrician-visit",
        "title": "Certified Electrician Diagnostic & Repair",
        "category": "Electrician",
        "description": "Switches, MCB tripping, fan installation, chandelier wiring & earthing test.",
        "duration_mins": 45,
        "price": 199.0,
        "rating": 4.93,
        "review_count": 12890,
        "image_url": "⚡",
        "warranty_days": 30,
        "addons": [
            {"id": "add-mcb", "name": "Heavy Duty 32A MCB Replacement", "price": 450.0}
        ]
    },
    {
        "id": "srv-salon-men",
        "title": "Men's Grooming: Haircut + Beard Styling + Head Massage",
        "category": "Men's Salon",
        "description": "Use-and-throw towel, sanitized scissors, organic mint head oil massage.",
        "duration_mins": 50,
        "price": 449.0,
        "rating": 4.95,
        "review_count": 19400,
        "image_url": "✂️",
        "warranty_days": 0,
        "addons": [
            {"id": "add-d-tan", "name": "De-Tan Facial Scrub", "price": 350.0}
        ]
    }
]

# Mechanic Packages & Roadside SOS
SEED_MECHANIC_PACKAGES = [
    {
        "id": "mech-car-periodic",
        "title": "Comprehensive Car Periodic Service",
        "vehicle_type": "car",
        "includes": ["Engine oil replacement (Synthetic)", "Oil & air filter change", "Brake pads inspection", "Coolant top-up", "40-point health check", "Free car wash"],
        "price": 3499.0,
        "duration_hours": 4
    },
    {
        "id": "mech-bike-service",
        "title": "Doorstep Bike General Servicing",
        "vehicle_type": "bike",
        "includes": ["Engine oil top-up", "Chain lubing & tensioning", "Carburetor/Fuel injector tune", "Brake tuning", "Clutch adjustment"],
        "price": 699.0,
        "duration_hours": 2
    }
]

# Travel - Flights & Trains
SEED_FLIGHTS = [
    {
        "flight_number": "6E-512",
        "airline": "IndiGo",
        "origin": "BLR (Bengaluru)",
        "destination": "DEL (New Delhi)",
        "departure_time": "06:15 AM",
        "arrival_time": "09:05 AM",
        "duration": "2h 50m",
        "price": 5499.0,
        "refundable": True,
        "seats_left": 4
    },
    {
        "flight_number": "AI-804",
        "airline": "Air India",
        "origin": "BLR (Bengaluru)",
        "destination": "BOM (Mumbai)",
        "departure_time": "08:45 AM",
        "arrival_time": "10:30 AM",
        "duration": "1h 45m",
        "price": 4250.0,
        "refundable": True,
        "seats_left": 8
    },
    {
        "flight_number": "QP-1302",
        "airline": "Akasa Air",
        "origin": "BLR (Bengaluru)",
        "destination": "GOI (Goa Mopa)",
        "departure_time": "11:20 AM",
        "arrival_time": "12:35 PM",
        "duration": "1h 15m",
        "price": 2899.0,
        "refundable": True,
        "seats_left": 12
    }
]

SEED_TRAINS = [
    {
        "train_number": "20608",
        "train_name": "Mysuru - MGR Chennai Central Vande Bharat",
        "origin": "SBC (Bengaluru City)",
        "destination": "MAS (Chennai Central)",
        "departure_time": "14:50",
        "arrival_time": "19:20",
        "classes": [
            {"class": "CC (Chair Car)", "price": 995.0, "status": "AVAILABLE-86"},
            {"class": "EC (Exec Chair)", "price": 1885.0, "status": "AVAILABLE-14"}
        ]
    },
    {
        "train_number": "22691",
        "train_name": "Bengaluru - Hazrat Nizamuddin Rajdhani Express",
        "origin": "SBC (Bengaluru City)",
        "destination": "NZM (New Delhi)",
        "departure_time": "20:00",
        "arrival_time": "05:30 (+2 days)",
        "classes": [
            {"class": "3A", "price": 2840.0, "status": "AVAILABLE-32"},
            {"class": "2A", "price": 4120.0, "status": "RAC-5"},
            {"class": "1A", "price": 6890.0, "status": "WL-2"}
        ]
    }
]

# Insurance Quotes
SEED_INSURANCE_QUOTES = [
    {
        "quote_id": "INS-HLTH-HDFC",
        "type": "health",
        "insurer_name": "HDFC ERGO",
        "plan_name": "Optima Secure 4X Booster",
        "cover_amount": 1000000.0,  # ₹10 Lakhs cover
        "premium_annual": 8940.0,
        "key_features": ["4X Base cover with 2X on day 1", "Zero deduction on consumables", "Instant cashless within 20 mins"],
        "cashless_hospitals_or_garages": 14200,
        "irda_claim_settlement_ratio": 99.1
    },
    {
        "quote_id": "INS-HLTH-STAR",
        "type": "health",
        "insurer_name": "Star Health",
        "plan_name": "Star Comprehensive Health Insurance",
        "cover_amount": 1500000.0,
        "premium_annual": 11200.0,
        "key_features": ["Maternity & newborn cover", "Annual free health checkup", "No claim bonus up to 100%"],
        "cashless_hospitals_or_garages": 13800,
        "irda_claim_settlement_ratio": 98.4
    },
    {
        "quote_id": "INS-MOTR-ICICI",
        "type": "motor",
        "insurer_name": "ICICI Lombard",
        "plan_name": "Comprehensive EV & Zero-Dep Cover",
        "cover_amount": 1450000.0,  # IDV of car
        "premium_annual": 14200.0,
        "key_features": ["Battery failure & surge protection", "Zero depreciation on all parts", "Roadside assistance included"],
        "cashless_hospitals_or_garages": 9500,
        "irda_claim_settlement_ratio": 98.9
    },
    {
        "quote_id": "INS-TRV-TATA",
        "type": "travel",
        "insurer_name": "Tata AIG",
        "plan_name": "Domestic Flight & Trip Shield",
        "cover_amount": 250000.0,
        "premium_annual": 79.0,  # Per trip add-on
        "key_features": ["Flight delay compensation (₹2,500)", "Baggage loss protection", "Emergency medical evacuation"],
        "cashless_hospitals_or_garages": 8000,
        "irda_claim_settlement_ratio": 99.4
    }
]

# Demo Seed User
SEED_DEFAULT_USER = {
    "id": "USR-DEMO-01",
    "phone": "+91 98765 43210",
    "name": "Arjun Sundaram",
    "email": "arjun.sundaram@ai1.in",
    "preferred_language": "en",
    "role": "customer",
    "is_kyc_verified": True,
    "mpin_set": True,
    "addresses": [
        {
            "id": "ADDR-01",
            "label": "Home",
            "street": "Flat 402, Prestige Palms, 12th Main, Indiranagar",
            "city": "Bengaluru",
            "pincode": "560038",
            "lat": 12.9780,
            "lng": 77.6405,
            "is_default": True
        },
        {
            "id": "ADDR-02",
            "label": "Work",
            "street": "Ai1 Tech Park, Embassy GolfLinks, Intermediate Ring Rd",
            "city": "Bengaluru",
            "pincode": "560071",
            "lat": 12.9498,
            "lng": 77.6480,
            "is_default": False
        }
    ],
    "vehicles": [
        {
            "id": "VEH-01",
            "vehicle_number": "KA 03 MX 8899",
            "make": "Tata",
            "model": "Nexon EV Max (40.5 kWh)",
            "vehicle_type": "car",
            "is_ev": True,
            "battery_capacity_kwh": 40.5,
            "supported_connectors": ["CCS2", "Type 2"]
        }
    ]
}
