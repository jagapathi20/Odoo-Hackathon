from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

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

@app.get("/health", tags=["Health Check"])
def health_check():
    """Simple health monitoring ping endpoint."""
    return {"status": "healthy", "service": "AssetFlow Backend"}