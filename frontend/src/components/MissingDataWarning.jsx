import { Info } from "lucide-react";

export default function MissingDataWarning({ fields = [] }) {
  if (!fields.length) return null;

  return (
    <section className="surface missing-warning">
      <div className="section-title">
        <Info size={19} />
        <h2>Eksik Veri</h2>
      </div>
      <div className="missing-list">
        {fields.map((field) => (
          <span key={field}>{field}</span>
        ))}
      </div>
    </section>
  );
}

