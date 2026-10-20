"""
Ai1 Super App - Main Backend Application Entrypoint
FastAPI Async Modular Monolith with OpenAPI Swagger & WebSockets
"""

import asyncio
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.config import settings
from backend.database.db import db
from backend.modules.auth import router as auth_router, user_router
from backend.modules.wallet import router as wallet_router
from backend.modules.quick_commerce import router as qc_router
from backend.modules.rides import router as rides_router
from backend.modules.home_services import router as services_router
from backend.modules.mechanic import router as mechanic_router
from backend.modules.travel import router as travel_router
from backend.modules.insurance import router as insurance_router
from backend.modules.ev_charging import router as ev_router
from backend.modules.assistant import router as assistant_router
from backend.modules.partner import router as partner_router
from backend.modules.admin import router as admin_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai1.main")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="India-First Super App unifiying Quick Commerce, Home Services, Mobility, Travel, Payments, Insurance, Real-Time EV Charging, and Voice AI.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for all local development and PWA domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Domain Routers under /api/v1
api_v1 = settings.API_V1_PREFIX
app.include_router(auth_router, prefix=api_v1)
app.include_router(user_router, prefix=api_v1)
app.include_router(wallet_router, prefix=api_v1)
app.include_router(qc_router, prefix=api_v1)
app.include_router(rides_router, prefix=api_v1)
app.include_router(services_router, prefix=api_v1)
app.include_router(mechanic_router, prefix=api_v1)
app.include_router(travel_router, prefix=api_v1)
app.include_router(insurance_router, prefix=api_v1)
app.include_router(ev_router, prefix=api_v1)
app.include_router(assistant_router, prefix=api_v1)
app.include_router(partner_router, prefix=api_v1)
app.include_router(admin_router, prefix=api_v1)


# WebSocket Connection Manager for Real-Time EV Viewports
class EvConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_status(self, data: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(json.dumps(data))
            except Exception:
                self.disconnect(connection)


ev_ws_manager = EvConnectionManager()


@app.websocket("/api/v1/ev/ws/viewport")
async def websocket_ev_viewport(websocket: WebSocket):
    """
    Real-time WebSocket feed pushing live status changes for visible chargers.
    """
    await ev_ws_manager.connect(websocket)
    try:
        while True:
            # Receive viewport bounding box or heartbeat from client
            data = await websocket.receive_text()
            # Periodically push a simulated status heartbeat or change
            stn = list(db.ev_stations.values())[0]
            update = {
                "event": "STATUS_UPDATE",
                "station_id": stn.id,
                "connector_id": stn.connectors[0].id,
                "status": stn.connectors[0].status,
                "last_heartbeat": "Just now",
                "freshness_seconds": 2
            }
            await websocket.send_text(json.dumps(update))
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        ev_ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ev_ws_manager.disconnect(websocket)


# Serve Frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    def serve_frontend_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "city": "Bengaluru",
        "modules_active": 9
    }
