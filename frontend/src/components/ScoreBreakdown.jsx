import { BarChart2, ShieldAlert, ShieldCheck, AlertTriangle, Info } from "lucide-react";

const AGENT_LABELS = {
  "Review Risk Agent": "Yorum Analizi",
  "Price Anomaly Agent": "Fiyat Anomalisi",
  "Seller Risk Agent": "Satıcı Riski",
  "Product Consistency Agent": "Ürün Tutarlılığı",
};

const AGENT_WEIGHTS = {
  "Review Risk Agent": 35,
  "Price Anomaly Agent": 25,
  "Seller Risk Agent": 25,
  "Product Consistency Agent": 15,
};

const AGENT_ICONS = {
  "Review Risk Agent": "💬",
  "Price Anomaly Agent": "💰",
  "Seller Risk Agent": "🏪",
  "Product Consistency Agent": "📋",
};

function getRiskColor(score) {
  if (score <= 30) return { bar: "#22c55e", text: "#15803d", bg: "rgba(34,197,94,0.08)", label: "Düşük" };
  if (score <= 55) return { bar: "#f59e0b", text: "#b45309", bg: "rgba(245,158,11,0.08)", label: "Orta" };
  if (score <= 75) return { bar: "#f97316", text: "#c2410c", bg: "rgba(249,115,22,0.08)", label: "Yüksek" };
  return { bar: "#ef4444", text: "#b91c1c", bg: "rgba(239,68,68,0.08)", label: "Kritik" };
}

export default function ScoreBreakdown({ agentOutputs, trustScore }) {
  if (!agentOutputs || agentOutputs.length === 0) return null;

  // Her agent'ın Trust Score'a katkısını hesapla
  const breakdown = agentOutputs.map((agent) => {
    const weight = AGENT_WEIGHTS[agent.agent_name] ?? 0;
    const riskContribution = Math.round((agent.risk_score * weight) / 100); // bu agent kaç puan risk ekledi
    const colors = getRiskColor(agent.risk_score);
    return {
      ...agent,
      label: AGENT_LABELS[agent.agent_name] ?? agent.agent_name,
      icon: AGENT_ICONS[agent.agent_name] ?? "🔍",
      weight,
      riskContribution,
      colors,
    };
  });

  const totalRisk = 100 - trustScore;

  return (
    <section className="surface">
      <div className="section-title">
        <BarChart2 size={19} />
        <h2>Puan Kırılımı</h2>
        <span style={{
          marginLeft: "auto",
          fontSize: "0.75rem",
          color: "var(--muted)",
          fontWeight: 600,
        }}>
          Toplam Risk: <strong style={{ color: "var(--ink)" }}>{totalRisk}</strong> / 100
        </span>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        {breakdown.map((item) => (
          <div
            key={item.agent_name}
            style={{
              background: item.colors.bg,
              border: `1px solid ${item.colors.bar}33`,
              borderRadius: "10px",
              padding: "0.85rem 1rem",
            }}
          >
            {/* Başlık satırı */}
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.5rem" }}>
              <span style={{ fontSize: "1.1rem" }}>{item.icon}</span>
              <span style={{ fontWeight: 700, color: "var(--ink)", fontSize: "0.9rem" }}>
                {item.label}
              </span>
              <span style={{
                marginLeft: "auto",
                fontSize: "0.72rem",
                color: "var(--muted)",
                fontWeight: 600,
              }}>
                Ağırlık: %{item.weight}
              </span>
              <span style={{
                fontSize: "0.8rem",
                fontWeight: 800,
                color: item.colors.text,
                background: `${item.colors.bar}18`,
                border: `1px solid ${item.colors.bar}44`,
                borderRadius: "999px",
                padding: "2px 10px",
                marginLeft: "0.4rem",
              }}>
                {item.label === "Düşük" ? "" : ""}{item.colors.label}
              </span>
            </div>

            {/* Progress bar */}
            <div style={{
              position: "relative",
              height: "8px",
              borderRadius: "999px",
              background: "rgba(0,0,0,0.07)",
              overflow: "hidden",
              marginBottom: "0.4rem",
            }}>
              <div style={{
                position: "absolute",
                left: 0,
                top: 0,
                height: "100%",
                width: `${item.risk_score}%`,
                background: item.colors.bar,
                borderRadius: "999px",
                transition: "width 0.8s cubic-bezier(0.25, 1, 0.5, 1)",
              }} />
            </div>

            {/* Alt bilgi */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontSize: "0.78rem", color: "var(--muted)" }}>
                Risk Skoru: <strong style={{ color: item.colors.text }}>{Math.round(item.risk_score)}/100</strong>
              </span>
              <span style={{ fontSize: "0.78rem", color: "var(--muted)" }}>
                Puana Etkisi:{" "}
                <strong style={{ color: item.riskContribution > 10 ? item.colors.text : "#15803d" }}>
                  −{item.riskContribution} puan
                </strong>
              </span>
            </div>

            {/* Reason codes — varsa */}
            {item.reason_codes && item.reason_codes.length > 0 && (
              <div style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "0.35rem",
                marginTop: "0.5rem",
              }}>
                {item.reason_codes.map((code) => (
                  <span key={code} style={{
                    fontSize: "0.68rem",
                    background: "rgba(0,0,0,0.05)",
                    border: "1px solid rgba(0,0,0,0.1)",
                    borderRadius: "999px",
                    padding: "2px 8px",
                    color: "var(--muted)",
                    fontWeight: 700,
                    fontFamily: "monospace",
                  }}>
                    {code}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Alt özet */}
      <div style={{
        marginTop: "1rem",
        padding: "0.75rem 1rem",
        background: "var(--surface-strong)",
        border: "1px solid var(--line)",
        borderRadius: "8px",
        display: "flex",
        alignItems: "center",
        gap: "0.5rem",
        fontSize: "0.82rem",
        color: "var(--muted)",
      }}>
        <Info size={14} style={{ flexShrink: 0 }} />
        Trust Score = 100 − (ağırlıklı ortalama risk) − eksik veri cezası
      </div>
    </section>
  );
}
