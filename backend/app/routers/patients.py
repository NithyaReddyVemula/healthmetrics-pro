from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.schemas import Patient
from app.models.pydantic_models import PatientListOut, PatientOut

router = APIRouter()


@router.get("/", response_model=PatientListOut)
def list_patients(
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    payer: Optional[str] = None,
    gender: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Patient)

    if payer:
        q = q.filter(Patient.payer == payer)
    if gender:
        q = q.filter(Patient.gender == gender)
    if min_age is not None:
        q = q.filter(Patient.age >= min_age)
    if max_age is not None:
        q = q.filter(Patient.age <= max_age)

    total = q.count()
    patients = q.offset(offset).limit(limit).all()

    return PatientListOut(
        patients=[PatientOut.model_validate(p) for p in patients],
        total=total,
    )


@router.get("/payers")
def list_payers(db: Session = Depends(get_db)):
    rows = db.query(Patient.payer).distinct().all()
    return {"payers": [r[0] for r in rows if r[0]]}
