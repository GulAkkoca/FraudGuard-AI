import { AlertCircle, AlertTriangle, CheckCircle2 } from "lucide-react";

const labelMap = {
  Low: "Düşük Risk",
  Medium: "Orta Risk",
  High: "Yüksek Risk",
};

const iconMap = {
  Low: CheckCircle2,
  Medium: AlertCircle,
  High: AlertTriangle,
};

export default function RiskBadge({ level }) {
  const Icon = iconMap[level] || AlertCircle;
  return (
    <section className={`surface risk-badge ${String(level).toLowerCase()}`}>
      <Icon size={30} />
      <div>
        <span>Risk seviyesi</span>
        <strong>{labelMap[level] || level}</strong>
      </div>
    </section>
  );
}
