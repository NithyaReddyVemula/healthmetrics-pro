interface KPICardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  color?: string;
}

export function KPICard({ title, value, subtitle, color = "#be185d" }: KPICardProps) {
  return (
    <div style={{
      background: "#1a0a1a",
      border: `1.5px solid ${color}44`,
      borderRadius: 12,
      padding: "20px 24px",
      minWidth: 160,
      flex: "1 1 160px",
    }}>
      <div style={{ fontSize: "0.72rem", color: "#94a3b8", textTransform: "uppercase",
        letterSpacing: "0.08em", marginBottom: 8 }}>
        {title}
      </div>
      <div style={{ fontSize: "2rem", fontWeight: 900, color, lineHeight: 1 }}>
        {value}
      </div>
      {subtitle && (
        <div style={{ fontSize: "0.75rem", color: "#64748b", marginTop: 6 }}>{subtitle}</div>
      )}
    </div>
  );
}
