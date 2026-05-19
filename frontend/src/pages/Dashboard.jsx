import { useMemo, useState, useEffect } from "react";
import { ArrowLeft } from "lucide-react";
import { analyzeDemo, analyzeUrl } from "../api/fraudguardApi.js";
import AgentTimeline from "../components/AgentTimeline.jsx";
import AnalysisNotes from "../components/AnalysisNotes.jsx";
import EvidenceCards from "../components/EvidenceCards.jsx";
import GeminiExplanation from "../components/GeminiExplanation.jsx";
import LoadingSteps from "../components/LoadingSteps.jsx";
import MissingDataWarning from "../components/MissingDataWarning.jsx";
import PriceAnalysisCard from "../components/PriceAnalysisCard.jsx";
import ProductSummaryCard from "../components/ProductSummaryCard.jsx";
import RiskBadge from "../components/RiskBadge.jsx";
import ScoreBreakdown from "../components/ScoreBreakdown.jsx";
import TrustScoreCard from "../components/TrustScoreCard.jsx";
import UrlInput from "../components/UrlInput.jsx";

const demoProducts = [
  { id: "p001", label: "Düşük risk" },
  { id: "p002", label: "Yorum şüphesi" },
  { id: "p003", label: "İndirim anomalisi" },
  { id: "p004", label: "Satıcı riski" },
  { id: "p005", label: "Tutarlılık problemi" },
  { id: "p006", label: "Çoklu yüksek risk" },
  { id: "p007", label: "Orta risk" },
  { id: "p008", label: "Sınırda" },
];

const loadingSteps = [
  "Ürün linki işleniyor",
  "Risk agent'ları çalışıyor",
  "Gemini güven raporu hazırlanıyor",
  "Sonuç oluşturuluyor",
];

export default function Dashboard({ onBack, initialUrl }) {
  const [url, setUrl] = useState(initialUrl || "demo-air-fryer");
  const [selectedDemo, setSelectedDemo] = useState(initialUrl ? null : "p003");
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeStep, setActiveStep] = useState(0);

  const strongestAgent = useMemo(() => {
    if (!report?.agent_outputs?.length) return null;
    return [...report.agent_outputs].sort((a, b) => b.risk_score - a.risk_score)[0];
  }, [report]);

  async function runWithLoading(task) {
    setLoading(true);
    setError("");
    setReport(null);
    setActiveStep(0);

    const interval = window.setInterval(() => {
      setActiveStep((step) => Math.min(step + 1, loadingSteps.length - 1));
    }, 450);

    try {
      const result = await task();
      setReport(result);
      setActiveStep(loadingSteps.length - 1);
    } catch (err) {
      setError(err.message);
    } finally {
      window.clearInterval(interval);
      setLoading(false);
    }
  }

  function handleAnalyzeUrl(event) {
    event.preventDefault();
    runWithLoading(() => analyzeUrl(url));
  }

  function handleAnalyzeDemo(productId = selectedDemo) {
    setSelectedDemo(productId);
    setUrl(`demo-${productId}`);
    runWithLoading(() => analyzeDemo(productId));
  }

  useEffect(() => {
    if (initialUrl) {
      setUrl(initialUrl);
      if (initialUrl.startsWith("demo-")) {
        const demoId = initialUrl.replace("demo-", "");
        setSelectedDemo(demoId);
        runWithLoading(() => analyzeDemo(demoId));
      } else {
        setSelectedDemo(null);
        runWithLoading(() => analyzeUrl(initialUrl));
      }
    }
  }, [initialUrl]);

  return (
    <main className="app-shell">
      <section className="top-band">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          {onBack && (
            <button 
              onClick={onBack} 
              style={{
                background: 'rgba(59,130,246,0.08)',
                border: '1px solid rgba(59,130,246,0.2)',
                color: '#1d4ed8',
                borderRadius: '50%',
                width: '40px',
                height: '40px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(59,130,246,0.15)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(59,130,246,0.08)'}
              title="Landing Page'e Dön"
            >
              <ArrowLeft size={20} />
            </button>
          )}
          <div>
            <p className="eyebrow">FraudGuard AI</p>
            <h1>Ürün Güven Analizi</h1>
          </div>
        </div>
      </section>

      <section className="workspace-grid">
        <aside className="control-panel">
          <UrlInput
            url={url}
            onUrlChange={setUrl}
            onSubmit={handleAnalyzeUrl}
            loading={loading}
          />

          <div className="demo-list" aria-label="Demo ürünler">
            {demoProducts.map((item) => (
              <button
                key={item.id}
                className={selectedDemo === item.id ? "demo-button active" : "demo-button"}
                onClick={() => handleAnalyzeDemo(item.id)}
                type="button"
              >
                <span>{item.id}</span>
                {item.label}
              </button>
            ))}
          </div>

          <LoadingSteps steps={loadingSteps} activeStep={activeStep} loading={loading} />
        </aside>

        <section className="report-panel">
          {error && <div className="error-box">{error}</div>}

          {!report && !loading && !error && (
            <div className="empty-state">
              <div className="score-orbit">FG</div>
              <p>Bir demo senaryosu seç veya ürün linki gir.</p>
            </div>
          )}

          {loading && (
            <div className="analysis-state">
              <div className="pulse-ring" />
              <p>{loadingSteps[activeStep]}</p>
            </div>
          )}

          {report && (
            <div className="report-layout">
              <div className="score-row">
                <TrustScoreCard score={report.trust_score} />
                <RiskBadge level={report.risk_level} />
              </div>

              <ProductSummaryCard product={report.product} source={report.source} status={report.extraction_status} />

              <AnalysisNotes notes={report.analysis_notes} />

              <ScoreBreakdown agentOutputs={report.agent_outputs} trustScore={report.trust_score} />

              <div className="two-column">
                <PriceAnalysisCard product={report.product} />
                <GeminiExplanation explanation={report.gemini_explanation} />
              </div>

              <AgentTimeline agents={report.agent_outputs} strongestAgent={strongestAgent} />
              <EvidenceCards evidence={report.evidence} reasonCodes={report.reason_codes} />
              <MissingDataWarning fields={report.missing_fields} />
            </div>
          )}
        </section>
      </section>
    </main>
  );
}

