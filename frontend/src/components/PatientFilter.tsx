import { useEffect, useState } from "react";
import { fetchPayers } from "../api";
import type { Filters } from "../types";

interface Props {
  filters: Filters;
  onChange: (f: Filters) => void;
}

const selectStyle: React.CSSProperties = {
  background: "#1a0a1a", border: "1px solid #4a1340", borderRadius: 8,
  color: "#e0d0e8", padding: "6px 12px", fontSize: "0.82rem", cursor: "pointer",
};

export function PatientFilter({ filters, onChange }: Props) {
  const [payers, setPayers] = useState<string[]>([]);

  useEffect(() => {
    fetchPayers().then(setPayers).catch(() => {});
  }, []);

  return (
    <div style={{ display: "flex", gap: 12, flexWrap: "wrap", alignItems: "center",
      background: "#0f060f", border: "1px solid #4a134066", borderRadius: 12,
      padding: "14px 20px" }}>
      <span style={{ fontSize: "0.75rem", color: "#94a3b8", fontWeight: 700,
        textTransform: "uppercase", letterSpacing: "0.08em" }}>Filters:</span>

      <select style={selectStyle} value={filters.payer || ""}
        onChange={(e) => onChange({ ...filters, payer: e.target.value || undefined })}>
        <option value="">All Payers</option>
        {payers.map((p) => <option key={p} value={p}>{p}</option>)}
      </select>

      <select style={selectStyle} value={filters.gender || ""}
        onChange={(e) => onChange({ ...filters, gender: e.target.value || undefined })}>
        <option value="">All Genders</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
        <option value="Non-binary">Non-binary</option>
      </select>

      <select style={selectStyle} value={filters.min_age || ""}
        onChange={(e) => onChange({ ...filters, min_age: e.target.value ? Number(e.target.value) : undefined })}>
        <option value="">Min Age</option>
        {[18, 30, 40, 50, 60, 70].map((a) => <option key={a} value={a}>{a}+</option>)}
      </select>

      {(filters.payer || filters.gender || filters.min_age) && (
        <button style={{ ...selectStyle, color: "#f9a8d4", border: "1px solid #be185d55" }}
          onClick={() => onChange({})}>
          Clear
        </button>
      )}
    </div>
  );
}
