"""
Ai1 Super App - EV Charging Provider Adapters
Includes:
- ChargingDataProvider (Abstract Interface)
- OpenChargeMapAdapter (Station discovery metadata)
- OcpiAdapter (OCPI 2.2.x standard protocol)
- OcppCentralSystemAdapter (OCPP 1.6J / 2.0.1 commands)
- SimulatedChargingAdapter (Default realistic live demo provider)
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import time
import random
from datetime import datetime
from backend.database.db import db, haversine_distance_km
from backend.models.schemas import EvStation, EvConnector, EvSession


class ChargingDataProvider(ABC):
    @abstractmethod
    def fetch_stations(self, min_lat: float, min_lng: float, max_lat: float, max_lng: float, filters: Dict[str, Any]) -> List[EvStation]:
        pass

    @abstractmethod
    def get_connector_live_status(self, station_id: str, connector_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def start_remote_session(self, user_id: str, station_id: str, connector_id: str, target_soc: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def stop_remote_session(self, session_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def reserve_connector(self, station_id: str, connector_id: str, user_id: str, hold_minutes: int) -> Dict[str, Any]:
        pass


class OpenChargeMapAdapter(ChargingDataProvider):
    """Open Charge Map (OCM) Aggregator Client"""
    def __init__(self, api_key: str = "MOCK_OCM_KEY"):
        self.api_key = api_key

    def fetch_stations(self, min_lat: float, min_lng: float, max_lat: float, max_lng: float, filters: Dict[str, Any]) -> List[EvStation]:
        # Merges and supplements OCM metadata
        return [s for s in db.ev_stations.values() if min_lat <= s.lat <= max_lat and min_lng <= s.lng <= max_lng]

    def get_connector_live_status(self, station_id: str, connector_id: str) -> Dict[str, Any]:
        return {"status": "available", "source": "OCM"}

    def start_remote_session(self, user_id: str, station_id: str, connector_id: str, target_soc: int) -> Dict[str, Any]:
        raise NotImplementedError("OCM is a directory provider and does not support remote transactions.")

    def stop_remote_session(self, session_id: str) -> Dict[str, Any]:
        raise NotImplementedError("OCM does not support remote session termination.")

    def reserve_connector(self, station_id: str, connector_id: str, user_id: str, hold_minutes: int) -> Dict[str, Any]:
        raise NotImplementedError("OCM does not support hardware reservations.")


class OcpiAdapter(ChargingDataProvider):
    """OCPI 2.2.x Operator / Aggregator Protocol Adapter"""
    def __init__(self, cpo_token: str = "MOCK_OCPI_BEARER_TOKEN"):
        self.cpo_token = cpo_token

    def fetch_stations(self, min_lat: float, min_lng: float, max_lat: float, max_lng: float, filters: Dict[str, Any]) -> List[EvStation]:
        return list(db.ev_stations.values())

    def get_connector_live_status(self, station_id: str, connector_id: str) -> Dict[str, Any]:
        return {"status": "available", "protocol": "OCPI-2.2.1"}

    def start_remote_session(self, user_id: str, station_id: str, connector_id: str, target_soc: int) -> Dict[str, Any]:
        return {"result": "ACCEPTED", "command": "START_SESSION"}

    def stop_remote_session(self, session_id: str) -> Dict[str, Any]:
        return {"result": "ACCEPTED", "command": "STOP_SESSION"}

    def reserve_connector(self, station_id: str, connector_id: str, user_id: str, hold_minutes: int) -> Dict[str, Any]:
        return {"result": "ACCEPTED", "reservation_id": f"OCPI-RES-{int(time.time())}"}


class OcppCentralSystemAdapter(ChargingDataProvider):
    """OCPP 1.6J / 2.0.1 Central System Hardware Protocol Adapter"""
    def __init__(self, websocket_endpoint: str = "ws://localhost:8000/ocpp/ws"):
        self.endpoint = websocket_endpoint

    def fetch_stations(self, min_lat: float, min_lng: float, max_lat: float, max_lng: float, filters: Dict[str, Any]) -> List[EvStation]:
        return list(db.ev_stations.values())

    def get_connector_live_status(self, station_id: str, connector_id: str) -> Dict[str, Any]:
        return {"status": "Charging", "ocpp_version": "1.6J"}

    def start_remote_session(self, user_id: str, station_id: str, connector_id: str, target_soc: int) -> Dict[str, Any]:
        return {"status": "Accepted", "transactionId": 1024}

    def stop_remote_session(self, session_id: str) -> Dict[str, Any]:
        return {"status": "Accepted"}

    def reserve_connector(self, station_id: str, connector_id: str, user_id: str, hold_minutes: int) -> Dict[str, Any]:
        return {"status": "Accepted"}


class SimulatedChargingAdapter(ChargingDataProvider):
    """
    Default Live Stateful Demo Simulator.
    Emits realistic live status updates, manages active charging sessions with energy metrics,
    and supports 15-minute connector hold reservations.
    """

    def fetch_stations(self, min_lat: float, min_lng: float, max_lat: float, max_lng: float, filters: Dict[str, Any]) -> List[EvStation]:
        matched = []
        connector_filter = filters.get("connector_type")
        min_power = filters.get("min_power", 0.0)
        only_available = filters.get("only_available", False)

        for stn in db.ev_stations.values():
            if not (min_lat <= stn.lat <= max_lat and min_lng <= stn.lng <= max_lng):
                continue
            
            # Filter connectors
            filtered_connectors = []
            for conn in stn.connectors:
                if connector_filter and conn.connector_type != connector_filter:
                    continue
                if conn.power_kw < min_power:
                    continue
                if only_available and conn.status != "available":
                    continue
                filtered_connectors.append(conn)

            if filtered_connectors:
                stn_copy = stn.model_copy()
                stn_copy.connectors = filtered_connectors
                matched.append(stn_copy)

        return matched

    def get_connector_live_status(self, station_id: str, connector_id: str) -> Dict[str, Any]:
        stn = db.ev_stations.get(station_id)
        if not stn:
            return {"error": "Station not found"}
        for conn in stn.connectors:
            if conn.id == connector_id:
                return {
                    "station_id": station_id,
                    "connector_id": connector_id,
                    "connector_type": conn.connector_type,
                    "status": conn.status,
                    "power_kw": conn.power_kw,
                    "tariff_per_kwh": conn.tariff_per_kwh,
                    "last_heartbeat": conn.last_heartbeat
                }
        return {"error": "Connector not found"}

    def start_remote_session(self, user_id: str, station_id: str, connector_id: str, target_soc: int = 80) -> Dict[str, Any]:
        stn = db.ev_stations.get(station_id)
        if not stn:
            return {"success": False, "error": "Station not found"}
        
        target_conn = None
        for conn in stn.connectors:
            if conn.id == connector_id:
                target_conn = conn
                break

        if not target_conn:
            return {"success": False, "error": "Connector not found"}

        if target_conn.status not in ["available", "reserved"]:
            return {"success": False, "error": f"Connector is currently {target_conn.status}"}

        # Mark connector occupied
        target_conn.status = "occupied"
        target_conn.last_heartbeat = "Just now"

        session = EvSession(
            user_id=user_id,
            station_id=station_id,
            station_name=stn.name,
            connector_id=connector_id,
            connector_type=target_conn.connector_type,
            power_kw=target_conn.power_kw,
            energy_delivered_kwh=4.2,  # Initial progress for instant demo visual
            current_power_kw=target_conn.power_kw,
            soc_current_pct=34,
            soc_target_pct=target_soc,
            duration_mins=8,
            total_cost=round(4.2 * target_conn.tariff_per_kwh, 2),
            status="charging"
        )
        db.ev_sessions[session.id] = session

        return {
            "success": True,
            "session_id": session.id,
            "session": session.model_dump(),
            "message": "Charging session initiated successfully via Ai1 SmartGrid"
        }

    def stop_remote_session(self, session_id: str) -> Dict[str, Any]:
        session = db.ev_sessions.get(session_id)
        if not session:
            return {"success": False, "error": "Session not found"}

        session.status = "completed"
        session.current_power_kw = 0.0
        session.soc_current_pct = session.soc_target_pct
        session.energy_delivered_kwh = 18.6
        
        stn = db.ev_stations.get(session.station_id)
        tariff = 19.5
        if stn:
            for conn in stn.connectors:
                if conn.id == session.connector_id:
                    conn.status = "available"
                    conn.last_heartbeat = "Just now"
                    tariff = conn.tariff_per_kwh
                    break

        session.total_cost = round(session.energy_delivered_kwh * tariff, 2)

        return {
            "success": True,
            "session_id": session.id,
            "energy_delivered_kwh": session.energy_delivered_kwh,
            "total_cost": session.total_cost,
            "status": "completed",
            "message": "Charging stopped. Summary generated."
        }

    def reserve_connector(self, station_id: str, connector_id: str, user_id: str, hold_minutes: int = 15) -> Dict[str, Any]:
        stn = db.ev_stations.get(station_id)
        if not stn:
            return {"success": False, "error": "Station not found"}

        for conn in stn.connectors:
            if conn.id == connector_id:
                if conn.status != "available":
                    return {"success": False, "error": f"Connector cannot be reserved. Status is {conn.status}"}
                
                conn.status = "reserved"
                reservation = {
                    "reservation_id": f"RES-{int(time.time())}",
                    "station_id": station_id,
                    "connector_id": connector_id,
                    "user_id": user_id,
                    "expires_at_timestamp": int(time.time()) + (hold_minutes * 60),
                    "hold_minutes": hold_minutes,
                    "status": "active"
                }
                db.ev_reservations[reservation["reservation_id"]] = reservation
                return {
                    "success": True,
                    "reservation": reservation,
                    "message": f"Connector reserved for {hold_minutes} minutes. Please arrive before expiry to avoid no-show fee."
                }

        return {"success": False, "error": "Connector not found"}


# Global EV provider singleton
ev_charging_adapter = SimulatedChargingAdapter()
