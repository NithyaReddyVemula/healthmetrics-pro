import type { QualitySummary } from "../types";

interface Props {
  summaries: QualitySummary[];
}

export function MeasureTable({ summaries }: Props) {
  const sorted = [...summaries].sort(
    (a, b) => Number(b.compliance_rate) - Number(a.compliance_rate)
  );

  return (
    <div style={{ background: "#0f060f", border: "1px solid #4a134066",
      borderRadius: 12, overflow: "hidden" }}>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#1a0a1a" }}>
            {["Measure", "Code", "Compliant", "Total", "Rate"].map((h) => (
              <th key={h} style={{ padding: "10px 16px", textAlign: "left",
                fontSize: "0.7rem", color: "#94a3b8", textTransform: "uppercase",
                letterSpacing: "0.08em", fontWeight: 700 }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.map((s, i) => {
            const rate = Number(s.compliance_rate);
            const color = rate >= 80 ? "#6ee7b7" : rate >= 65 ? "#f9a8d4" : "#f87171";
            return (
              <tr key={s.measure_code}
                style={{ borderTop: "1px solid #2a0f2a",
                  background: i % 2 === 0 ? "transparent" : "#0d060d" }}>
                <td style={{ padding: "10px 16px", fontSize: "0.82rem",
                  color: "#e0d0e8" }}>{s.measure_name}</td>
                <td style={{ padding: "10px 16px", fontSize: "0.75rem",
                  color: "#94a3b8", fontFamily: "monospace" }}>{s.measure_code}</td>
                <td style={{ padding: "10px 16px", fontSize: "0.82rem",
                  color: "#e0d0e8" }}>{s.compliant_patients}</td>
                <td style={{ padding: "10px 16px", fontSize: "0.82rem",
                  color: "#e0d0e8" }}>{s.total_patients}</td>
                <td style={{ padding: "10px 16px" }}>
                  <span style={{ color, fontWeight: 700, fontSize: "0.85rem" }}>
                    {rate.toFixed(1)}%
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
