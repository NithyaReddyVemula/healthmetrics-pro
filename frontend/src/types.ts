export interface Patient {
  id: number;
  age: number;
  gender: string;
  zip_code: string | null;
  payer: string | null;
}

export interface QualitySummary {
  measure_code: string;
  measure_name: string;
  total_patients: number;
  compliant_patients: number;
  compliance_rate: number;
  month_year: string;
}

export interface MetricsDashboard {
  overall_compliance: number;
  total_patients: number;
  top_measure: string;
  bottom_measure: string;
  summaries: QualitySummary[];
}

export interface PatientListResponse {
  patients: Patient[];
  total: number;
}

export interface Filters {
  payer?: string;
  gender?: string;
  min_age?: number;
  max_age?: number;
}
