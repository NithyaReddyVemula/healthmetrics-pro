import { useEffect, useState } from "react";
import { fetchDashboard } from "../api";
import type { MetricsDashboard, Filters } from "../types";
import { KPICard } from "./KPICard";
import { QualityChart } from "./QualityChart";
import { MeasureTable } from "./MeasureTable";
import { PatientFilter } from "./PatientFilter";
import { ExportButton } from "./ExportButton";

export function Dashboard() {
  const [data, setData] = useState<MetricsDashboard | null>(null);
  const [filters, setFilters] = useState<Filters>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboard()
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div style={{ color: "#f9a8d4", textAlign: "center", marginTop: 80, fontSize: "1.1rem" }}>
      Loading clinical data...
    </div>
  );

  if (!data) return (
    <div style={{ color: "#f87171", textAlign: "center", marginTop: 80 }}>
      Failed to load data. Check API connection.
    </div>
  );

  return (
    <div style={{ minHeight: "100vh", background: "#080308", color: "#e0d0e8",
      fontFamily: "system-ui, sans-serif", padding: "32px 40px" }}>

      <div style={{ display: "flex", justifyContent: "space-between",
        alignItems: "flex-start", marginBottom: 32 }}>
        <div>
          <div style={{ fontSize: "0.72rem", color: "#be185d", fontWeight: 700,
            textTransform: "uppercase", letterSpacing: "0.12em", marginBottom: 6 }}>
            Clinical Intelligence
          </div>
          <h1 style={{ fontSize: "1.8rem", fontWeight: 900, color: "#fdf2f8", margin: 0 }}>
            HealthMetrics Pro
          </h1>
          <p style={{ color: "#94a3b8", marginTop: 4, fontSize: "0.88rem" }}>
            HEDIS Quality Compliance Dashboard
          </p>
        </div>
        <ExportButton />
      </div>

      <div style={{ display: "flex", gap: 16, marginBottom: 24, flexWrap: "wrap" }}>
        <KPICard title="Overall Compliance"
          value={`${data.overall_compliance.toFixed(1)}%`}
          subtitle="Across all HEDIS measures" color="#be185d" />
        <KPICard title="Total Patients"
          value={data.total_patients.toLocaleString()}
          subtitle="In current cohort" color="#7c2d6b" />
        <KPICard title="Top Measure"
          value={data.top_measure}
          subtitle="Highest compliance" color="#6ee7b7" />
        <KPICard title="Needs Attention"
          value={data.bottom_measure}
          subtitle="Lowest compliance" color="#f9a8d4" />
      </div>

      <div style={{ marginBottom: 24 }}>
        <PatientFilter filters={filters} onChange={setFilters} />
      </div>

      <div style={{ marginBottom: 24 }}>
        <QualityChart summaries={data.summaries} />
      </div>

      <MeasureTable summaries={data.summaries} />
    </div>
  );
}
