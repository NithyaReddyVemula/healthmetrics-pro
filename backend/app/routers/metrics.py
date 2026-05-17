from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import get_db
from app.models.schemas import QualitySummary, Patient, HedisMeasure
from app.models.pydantic_models import MetricsDashboard, QualitySummaryOut

router = APIRouter()


def _from_quality_summary(db: Session):
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


def _from_patients(db: Session, payer, gender, min_age, max_age):
    patient_filter = db.query(Patient.id)
    if payer:
        patient_filter = patient_filter.filter(Patient.payer == payer)
    if gender:
        patient_filter = patient_filter.filter(Patient.gender == gender)
    if min_age is not None:
        patient_filter = patient_filter.filter(Patient.age >= min_age)
    if max_age is not None:
        patient_filter = patient_filter.filter(Patient.age <= max_age)

    patient_ids = [r[0] for r in patient_filter.all()]

    if not patient_ids:
        return MetricsDashboard(
            overall_compliance=0.0,
            total_patients=0,
            top_measure="N/A",
            bottom_measure="N/A",
            summaries=[],
        )

    results = (
        db.query(
            HedisMeasure.measure_code,
            HedisMeasure.measure_name,
            func.count(HedisMeasure.id).label("total_patients"),
            func.sum(func.cast(HedisMeasure.is_compliant, int)).label("compliant_patients"),
        )
        .filter(HedisMeasure.patient_id.in_(patient_ids))
        .group_by(HedisMeasure.measure_code, HedisMeasure.measure_name)
        .all()
    )

    if not results:
        return MetricsDashboard(
            overall_compliance=0.0,
            total_patients=len(patient_ids),
            top_measure="N/A",
            bottom_measure="N/A",
            summaries=[],
        )

    summaries = []
    rates = []
    for measure_code, measure_name, total, compliant in results:
        compliance_rate = round((compliant / total) * 100, 2) if total > 0 else 0.0
        rates.append((measure_name, compliance_rate))
        summaries.append(
            QualitySummaryOut(
                measure_code=measure_code,
                measure_name=measure_name,
                total_patients=total,
                compliant_patients=compliant,
                compliance_rate=compliance_rate,
                month_year=date.today(),
            )
        )

    overall = round(sum(r for _, r in rates) / len(rates), 2)
    top = max(rates, key=lambda x: x[1])[0]
    bottom = min(rates, key=lambda x: x[1])[0]

    return MetricsDashboard(
        overall_compliance=overall,
        total_patients=len(patient_ids),
        top_measure=top,
        bottom_measure=bottom,
        summaries=summaries,
    )


@router.get("/dashboard", response_model=MetricsDashboard)
def get_dashboard(
    payer: Optional[str] = None,
    gender: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    db: Session = Depends(get_db),
):
    # If no filters applied, use pre-computed QualitySummary for speed & backward compat
    if not any([payer, gender, min_age is not None, max_age is not None]):
        return _from_quality_summary(db)

    return _from_patients(db, payer, gender, min_age, max_age)
