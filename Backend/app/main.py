from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.services.allocation_service import AllocationConflictError

app = FastAPI(
    title="AssetFlow API",
    description="Backend engine for corporate asset tracking and resource scheduling",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS origins to let your React + Vite frontend communicate smoothly
# During hackathon development, settings.ALLOWED_ORIGINS can fall back to ["*"]
if settings.ALLOWED_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.ALLOWED_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Connect the domain-driven endpoints router
app.include_router(api_router, prefix="/api/v1")


# FIX: allocation_service.check_and_allocate raises a domain-specific
# AllocationConflictError, but nothing previously converted that into an
# HTTP response — it would have surfaced as an unhandled 500 the moment the
# allocations router was wired to call the service directly. This handler
# restores the documented 409 ASSET_ALREADY_ALLOCATED contract.
@app.exception_handler(AllocationConflictError)
async def allocation_conflict_handler(request: Request, exc: AllocationConflictError):
    return JSONResponse(
        status_code=409,
        content={"detail": exc.current_holder_info},
    )


@app.get("/health", tags=["Health Check"])
def health_check():
    """Simple health monitoring ping endpoint."""
    return {"status": "healthy", "service": "AssetFlow Backend"}