import { ShieldCheck } from "lucide-react";

export default function TrustScoreCard({ score }) {
  const angle = Math.round((score / 100) * 360);
  return (
    <section className="surface score-card">
      <div className="section-title">
        <ShieldCheck size={19} />
        <h2>Trust Score</h2>
      </div>
      <div
        className="score-dial"
        style={{ background: `conic-gradient(var(--accent) ${angle}deg, var(--line) 0deg)` }}
      >
        <div>
          <strong>{score}</strong>
          <span>/ 100</span>
        </div>
      </div>
    </section>
  );
}

