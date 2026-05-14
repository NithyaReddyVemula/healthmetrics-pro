from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.schemas import QualitySummary
from app.models.pydantic_models import MetricsDashboard, QualitySummaryOut

router = APIRouter()


@router.get("/dashboard", response_model=MetricsDashboard)
def get_dashboard(db: Session = Depends(get_db)):
    summaries = db.query(QualitySummary).all()

    if not summaries:
        return MetricsDashboard(
            overall_compliance=0.0,
            total_patients=0,
            top_measure="N/A",
            bottom_measure="N/A",
            summaries=[],
        )

    rates = [(s.measure_name, float(s.compliance_rate)) for s in summaries]
    overall = round(sum(r for _, r in rates) / len(rates), 2)
    top = max(rates, key=lambda x: x[1])[0]
    bottom = min(rates, key=lambda x: x[1])[0]
    total = summaries[0].total_patients if summaries else 0

    return MetricsDashboard(
        overall_compliance=overall,
        total_patients=total,
        top_measure=top,
        bottom_measure=bottom,
        summaries=[QualitySummaryOut.model_validate(s) for s in summaries],
    )
