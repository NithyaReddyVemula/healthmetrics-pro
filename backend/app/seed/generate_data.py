"""
Run: python -m app.seed.generate_data
Generates 500 synthetic patients + HEDIS measure records.
Safe to run multiple times — clears existing data first.
"""
import os
import random
from datetime import date, timedelta
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

from app.models.database import engine, SessionLocal
from app.models.schemas import Patient, HedisMeasure, QualitySummary

HEDIS_MEASURES = [
    ("BCS", "Breast Cancer Screening"),
    ("COL", "Colorectal Cancer Screening"),
    ("CDC-HbA1c", "Diabetes HbA1c Control"),
    ("CDC-Eye", "Diabetes Eye Exam"),
    ("CBP", "Controlling Blood Pressure"),
    ("CIS", "Childhood Immunizations"),
    ("AWC", "Adolescent Well-Care"),
    ("AMB-ED", "Ambulatory Care - ED Utilization"),
    ("FUH", "Follow-up After Hospitalization - Mental Health"),
    ("LBP", "Use of Imaging for Low Back Pain"),
    ("PBH-A", "Prevention and Screening - Unhealthy Alcohol Use"),
    ("W34", "Well-Child Visits 3-6 Years"),
]

PAYERS = ["Cigna", "Aetna", "UnitedHealth", "BlueCross", "Humana", "Medicaid"]
PROVIDER_TYPES = ["Primary Care", "Specialist", "OB-GYN", "Pediatrics", "Urgent Care"]
GENDERS = ["Male", "Female", "Non-binary"]
ZIP_CODES = [f"{z:05d}" for z in random.sample(range(75000, 76000), 50)]


def random_date(start_year: int = 2023) -> date:
    start = date(start_year, 1, 1)
    end = date(2025, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def generate():
    db = SessionLocal()
    try:
        db.execute(text("DELETE FROM healthmetrics.quality_summary"))
        db.execute(text("DELETE FROM healthmetrics.hedis_measures"))
        db.execute(text("DELETE FROM healthmetrics.patients"))
        db.commit()

        print("Generating 500 patients...")
        patients = []
        for _ in range(500):
            p = Patient(
                age=random.randint(18, 85),
                gender=random.choice(GENDERS),
                zip_code=random.choice(ZIP_CODES),
                payer=random.choice(PAYERS),
            )
            db.add(p)
            patients.append(p)
        db.flush()

        print("Generating HEDIS measures...")
        for patient in patients:
            for code, name in HEDIS_MEASURES:
                is_compliant = random.random() < random.uniform(0.60, 0.85)
                measure = HedisMeasure(
                    patient_id=patient.id,
                    measure_code=code,
                    measure_name=name,
                    is_compliant=is_compliant,
                    last_encounter=random_date() if is_compliant else None,
                    provider_type=random.choice(PROVIDER_TYPES) if is_compliant else None,
                )
                db.add(measure)

        db.commit()

        print("Generating quality summary...")
        for code, name in HEDIS_MEASURES:
            measures = db.query(HedisMeasure).filter(HedisMeasure.measure_code == code).all()
            total = len(measures)
            compliant = sum(1 for m in measures if m.is_compliant)
            rate = round((compliant / total) * 100, 2) if total > 0 else 0.0

            summary = QualitySummary(
                measure_code=code,
                measure_name=name,
                total_patients=total,
                compliant_patients=compliant,
                compliance_rate=rate,
                month_year=date(2025, 1, 1),
            )
            db.add(summary)

        db.commit()
        print(f"Done. 500 patients, {500 * 12} measures, {len(HEDIS_MEASURES)} summaries.")

    finally:
        db.close()


if __name__ == "__main__":
    generate()
