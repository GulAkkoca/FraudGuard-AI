import { Sparkles, AlertCircle, ShieldCheck } from "lucide-react";

export default function GeminiExplanation({ explanation }) {
  if (!explanation) return null;

  const isRuleBased = explanation.explanation_source === "rule_based";

  return (
    <section className="surface explanation-card">
      <div className="section-title">
        <Sparkles size={19} />
        <h2>Gemini Güven Raporu</h2>
        {isRuleBased && (
          <span style={{
            marginLeft: 'auto',
            fontSize: '0.7rem',
            background: 'rgba(19,134,111,0.1)',
            color: '#0b6656',
            border: '1px solid rgba(19,134,111,0.25)',
            borderRadius: '999px',
            padding: '2px 10px',
            fontWeight: 700,
          }}>Kural Tabanlı</span>
        )}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>

        {/* Gemini Özeti */}
        <div className="gemini-block">
          <span className="gemini-label">Gemini Özeti</span>
          <p className="gemini-text" style={{ fontWeight: 600, color: 'var(--ink)' }}>
            {explanation.summary || "Özet bulunamadı."}
          </p>
        </div>

        {/* Kullanıcı Dostu Açıklama */}
        <div className="gemini-block">
          <span className="gemini-label">Kullanıcı Dostu Açıklama</span>
          <p className="gemini-text">
            {explanation.user_friendly_explanation || "Açıklama bulunamadı."}
          </p>
        </div>

        {/* Öne Çıkan Riskler */}
        {explanation.key_concerns && explanation.key_concerns.length > 0 && (
          <div className="gemini-block">
            <span className="gemini-label">Öne Çıkan Riskler</span>
            <ul style={{ margin: 0, padding: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
              {explanation.key_concerns.map((concern, i) => (
                <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem', color: 'var(--muted)', fontSize: '0.9rem', lineHeight: 1.5 }}>
                  <AlertCircle size={14} style={{ marginTop: '3px', color: '#c77d16', flexShrink: 0 }} />
                  {concern}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Önerilen Aksiyon */}
        <div className="action-line" style={{ display: 'flex', alignItems: 'flex-start', gap: '0.6rem' }}>
          <ShieldCheck size={16} style={{ marginTop: '2px', color: 'var(--accent)', flexShrink: 0 }} />
          <div>
            <span className="gemini-label" style={{ display: 'block', marginBottom: '2px' }}>Önerilen Aksiyon</span>
            <span style={{ fontWeight: 700, color: 'var(--ink)' }}>
              {explanation.recommended_action || "Dikkatli inceleyin."}
            </span>
          </div>
        </div>

        {/* Confidence */}
        {explanation.confidence != null && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.82rem', color: 'var(--muted)' }}>
            <span>Analiz güven skoru:</span>
            <strong style={{ color: 'var(--accent-strong)' }}>%{explanation.confidence}</strong>
          </div>
        )}
      </div>
    </section>
  );
}
