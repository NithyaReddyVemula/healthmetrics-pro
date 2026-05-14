import { getExportUrl } from "../api";

export function ExportButton() {
  return (
    <a href={getExportUrl()} download="healthmetrics_export.csv"
      style={{
        display: "inline-block", padding: "8px 20px",
        background: "transparent", border: "1.5px solid #be185d",
        borderRadius: 8, color: "#f9a8d4", fontSize: "0.82rem",
        fontWeight: 700, textDecoration: "none", letterSpacing: "0.05em",
      }}>
      ↓ Export CSV
    </a>
  );
}
