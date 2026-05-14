from datetime import date, datetime
from sqlalchemy import Boolean, Column, Date, DateTime, Decimal, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base


class Patient(Base):
    __tablename__ = "patients"
    __table_args__ = {"schema": "healthmetrics"}

    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    zip_code = Column(String(10))
    payer = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    measures = relationship("HedisMeasure", back_populates="patient")


class HedisMeasure(Base):
    __tablename__ = "hedis_measures"
    __table_args__ = {"schema": "healthmetrics"}

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("healthmetrics.patients.id"), nullable=False)
    measure_code = Column(String(20), nullable=False)
    measure_name = Column(String(100), nullable=False)
    is_compliant = Column(Boolean, nullable=False)
    last_encounter = Column(Date)
    provider_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="measures")


class QualitySummary(Base):
    __tablename__ = "quality_summary"
    __table_args__ = {"schema": "healthmetrics"}

    id = Column(Integer, primary_key=True)
    measure_code = Column(String(20), nullable=False)
    measure_name = Column(String(100), nullable=False)
    total_patients = Column(Integer, nullable=False)
    compliant_patients = Column(Integer, nullable=False)
    compliance_rate = Column(Decimal(5, 2), nullable=False)
    month_year = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
