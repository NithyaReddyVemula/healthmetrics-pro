import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
} from "recharts";
import type { QualitySummary } from "../types";

interface Props {
  summaries: QualitySummary[];
}

export function QualityChart({ summaries }: Props) {
  const data = summaries.map((s) => ({
    name: s.measure_code,
    rate: Number(s.compliance_rate),
  }));

  return (
    <div style={{ background: "#0f060f", border: "1px solid #4a134066",
      borderRadius: 12, padding: "20px 16px" }}>
      <div style={{ fontSize: "0.8rem", color: "#f9a8d4", fontWeight: 700,
        marginBottom: 16 }}>
        Compliance Rate by Measure
      </div>
      <ResponsiveContainer width="100%" height={220}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="rateGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#be185d" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#be185d" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a0f2a" />
          <XAxis dataKey="name" tick={{ fill: "#64748b", fontSize: 10 }} />
          <YAxis domain={[0, 100]} tick={{ fill: "#64748b", fontSize: 10 }} unit="%" />
          <Tooltip
            contentStyle={{ background: "#1a0a1a", border: "1px solid #be185d55",
              borderRadius: 8, color: "#f9a8d4" }}
            formatter={(v: number) => [`${v.toFixed(1)}%`, "Compliance"]}
          />
          <Area type="monotone" dataKey="rate" stroke="#be185d"
            fill="url(#rateGrad)" strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
