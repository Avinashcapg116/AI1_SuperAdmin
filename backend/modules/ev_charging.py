"""
Ai1 Super App - Real-Time EV Charging Module
Interactive map of charging stations with live connector status,
filters (CCS2, Type 2, CHAdeMO, Bharat DC, 3-pin, kW power),
route planner, start/stop charging session with live kWh telemetry,
15-minute connector reservations, crowdsourced layer, and cost estimator.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import random
from backend.models.schemas import (
    EvStation, EvSession, StartSessionRequest, StopSessionRequest,
    ReserveConnectorRequest, CrowdsourceReportRequest, EvRoutePlanRequest, User
)
from backend.modules.auth import get_current_user
from backend.database.db import db
from backend.adapters.ev_charging_adapter import ev_charging_adapter
from backend.adapters.map_adapter import map_adapter
from backend.adapters.payment_adapter import payment_adapter

router = APIRouter(prefix="/ev", tags=["Real-Time EV Charging Network"])


@router.get("/stations", response_model=List[EvStation])
def get_ev_stations(
    min_lat: float = Query(12.80),
    min_lng: float = Query(77.50),
    max_lat: float = Query(13.30),
    max_lng: float = Query(77.85),
    connector_type: Optional[str] = None,
    min_power: float = Query(0.0),
    only_available: bool = Query(False)
):
    filters = {
        "connector_type": connector_type,
        "min_power": min_power,
        "only_available": only_available
    }
    return ev_charging_adapter.fetch_stations(min_lat, min_lng, max_lat, max_lng, filters)


@router.get("/stations/{station_id}", response_model=EvStation)
def get_station_details(station_id: str):
    stn = db.ev_stations.get(station_id)
    if not stn:
        raise HTTPException(status_code=404, detail="EV station not found")
    return stn


@router.post("/sessions/start")
def start_charging_session(req: StartSessionRequest, user: User = Depends(get_current_user)):
    res = ev_charging_adapter.start_remote_session(
        user_id=user.id,
        station_id=req.station_id,
        connector_id=req.connector_id,
        target_soc=req.target_soc
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error", "Failed to start charging"))
    return res


@router.get("/sessions/{session_id}/live", response_model=EvSession)
def get_live_session(session_id: str):
    session = db.ev_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="EV Session not found")

    if session.status == "charging":
        # Simulate live energy delivery telemetry
        session.duration_mins += 1
        session.energy_delivered_kwh = round(session.energy_delivered_kwh + 0.45, 2)
        if session.soc_current_pct < session.soc_target_pct:
            session.soc_current_pct += 1
        session.total_cost = round(session.energy_delivered_kwh * 19.5, 2)

    return session


@router.post("/sessions/stop")
def stop_charging_session(req: StopSessionRequest, user: User = Depends(get_current_user)):
    res = ev_charging_adapter.stop_remote_session(req.session_id)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error", "Failed to stop charging"))

    # Auto-deduct session cost from Ai1 wallet
    pay_res = payment_adapter.debit_wallet(
        user_id=user.id,
        amount=res["total_cost"],
        module="ev_charging",
        ref_id=req.session_id,
        description=f"EV Charging Session ({res['energy_delivered_kwh']} kWh)"
    )

    return {
        **res,
        "payment": pay_res
    }


@router.post("/reservations")
def reserve_connector(req: ReserveConnectorRequest, user: User = Depends(get_current_user)):
    res = ev_charging_adapter.reserve_connector(
        station_id=req.station_id,
        connector_id=req.connector_id,
        user_id=user.id,
        hold_minutes=req.hold_minutes
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error", "Reservation failed"))
    return res


@router.post("/crowdsource/report")
def report_station_status(req: CrowdsourceReportRequest, user: User = Depends(get_current_user)):
    stn = db.ev_stations.get(req.station_id)
    if not stn:
        raise HTTPException(status_code=404, detail="Station not found")

    if not req.is_working:
        stn.reliability_score = max(50.0, round(stn.reliability_score - 1.5, 1))
    else:
        stn.reliability_score = min(100.0, round(stn.reliability_score + 0.5, 1))

    return {
        "success": True,
        "message": "Thank you for contributing to the Ai1 Community Grid! 10 Ai1 Coins awarded for verified report.",
        "station_reliability_score": stn.reliability_score
    }


@router.post("/route-planner")
def plan_ev_route(req: EvRoutePlanRequest):
    return map_adapter.plan_ev_route(
        origin=req.origin,
        destination=req.destination,
        current_battery_pct=req.current_battery_pct,
        battery_capacity_kwh=req.vehicle_battery_capacity_kwh,
        range_full_km=req.range_full_km
    )


@router.get("/tariff-estimator")
def estimate_charging_cost(
    battery_kwh: float = Query(40.5),
    current_soc: int = Query(20),
    target_soc: int = Query(80),
    tariff_per_kwh: float = Query(19.5),
    power_kw: float = Query(60.0)
):
    needed_pct = max(0, target_soc - current_soc)
    needed_kwh = round((needed_pct / 100.0) * battery_kwh, 2)
    est_cost = round(needed_kwh * tariff_per_kwh, 2)
    est_duration_mins = max(10, int((needed_kwh / power_kw) * 60))

    return {
        "battery_capacity_kwh": battery_kwh,
        "current_soc_pct": current_soc,
        "target_soc_pct": target_soc,
        "energy_needed_kwh": needed_kwh,
        "estimated_cost_inr": est_cost,
        "estimated_duration_mins": est_duration_mins,
        "power_kw": power_kw
    }
