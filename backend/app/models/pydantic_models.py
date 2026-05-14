from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class PatientOut(BaseModel):
    id: int
    age: int
    gender: str
    zip_code: Optional[str]
    payer: Optional[str]

    model_config = {"from_attributes": True}


class MeasureOut(BaseModel):
    measure_code: str
    measure_name: str
    is_compliant: bool
    last_encounter: Optional[date]

    model_config = {"from_attributes": True}


class QualitySummaryOut(BaseModel):
    measure_code: str
    measure_name: str
    total_patients: int
    compliant_patients: int
    compliance_rate: Decimal
    month_year: date

    model_config = {"from_attributes": True}


class MetricsDashboard(BaseModel):
    overall_compliance: float
    total_patients: int
    top_measure: str
    bottom_measure: str
    summaries: list[QualitySummaryOut]


class PatientListOut(BaseModel):
    patients: list[PatientOut]
    total: int
