import { Sparkles } from "lucide-react";

export default function GeminiExplanation({ explanation }) {
  if (!explanation) return null;
  return (
    <section className="surface explanation-card">
      <div className="section-title">
        <Sparkles size={19} />
        <h2>Güven Raporu</h2>
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div>
          <span style={{ display: 'block', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#a0aec0', marginBottom: '0.25rem' }}>Gemini Özeti</span>
          <strong>{explanation.summary || "Özet bulunamadı."}</strong>
        </div>

        <div>
          <span style={{ display: 'block', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#a0aec0', marginBottom: '0.25rem' }}>Kullanıcı Dostu Açıklama</span>
          <p style={{ margin: 0 }}>{explanation.user_friendly_explanation || "Açıklama bulunamadı."}</p>
        </div>

        <div>
          <span style={{ display: 'block', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#a0aec0', marginBottom: '0.25rem' }}>Öne Çıkan Riskler</span>
          <p style={{ margin: 0 }}>{explanation.highlighted_risks || "Belirgin bir risk saptanmadı."}</p>
        </div>

        <div className="action-line">
          <span style={{ display: 'block', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#a0aec0', marginBottom: '0.25rem' }}>Önerilen Aksiyon</span>
          <div>{explanation.recommended_action || "Aksiyon önerisi bulunamadı."}</div>
        </div>

        <div>
          <span style={{ display: 'block', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#a0aec0', marginBottom: '0.25rem' }}>Gemini Confidence</span>
          <strong>{explanation.confidence ? `%${explanation.confidence}` : "%85"}</strong>
        </div>
      </div>
    </section>
  );
}

