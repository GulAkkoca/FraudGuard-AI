import { Info } from "lucide-react";

export default function AnalysisNotes({ notes }) {
  if (!notes || notes.length === 0) return null;

  return (
    <section className="surface">
      <div className="section-title">
        <Info size={18} />
        <h2>Analiz Notları</h2>
      </div>
      <div className="analysis-notes-card">
        {notes.map((note, i) => (
          <div key={i} className="note-item">
            <span className="note-dot" />
            {note}
          </div>
        ))}
      </div>
    </section>
  );
}
