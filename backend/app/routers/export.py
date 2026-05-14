import csv
import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.schemas import HedisMeasure, Patient

router = APIRouter()


@router.get("/csv")
def export_quality_csv(db: Session = Depends(get_db)):
    rows = (
        db.query(HedisMeasure, Patient)
        .join(Patient, HedisMeasure.patient_id == Patient.id)
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["patient_id", "age", "gender", "payer", "measure_code",
                     "measure_name", "is_compliant", "last_encounter", "provider_type"])

    for measure, patient in rows:
        writer.writerow([
            patient.id, patient.age, patient.gender, patient.payer,
            measure.measure_code, measure.measure_name,
            measure.is_compliant, measure.last_encounter, measure.provider_type,
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=healthmetrics_export.csv"},
    )
