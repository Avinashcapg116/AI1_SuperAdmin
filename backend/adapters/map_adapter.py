"""
Ai1 Super App - Map & Geolocation Adapter
Provides geocoding, reverse geocoding, and EV route planning with charging stops.
"""

from typing import Dict, List, Any, Tuple
from backend.database.db import haversine_distance_km, db


class MapAdapter:
    """
    OpenStreetMap & Leaflet Geolocation Adapter.
    Zero API-keys required for local runs; clean drop-in interface for Google Maps / Mapbox.
    """

    KNOWN_LOCATIONS: Dict[str, Tuple[float, float]] = {
        "indiranagar": (12.9784, 77.6408),
        "koramangala": (12.9352, 77.6245),
        "hsr layout": (12.9116, 77.6389),
        "whitefield": (12.9698, 77.7500),
        "kempegowda international airport": (13.1986, 77.7066),
        "airport": (13.1986, 77.7066),
        "mg road": (12.9756, 77.6066),
        "electronic city": (12.8399, 77.6770),
        "bellandur": (12.9304, 77.6784),
        "hebbal": (13.0358, 77.5970)
    }

    def geocode(self, query: str) -> Dict[str, Any]:
        clean_q = query.lower().strip()
        for loc_name, coords in self.KNOWN_LOCATIONS.items():
            if loc_name in clean_q:
                return {
                    "address": query,
                    "lat": coords[0],
                    "lng": coords[1],
                    "city": "Bengaluru",
                    "matched": True
                }
        # Fallback to Central Bengaluru (MG Road)
        return {
            "address": query,
            "lat": 12.9756,
            "lng": 77.6066,
            "city": "Bengaluru",
            "matched": False
        }

    def calculate_eta_and_distance(self, lat1: float, lng1: float, lat2: float, lng2: float, speed_kmh: float = 30.0) -> Dict[str, Any]:
        dist_km = haversine_distance_km(lat1, lng1, lat2, lng2)
        duration_mins = max(5, int((dist_km / speed_kmh) * 60))
        return {
            "distance_km": dist_km,
            "duration_mins": duration_mins
        }

    def plan_ev_route(self, origin: str, destination: str, current_battery_pct: int, battery_capacity_kwh: float = 40.5, range_full_km: float = 312.0) -> Dict[str, Any]:
        p1 = self.geocode(origin)
        p2 = self.geocode(destination)
        dist_km = haversine_distance_km(p1["lat"], p1["lng"], p2["lat"], p2["lng"])

        # Calculate current remaining range
        available_range_km = (current_battery_pct / 100.0) * range_full_km
        needs_charging_stop = available_range_km < (dist_km * 1.2)  # 20% safety margin

        recommended_stops = []
        if needs_charging_stop or dist_km > 50:
            # Pick a station near intermediate route
            mid_lat = (p1["lat"] + p2["lat"]) / 2
            mid_lng = (p1["lng"] + p2["lng"]) / 2
            
            # Find closest EV station
            closest_stn = None
            min_stn_dist = 9999.0
            for stn in db.ev_stations.values():
                d = haversine_distance_km(mid_lat, mid_lng, stn.lat, stn.lng)
                if d < min_stn_dist:
                    min_stn_dist = d
                    closest_stn = stn

            if closest_stn:
                recommended_stops.append({
                    "station_id": closest_stn.id,
                    "station_name": closest_stn.name,
                    "address": closest_stn.address,
                    "recommended_charge_mins": 25,
                    "target_battery_pct": 80,
                    "lat": closest_stn.lat,
                    "lng": closest_stn.lng,
                    "available_fast_connectors": sum(1 for c in closest_stn.connectors if c.status == "available" and c.power_kw >= 50)
                })

        return {
            "origin": p1["address"],
            "destination": p2["address"],
            "total_distance_km": dist_km,
            "current_battery_pct": current_battery_pct,
            "estimated_current_range_km": round(available_range_km, 1),
            "needs_charging_stop": needs_charging_stop,
            "recommended_charging_stops": recommended_stops,
            "route_polyline_waypoints": [
                [p1["lat"], p1["lng"]],
                [(p1["lat"] + p2["lat"]) / 2, (p1["lng"] + p2["lng"]) / 2],
                [p2["lat"], p2["lng"]]
            ]
        }


map_adapter = MapAdapter()
