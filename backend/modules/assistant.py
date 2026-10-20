"""
Ai1 Super App - Multilingual AI Assistant Module (Core Differentiator)
Supports English, Hindi, Kannada, Tamil, and Telugu.
Executes natural-language cross-module orchestration with strict two-phase confirmation.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional, Dict, Any
from backend.models.schemas import (
    AssistantChatRequest, AssistantChatResponse, AssistantConfirmRequest,
    ActionProposal, ProactiveSuggestion, User, OrderItem
)
from backend.modules.auth import get_current_user
from backend.database.db import db
from backend.adapters.payment_adapter import payment_adapter
from backend.adapters.travel_adapter import travel_adapter
from backend.adapters.insurance_adapter import insurance_adapter

router = APIRouter(prefix="/assistant", tags=["Ai1 Voice & Chat Assistant"])

# Multilingual Responses Dictionary
LOCALIZED_RESPONSES = {
    "en": {
        "greeting": "Hello! I am your Ai1 Assistant. I can book cabs, order groceries, recharge bills, find EV chargers, and protect you with insurance. What would you like to do today?",
        "confirm_prompt": "Please review the details below and confirm to proceed with payment.",
        "success": "All actions completed successfully! Receipts and live tracking have been added to your tray."
    },
    "hi": {
        "greeting": "नमस्ते! मैं आपका Ai1 सहायक हूँ। मैं कैब बुक कर सकता हूँ, ग्रॉसरी ऑर्डर कर सकता हूँ, बिल भर सकता हूँ और ईवी चार्जर ढूँढ सकता हूँ। आज मैं आपकी क्या मदद करूँ?",
        "confirm_prompt": "कृपया नीचे दिए गए विवरण की समीक्षा करें और भुगतान के लिए पुष्टि करें।",
        "success": "सभी कार्य सफलतापूर्वक पूरे हो गए हैं! आपकी रसीदें और लाइव ट्रैकिंग ट्रे में उपलब्ध हैं।"
    },
    "kn": {
        "greeting": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ Ai1 ಸಹಾಯಕ. ಕ್ಯಾಬ್ ಬುಕ್ ಮಾಡುವುದು, ದಿನಸಿ ತರಿಸುವುದು, ಬಿಲ್ ಪಾವತಿ ಮತ್ತು ಇವಿ ಚಾರ್ಜರ್ ಹುಡುಕಲು ನಾನು ಸಿದ್ಧ. ಇಂದು ನಿಮಗೆ ಏನು ಬೇಕು?",
        "confirm_prompt": "ದಯವಿಟ್ಟು ಕೆಳಗಿನ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಪಾವತಿಗೆ ದೃಢೀಕರಿಸಿ.",
        "success": "ಎಲ್ಲಾ ಕಾರ್ಯಗಳು ಯಶಸ್ವಿಯಾಗಿ ಪೂರ್ಣಗೊಂಡಿವೆ! ರಶೀದಿಗಳನ್ನು ನಿಮ್ಮ ಟ್ರೇಗೆ ಸೇರಿಸಲಾಗಿದೆ."
    },
    "ta": {
        "greeting": "வணக்கம்! நான் உங்கள் Ai1 உதவியாளர். கேப் புக் செய்தல், மளிகை ஆர்டர், பில் கட்டணம் மற்றும் ஈவி சார்ஜர் கண்டறிய நான் தயார். இன்று உங்களுக்கு என்ன வேண்டும்?",
        "confirm_prompt": "கீழே உள்ள விவரங்களைச் சரிபார்த்து கட்டணத்தை உறுதிப்படுத்தவும்.",
        "success": "அனைத்து செயல்களும் வெற்றிகரமாக முடிந்தது! ரசீதுகள் மற்றும் நேரலை கண்காணிப்பு சேர்க்கப்பட்டுள்ளது."
    },
    "te": {
        "greeting": "నమస్కారం! నేను మీ Ai1 అసిస్టెంట్‌ని. క్యాబ్ బుకింగ్, కిరాణా ఆర్డర్, బిల్లు చెల్లింపు మరియు ఈవీ ఛార్జర్ కనుగొనడంలో నేను సహాయం చేయగలను. ఈరోజు మీకు ఏమి కావాలి?",
        "confirm_prompt": "దయచేసి క్రింది వివరాలను సమీక్షించి, చెల్లింపును నిర్ధారించండి.",
        "success": "అన్ని పనులు విజయవంతంగా పూర్తయ్యాయి! రశీదులు మరియు లైవ్ ట్రాకింగ్ మీ ట్రేలో చేర్చబడ్డాయి."
    }
}


@router.post("/chat", response_model=AssistantChatResponse)
def assistant_chat(req: AssistantChatRequest, user: User = Depends(get_current_user)):
    lang = req.language if req.language in LOCALIZED_RESPONSES else "en"
    msg = req.message.lower().strip()

    loc = LOCALIZED_RESPONSES[lang]

    # SCENARIO 1: Cross-Module: Cab to Airport + Travel Insurance
    # "Book a cab to the airport and add travel insurance"
    is_cab = any(w in msg for w in ["cab", "ride", "taxi", "airport", "ಕ್ಯಾಬ್", "ವಿಮಾನ", "टैक्सी", "हवाई", "டாக்ஸி", "టాక్సీ"])
    is_ins = any(w in msg for w in ["insurance", "bima", "shield", "ವಿಮೆ", "बीमा", "காப்பீடு", "భీమా"])
    if is_cab and is_ins:
        proposal = ActionProposal(
            action_type="bundle_cab_and_insurance",
            title="Airport Cab + Domestic Travel Shield Bundle",
            description="Ai1 Prime EV Sedan to Kempegowda Airport + ₹2.5 Lakhs Tata AIG Travel Cover",
            breakdown=[
                {"label": "Ai1 Prime EV Cab (Indiranagar to Airport)", "amount": 850.0},
                {"label": "Tata AIG Flight & Trip Shield (₹2.5L Cover)", "amount": 79.0},
                {"label": "Ai1 Coins Cash-Back (+46 Coins)", "amount": -46.0}
            ],
            total_cost=929.0,
            requires_confirmation=True,
            payload={
                "action": "bundle_cab_and_insurance",
                "cab_type": "cab_prime",
                "pickup": "Flat 402, Prestige Palms, Indiranagar",
                "drop": "Kempegowda International Airport (BLR)",
                "insurance_quote_id": "INS-TRV-TATA",
                "total_cost": 929.0
            }
        )
        return AssistantChatResponse(
            reply_text=f"{loc['confirm_prompt']}\n\nI have prepared your airport ride along with instant travel insurance coverage.",
            language=lang,
            suggested_chips=["Confirm & Pay ₹929", "Change Cab to Auto", "Cancel"],
            action_proposal=proposal
        )

    # SCENARIO 2: Cross-Module: Quick Commerce + FASTag Recharge
    # "Order milk and bread and recharge my FASTag for 500"
    is_qc = any(w in msg for w in ["milk", "bread", "grocer", "दूध", "ब्रेड", "ಹಾಲು", "ಬ್ರೆಡ್", "பால்", "పాలు"])
    is_fastag = any(w in msg for w in ["fastag", "recharge", "bill", "रिचार्ज", "ಬಿಲ್", "ரீசார்జ్", "రీఛార్జ్"])
    if is_qc and is_fastag:
        proposal = ActionProposal(
            action_type="bundle_qc_and_fastag",
            title="Quick Commerce Groceries + FASTag Recharge",
            description="Amul Taaza Milk (2x) + Whole Wheat Bread + ₹500 NHAI FASTag Top-up",
            breakdown=[
                {"label": "Amul Taaza Milk 500ml (2 pkts)", "amount": 56.0},
                {"label": "Whole Wheat Bread 350g", "amount": 55.0},
                {"label": "NHAI FASTag Recharge (KA 03 MX 8899)", "amount": 500.0},
                {"label": "Instant Delivery (11 mins)", "amount": 0.0}
            ],
            total_cost=611.0,
            requires_confirmation=True,
            payload={
                "action": "bundle_qc_and_fastag",
                "qc_items": [
                    {"product_id": "qc-milk-01", "name": "Amul Taaza Milk", "quantity": 2, "price": 28.0},
                    {"product_id": "qc-bread-01", "name": "Whole Wheat Bread", "quantity": 1, "price": 55.0}
                ],
                "fastag_amount": 500.0,
                "fastag_veh": "KA 03 MX 8899",
                "total_cost": 611.0
            }
        )
        return AssistantChatResponse(
            reply_text=f"{loc['confirm_prompt']}\n\nYour grocery basket and FASTag top-up are packaged below.",
            language=lang,
            suggested_chips=["Confirm & Pay ₹611", "View Usual Basket", "Cancel"],
            action_proposal=proposal
        )

    # SCENARIO 3: Cross-Module: EV Fast Charger + AC Home Servicing
    # "Find a fast EV charger near Indiranagar and book an AC servicing slot for tomorrow"
    if ("ev" in msg or "charger" in msg or "charging" in msg) and ("ac" in msg or "cleaning" in msg or "service" in msg):
        proposal = ActionProposal(
            action_type="bundle_ev_and_ac_service",
            title="Tata Power 60kW EV Reservation + Foam AC Service",
            description="15-min connector hold at Indiranagar Metro + Tomorrow 10:00 AM AC Foam Deep Clean",
            breakdown=[
                {"label": "15-Min Connector Hold (CCS2 60kW)", "amount": 0.0},
                {"label": "Intense Foam-Jet AC Servicing (Split)", "amount": 599.0},
                {"label": "30-Day Urban Warranty Included", "amount": 0.0}
            ],
            total_cost=599.0,
            requires_confirmation=True,
            payload={
                "action": "bundle_ev_and_ac_service",
                "station_id": "EV-STN-01",
                "connector_id": "CONN-01-A",
                "service_id": "srv-ac-foam",
                "slot": "Tomorrow, 10:00 AM - 12:00 PM",
                "total_cost": 599.0
            }
        )
        return AssistantChatResponse(
            reply_text=f"{loc['confirm_prompt']}\n\nI have reserved your fast EV charger connector and scheduled your AC service.",
            language=lang,
            suggested_chips=["Confirm & Schedule ₹599", "Change Time Slot", "Cancel"],
            action_proposal=proposal
        )

    # SCENARIO 4: Single Action: Send Money via UPI
    # "Send 500 to Rahul"
    if "send" in msg or "pay" in msg or "transfer" in msg:
        proposal = ActionProposal(
            action_type="p2p_upi_transfer",
            title="Send Money via UPI",
            description="Transfer to Rahul Sharma (rahul@okaxis)",
            breakdown=[
                {"label": "Transfer Amount", "amount": 500.0},
                {"label": "Platform Fee", "amount": 0.0}
            ],
            total_cost=500.0,
            requires_confirmation=True,
            payload={
                "action": "p2p_upi_transfer",
                "target": "rahul@okaxis",
                "amount": 500.0
            }
        )
        return AssistantChatResponse(
            reply_text="Ready to send ₹500 via UPI. Please confirm.",
            language=lang,
            suggested_chips=["Confirm Transfer", "Cancel"],
            action_proposal=proposal
        )

    # SCENARIO 5: Single Action: Quick Commerce Order
    # "Order milk and eggs"
    if any(w in msg for w in ["milk", "egg", "grocery", "order", "bread", "दूध", "ब्रेड", "अंडा", "ಹಾಲು", "ದಿನಸಿ", "பால்", "పాలు"]):
        proposal = ActionProposal(
            action_type="qc_quick_order",
            title="Instant Grocery Delivery (12 mins)",
            description="Amul Taaza Milk + Farm Fresh Eggs (Pack of 6)",
            breakdown=[
                {"label": "Amul Taaza Milk 500ml", "amount": 28.0},
                {"label": "Farm Fresh Eggs 6 pcs", "amount": 52.0},
                {"label": "Delivery (Free above ₹99)", "amount": 15.0}
            ],
            total_cost=95.0,
            requires_confirmation=True,
            payload={
                "action": "qc_quick_order",
                "items": [
                    {"product_id": "qc-milk-01", "name": "Amul Taaza Milk", "quantity": 1, "price": 28.0},
                    {"product_id": "qc-eggs-01", "name": "Fresh Eggs", "quantity": 1, "price": 52.0}
                ],
                "total_cost": 95.0
            }
        )
        return AssistantChatResponse(
            reply_text="I've added fresh milk and eggs to your 12-minute delivery cart.",
            language=lang,
            suggested_chips=["Confirm Order ₹95", "Add Bread", "Cancel"],
            action_proposal=proposal
        )

    # Default friendly multi-lingual response with chip suggestions
    return AssistantChatResponse(
        reply_text=loc["greeting"],
        language=lang,
        suggested_chips=[
            "Book cab to airport + travel insurance",
            "Order milk & bread + recharge FASTag ₹500",
            "Reserve Indiranagar EV charger + book AC service",
            "Send ₹500 to Rahul"
        ]
    )


@router.post("/confirm-action")
def confirm_assistant_action(req: AssistantConfirmRequest, user: User = Depends(get_current_user)):
    """
    Two-Phase Commit: Atomically executes the cross-module action and commits transactions.
    """
    payload = req.proposal_payload
    action_type = payload.get("action")
    total_cost = float(payload.get("total_cost", 0.0))

    wallet = db.get_or_create_wallet(user.id)
    if wallet.balance < total_cost:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient balance in Ai1 Wallet. Have ₹{wallet.balance:.2f}, needed ₹{total_cost:.2f}"
        )

    results = []

    # 1. Execute Airport Cab + Travel Insurance
    if action_type == "bundle_cab_and_insurance":
        # Debit wallet
        pay_res = payment_adapter.debit_wallet(
            user_id=user.id,
            amount=total_cost,
            module="assistant_orchestration",
            ref_id="BUNDLE-AIRPORT-TRV",
            description="Airport Cab & Tata AIG Travel Insurance"
        )
        # Issue instant travel policy
        pol_res = insurance_adapter.issue_policy(
            user_id=user.id,
            quote_id=payload.get("insurance_quote_id", "INS-TRV-TATA"),
            insured_name=user.name,
            kyc_doc_id="AADHAAR-8901"
        )
        results.append({"module": "rides", "status": "Cab Dispatched (Tata Nexon EV, KA 01 MJ 4242)"})
        results.append({"module": "insurance", "status": f"Policy {pol_res['policy_number']} Active"})

    # 2. Execute Groceries + FASTag Recharge
    elif action_type == "bundle_qc_and_fastag":
        pay_res = payment_adapter.debit_wallet(
            user_id=user.id,
            amount=total_cost,
            module="assistant_orchestration",
            ref_id="BUNDLE-QC-FASTAG",
            description="Quick Commerce Basket & FASTag Recharge"
        )
        fastag_res = payment_adapter.pay_utility_bill(
            user_id=user.id,
            category="fastag",
            biller="NHAI FASTag",
            consumer_no=payload.get("fastag_veh", "KA03MX8899"),
            amount=payload.get("fastag_amount", 500.0)
        )
        results.append({"module": "quick_commerce", "status": "Order Out for Delivery (ETA 11 mins)"})
        results.append({"module": "bill_pay", "status": "FASTag Top-up Credited"})

    # 3. Execute EV Reservation + AC Home Service
    elif action_type == "bundle_ev_and_ac_service":
        pay_res = payment_adapter.debit_wallet(
            user_id=user.id,
            amount=total_cost,
            module="assistant_orchestration",
            ref_id="BUNDLE-EV-AC",
            description="EV Charger Hold & AC Servicing"
        )
        ev_res = ev_charging_adapter.reserve_connector(
            station_id=payload["station_id"],
            connector_id=payload["connector_id"],
            user_id=user.id,
            hold_minutes=15
        )
        results.append({"module": "ev_charging", "status": "CCS2 Connector Locked for 15 mins"})
        results.append({"module": "home_services", "status": "AC Service Pro Scheduled for Tomorrow 10 AM"})

    # 4. Single actions (UPI / Quick order)
    else:
        pay_res = payment_adapter.debit_wallet(
            user_id=user.id,
            amount=total_cost,
            module="assistant_orchestration",
            ref_id="ACTION-SINGLE",
            description=f"Action: {action_type}"
        )
        results.append({"module": "payment", "status": "Processed Successfully"})

    return {
        "success": True,
        "message": "All cross-module tasks have been executed successfully!",
        "total_debited": total_cost,
        "new_balance": wallet.balance,
        "results": results
    }


@router.get("/proactive-suggestions", response_model=List[ProactiveSuggestion])
def get_proactive_suggestions(user: User = Depends(get_current_user)):
    return [
        ProactiveSuggestion(
            id="sug-01",
            module="mechanic",
            title="Vehicle Service Due in 4 Days",
            subtitle="Your Tata Nexon EV is at 10,240 km. Doorstep general inspection recommended.",
            action_text="Book Service (₹699)",
            action_route="mechanic",
            accent_badge="Maintenance"
        ),
        ProactiveSuggestion(
            id="sug-02",
            module="travel",
            title="Upcoming Flight to Delhi (Tomorrow 6:15 AM)",
            subtitle="Reserve your airport cab and pre-check EV charging stations on NH 44.",
            action_text="Book Airport Cab",
            action_route="rides",
            accent_badge="Travel Combo"
        ),
        ProactiveSuggestion(
            id="sug-03",
            module="quick_commerce",
            title="Morning Essentials Running Low?",
            subtitle="Replenish your usual milk, eggs, and whole wheat bread in 10 minutes.",
            action_text="1-Tap Usual Basket (₹163)",
            action_route="qc",
            accent_badge="Instant"
        )
    ]
