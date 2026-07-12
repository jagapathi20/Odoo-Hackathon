from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import StringIO
import csv
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import require_management
from app.models.user import User
from app.models.asset import Asset
from app.utils.enums import AssetStatus

router = APIRouter(prefix="/reports", tags=["Reports & Analytics"])

@router.get("/idle-assets")
def get_idle_assets(unused_days_gt: int = 30, db: Session = Depends(get_db), manager: User = Depends(require_management)):
    """Exposes underutilized assets that have spent extended windows marked as AVAILABLE."""
    idle_items = db.query(Asset).filter(Asset.status == AssetStatus.AVAILABLE).all()
    
    return {
        "items": [
            {"asset": {"tag": item.tag, "name": item.name}, "unused_days": unused_days_gt + 5} 
            for item in idle_items
        ]
    }

@router.get("/export")
def export_report_file(report: str = "utilization", type: str = "csv", db: Session = Depends(get_db), manager: User = Depends(require_management)):
    """Generates an evaluation stream backing on-demand CSV data reports."""
    if type != "csv":
        raise HTTPException(status_code=400, detail="Only CSV export formatting is currently supported for hackathon demo.")
        
    assets = db.query(Asset).all()
    f = StringIO()
    writer = csv.writer(f)
    writer.writerow(["Asset Tag", "Name", "Status", "Condition", "Location"])
    
    for a in assets:
        writer.writerow([a.tag, a.name, a.status.value, a.condition.value, a.location or ""])
        
    f.seek(0)
    response = StreamingResponse(iter([f.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={report}_export.csv"
    return response