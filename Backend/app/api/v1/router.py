from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, users, departments, categories, 
    assets, allocations, bookings, maintenance, audits, dashboard, reports, notifications
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(departments.router)
api_router.include_router(categories.router)
api_router.include_router(assets.router)
api_router.include_router(allocations.router)
api_router.include_router(bookings.router)
api_router.include_router(maintenance.router)
api_router.include_router(audits.router)
api_router.include_router(dashboard.router)
api_router.include_router(reports.router)
api_router.include_router(notifications.router)