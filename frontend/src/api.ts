import axios from "axios";
import type { MetricsDashboard, PatientListResponse, Filters } from "./types";

const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
const api = axios.create({ baseURL: BASE });

export async function fetchDashboard(): Promise<MetricsDashboard> {
  const { data } = await api.get<MetricsDashboard>("/api/metrics/dashboard");
  return data;
}

export async function fetchPatients(
  filters: Filters = {},
  limit = 50,
  offset = 0
): Promise<PatientListResponse> {
  const { data } = await api.get<PatientListResponse>("/api/patients/", {
    params: { ...filters, limit, offset },
  });
  return data;
}

export async function fetchPayers(): Promise<string[]> {
  const { data } = await api.get<{ payers: string[] }>("/api/patients/payers");
  return data.payers;
}

export function getExportUrl(): string {
  return `${BASE}/api/export/csv`;
}
