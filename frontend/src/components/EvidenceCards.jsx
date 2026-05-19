import { FileText, Tag } from "lucide-react";

export default function EvidenceCards({ evidence = [], reasonCodes = [] }) {
  return (
    <section className="surface">
      <div className="section-title">
        <FileText size={19} />
        <h2>Kanıtlar</h2>
      </div>
      <div className="reason-row">
        {reasonCodes.map((code) => (
          <span key={code}>
            <Tag size={13} />
            {code}
          </span>
        ))}
      </div>
      <div className="evidence-list">
        {evidence.length ? (
          evidence.map((item, index) => <p key={`${item}-${index}`}>{item}</p>)
        ) : (
          <p>Belirgin risk kanıtı bulunmadı.</p>
        )}
      </div>
    </section>
  );
}

