"""
Ai1 Super App - Mechanic Solutions & Roadside Breakdown Assistance Module
Book car/bike servicing, doorstep repairs, breakdown/roadside assistance (towing, battery, flat tyre)
with SOS, vehicle profile maintenance reminders, and transparent estimate approval.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from backend.models.schemas import (
    MechanicPackage, MechanicJob, BookMechanicRequest, BreakdownSosRequest, User
)
from backend.modules.auth import get_current_user
from backend.database.db import db
from backend.adapters.payment_adapter import payment_adapter

router = APIRouter(prefix="/mechanic", tags=["Mechanic & Roadside Assistance"])


@router.get("/packages", response_model=List[MechanicPackage])
def get_mechanic_packages():
    return list(db.mechanic_packages.values())


@router.post("/book", response_model=MechanicJob)
def book_mechanic_service(req: BookMechanicRequest, user: User = Depends(get_current_user)):
    pkg = db.mechanic_packages.get(req.package_id)
    estimated_cost = pkg.price if pkg else 1499.0

    job = MechanicJob(
        user_id=user.id,
        service_type=pkg.title if pkg else "Custom Vehicle Repair",
        is_emergency_sos=False,
        vehicle_model=f"{req.vehicle_model} ({req.vehicle_number})",
        location_address=req.address,
        estimated_cost=estimated_cost,
        is_estimate_approved=True,
        status="technician_dispatched"
    )
    db.mechanic_jobs[job.id] = job
    return job


@router.post("/breakdown-sos", response_model=MechanicJob)
def emergency_breakdown_sos(req: BreakdownSosRequest, user: User = Depends(get_current_user)):
    emergency_cost_map = {
        "flat_tyre": 350.0,
        "battery_dead": 499.0,
        "towing": 1499.0,
        "accident": 1999.0,
        "engine_overheat": 650.0
    }
    cost = emergency_cost_map.get(req.emergency_type, 500.0)

    job = MechanicJob(
        user_id=user.id,
        service_type=f"Emergency RSA: {req.emergency_type.replace('_', ' ').title()}",
        is_emergency_sos=True,
        vehicle_model=f"{req.vehicle_type.upper()} Breakdown",
        location_address=req.location_address,
        estimated_cost=cost,
        is_estimate_approved=True,  # Auto-approved in emergency
        status="technician_dispatched"
    )
    db.mechanic_jobs[job.id] = job
    return job


@router.post("/jobs/{job_id}/approve-estimate")
def approve_estimate(job_id: str, user: User = Depends(get_current_user)):
    job = db.mechanic_jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.is_estimate_approved = True
    job.status = "repairing"

    # Deduct approved estimate from wallet
    pay_res = payment_adapter.debit_wallet(
        user_id=user.id,
        amount=job.estimated_cost,
        module="mechanic",
        ref_id=job.id,
        description=f"Mechanic Service: {job.service_type}"
    )

    return {
        "success": True,
        "job_id": job.id,
        "status": "repairing",
        "approved_cost": job.estimated_cost,
        "payment_status": "PAID_FROM_WALLET" if pay_res["success"] else "PENDING_CASH"
    }


@router.get("/jobs/{job_id}", response_model=MechanicJob)
def get_job(job_id: str):
    job = db.mechanic_jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
