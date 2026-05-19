import React, { useState, useRef, useEffect } from 'react';
import { ChevronRight, ArrowUpRight, Lock, Plus, Minus } from 'lucide-react';
import './LandingPage.css';
import { allFaqs } from './FAQPage.jsx';

export default function LandingPage({ onEnterApp, onGoToFAQ }) {
  const [showContent, setShowContent] = useState(false);
  const [openFaqId, setOpenFaqId] = useState(null);
  const [heroUrl, setHeroUrl] = useState('');
  const [headerClicked, setHeaderClicked] = useState(false);
  const videoRef = useRef(null);

  const handleUrlSubmit = (e) => {
    e.preventDefault();
    if (heroUrl.trim()) {
      onEnterApp(heroUrl.trim());
    }
  };

  const handleHeaderClick = () => {
    setHeaderClicked(true);
    setTimeout(() => {
      onEnterApp('');
    }, 150);
  };

  useEffect(() => {
    const video = videoRef.current;
    if (video) {
      // Play video on load
      video.play().catch(e => console.log("Autoplay blocked", e));

      video.onended = () => {
        setShowContent(true);
      };
    }
  }, []);

  return (
    <div className="lp-container">
      {/* Video Background */}
      <div className="lp-video-wrapper">
        <video
          ref={videoRef}
          muted
          playsInline
          className="lp-video"
        >
          <source src="/bg-video.mp4" type="video/mp4" />
        </video>
        {/* Subtle overlay after video ends to make text readable */}
        <div className={`lp-video-overlay ${showContent ? 'active' : ''}`}></div>
      </div>

      {/* Hero Section — fades in after video ends */}
      <div className={`lp-hero-overlay ${showContent ? 'visible' : ''}`}>

        {/* Dev Arkaplan Yazısı (BLUE BIRD) */}
        <div className="lp-bg-text">
          <span>FRAUD       GUARD</span>
        </div>

        <div className="lp-inner">
          {/* Header Navigation */}
          <header className="lp-header">
            <div className="lp-logo" onClick={onEnterApp}>
              <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor">
                <path d="M21 5c-1.11-.35-2.33-.5-3.5-.5-1.95 0-4.05.4-5.5 1.5-1.45-1.1-3.55-1.5-5.5-1.5S2.45 5 1 6v14.65c0 .25.25.5.5.5.1 0 .15-.05.25-.05C3.1 20.45 5.05 20 6.5 20c1.95 0 4.05.4 5.5 1.5 1.35-.85 3.1-1.3 4.85-1.45.15-.05.35-.05.5-.05.25 0 .5.25.5.5V6c-.6-.35-1.25-.7-2-.85V19c-1.1-.35-2.3-.5-3.5-.5-1.95 0-4.05.4-5.5 1.5V6.5c1.45-1.1 3.55-1.5 5.5-1.5s4.05.4 5.5 1.5c1.35-1.25 3.4-1.75 5.5-1.5V6c-.6-.35-1.25-.7-2-.85z" />
              </svg>
            </div>

            <nav className="lp-nav">
              <a href="#anasayfa" className="lp-nav-item lp-nav-active">Anasayfa</a>
              <a href="#hakkimizda" className="lp-nav-item">Hakkımızda</a>
              <a href="#cozumler" className="lp-nav-item">Nasıl Çalışır?</a>
              <a href="#ozellikler" className="lp-nav-item">Özellikler</a>
              <a href="#neden fraud-guard" className="lp-nav-item">Neden Fraud Guard</a>
              <a href="#faq" className="lp-nav-item">FAQ</a>
            </nav>

            <button className={`lp-btn-resources ${headerClicked ? 'clicked-blue' : ''}`} onClick={handleHeaderClick}>
              Analiz Et
            </button>
          </header>

          {/* Main Content Area */}
          <main id="anasayfa" className="lp-main">

            {/* Left Side (Text & Input) */}
            <div className="lp-hero-text">
              <h1>
                Güvenli bir adım <br />
                <span>& Akıllı alışveriş</span>
              </h1>
              <p>
                E-ticarette manipülasyonu sonlandırın. Ürün linkini yapıştırın; sahte yorumları ve satıcı risklerini saniyeler içinde analiz edelim.
              </p>

              <div className="lp-hero-input-wrapper">
                <form onSubmit={handleUrlSubmit} className="lp-hero-form">
                  <input
                    type="url"
                    placeholder="Ürün linkini yapıştırın..."
                    value={heroUrl}
                    onChange={(e) => setHeroUrl(e.target.value)}
                    required
                    className="lp-hero-input"
                  />
                  <button type="submit" className="lp-btn-primary lp-hero-btn">
                    <span className="lp-btn-text">Analiz Et</span>
                    <span className="lp-btn-icon">
                      <ChevronRight size={18} />
                    </span>
                  </button>
                </form>
              </div>
            </div>

            {/* Right Side (Cards) */}
            <div className="lp-cards-container">

              {/* Left Small Card (Glass) */}
              <div className="lp-card lp-glass-card lp-card-security">
                <div className="lp-card-icon-wrapper">
                  <Lock size={32} />
                </div>
                <div className="lp-card-content">
                  <span className="lp-badge">Review Shield</span>
                  <h3>Sahte yorum sinyallerini tespit eder.</h3>
                </div>
                <ArrowUpRight className="lp-card-arrow" size={20} />
              </div>

              {/* Center Big Card (White) */}
              <div className="lp-card lp-white-card lp-card-ai">
                <div className="lp-orb">
                  <div className="lp-orb-inner"></div>
                </div>
                <div className="lp-card-content">
                  <h3>Gemini Trust Agent</h3>
                  <p>Yorum, fiyat, satıcı ve ürün tutarlılığı sinyallerini açıklar..</p>
                </div>
                <ArrowUpRight className="lp-card-arrow lp-arrow-dark" size={24} />
              </div>

              {/* Right Card (Glass) with Active Users */}
              <div className="lp-card-wrapper-right">
                <div className="lp-active-users">
                  <div className="lp-avatars">
                    <div className="lp-avatar lp-av-1"></div>
                    <div className="lp-avatar lp-av-2"></div>
                    <div className="lp-avatar lp-av-3"></div>
                  </div>
                  <span>Active Users <strong>+323</strong></span>
                </div>

                <div className="lp-card lp-glass-card lp-card-stats">
                  <h2>42<span>%</span></h2>
                  <p>E-ticaretteki yorumların %42'sinin<br />şüpheli veya yanıltıcı olduğunu biliyor muydunuz?</p>
                  <ArrowUpRight className="lp-card-arrow" size={20} />
                </div>
              </div>

            </div>
          </main>
        </div>
      </div>

      {/* Scrolling Sections — always visible, no video gate */}
      <div className="lp-sections-wrapper">
        <section id="hakkimizda" className="lp-section">
          <div className="lp-section-content">
            <h2>Hakkımızda</h2>
            <p> <strong>Online Alışverişte Gördüğün Her Şey Gerçek Olmayabilir  </strong> </p>

            <p> Yüksek puan, binlerce yorum ve büyük indirim… Hepsi güven verici görünebilir. Ama sahte yorumlar, şişirilmiş indirimler ve eksik satıcı bilgileri kullanıcıyı kolayca yanıltabilir.

              FraudGuard AI, ürün linkini analiz eder; yorumları, fiyat tutarlılığını, satıcı riskini ve ürün açıklamalarını birlikte değerlendirir.

              Sonuç: yalnızca bir puan değil, <strong>kanıta dayalı Trust Score.</strong></p>
            <p> <strong>Satın almadan önce riski gör, güvenle karar ver.</strong></p>

            <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'center' }}>
              <button
                className="lp-btn-primary"
                onClick={() => onEnterApp('')}
                style={{ fontSize: '1rem', padding: '0.5rem 0.5rem 0.5rem 1.75rem' }}
              >
                <span className="lp-btn-text">Analiz Et</span>
                <span className="lp-btn-icon">
                  <ChevronRight size={18} />
                </span>
              </button>
            </div>
          </div>
        </section>


        <section id="FraudGuardAI nasıl çalışır" className="lp-section lp-how-it-works-section">
          <div className="lp-section-content lp-how-it-works-content">
            <h2>Nasıl Çalışır?</h2>

            <div className="lp-steps-grid">
              {/* Row 1 */}
              <div className="lp-step-card">
                <div className="lp-step-number">01</div>
                <div className="lp-step-info">
                  <h3>Ürün Linkini Yapıştır</h3>
                  <p>Kullanıcı analiz etmek istediği ürün linkini FraudGuard AI’a yapıştırır.</p>
                </div>
              </div>

              <div className="lp-step-card">
                <div className="lp-step-number">02</div>
                <div className="lp-step-info">
                  <h3>Ürün Verisi Çıkarılır</h3>
                  <p>Sistem ürün adı, fiyat, satıcı bilgisi, yorumlar, puan ve ürün açıklaması gibi temel verileri çıkarır.</p>
                </div>
              </div>

              {/* Row 2 */}
              <div className="lp-step-card">
                <div className="lp-step-number">03</div>
                <div className="lp-step-info">
                  <h3>Risk Agent’ları Analiz Eder</h3>
                  <p>Yorum riski, fiyat anomalisi, satıcı güveni ve ürün açıklaması-yorum tutarlılığı ayrı ayrı değerlendirilir.</p>
                </div>
              </div>

              <div className="lp-step-card">
                <div className="lp-step-number">04</div>
                <div className="lp-step-info">
                  <h3>Trust Score Oluşturulur</h3>
                  <p>FraudGuard AI, ürüne 0–100 arasında bir güven skoru verir. Risk seviyesi, kanıt kartları ve eksik veri uyarıları kullanıcıya gösterilir.</p>
                </div>
              </div>

              {/* Row 3 - centered at bottom */}
              <div className="lp-step-card lp-step-card-last">
                <div className="lp-step-number">05</div>
                <div className="lp-step-info">
                  <h3>Güvenle Karar Ver</h3>
                  <p>Kullanıcı yalnızca puana değil, puanın neden oluştuğuna da bakarak daha bilinçli alışveriş kararı verir.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="ozellikler" className="lp-section">
          <div className="lp-section-content">
            <h2>Özellikler</h2>
            <div className="lp-features-grid">
              <div className="lp-feature-item">
                <h3>Gerçek Zamanlı Analiz</h3>
                <p>Gelen yorum ve puanlamaları saniyeler içinde tarayın.</p>
              </div>
              <div className="lp-feature-item">
                <h3>Detaylı Raporlama</h3>
                <p>Riskli durumları ve potansiyel sahtekarlıkları görselleştirin.</p>
              </div>
              <div className="lp-feature-item">
                <h3>Güvenilir Karar Destek</h3>
                <p>AI tarafından sağlanan açıklamalarla doğru kararlar verin.</p>
              </div>
            </div>
          </div>
        </section>

        <section id="tehdit" className="lp-section">
          <div className="lp-section-content">
            <h2></h2>
            <p>Sektörel veriler ve anlık trend analizleriyle yeni nesil sahtekarlık ağlarını keşfedin. Proaktif koruma kalkanımız sizi hep bir adım önde tutar.</p>
          </div>
        </section>

        <section id="faq" className="lp-section lp-faq-section">
          <div className="lp-section-content lp-faq-content">
            <h2>Sıkça Sorulan Sorular</h2>
            <div className="lp-faq-accordion">
              {allFaqs
                .filter(faq => faq.showOnLanding)
                .map(faq => {
                  const isOpen = openFaqId === faq.id;
                  return (
                    <div
                      key={faq.id}
                      className={`lp-faq-item ${isOpen ? 'active' : ''}`}
                      onClick={() => setOpenFaqId(isOpen ? null : faq.id)}
                    >
                      <div className="lp-faq-question">
                        <span className="lp-faq-toggle-icon">
                          {isOpen ? <Minus size={18} /> : <Plus size={18} />}
                        </span>
                        <h3>{faq.question}</h3>
                      </div>
                      <div className={`lp-faq-answer ${isOpen ? 'show' : ''}`}>
                        <p>{faq.answer}</p>
                      </div>
                    </div>
                  );
                })}
            </div>

            <div className="lp-faq-action">
              <button className="lp-btn-primary" onClick={onGoToFAQ}>
                Bütün Soruları Görüntüle
              </button>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="lp-footer">
          <div className="lp-footer-content">
            <div className="lp-footer-logo">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M21 5c-1.11-.35-2.33-.5-3.5-.5-1.95 0-4.05.4-5.5 1.5-1.45-1.1-3.55-1.5-5.5-1.5S2.45 5 1 6v14.65c0 .25.25.5.5.5.1 0 .15-.05.25-.05C3.1 20.45 5.05 20 6.5 20c1.95 0 4.05.4 5.5 1.5 1.35-.85 3.1-1.3 4.85-1.45.15-.05.35-.05.5-.05.25 0 .5.25.5.5V6c-.6-.35-1.25-.7-2-.85V19c-1.1-.35-2.3-.5-3.5-.5-1.95 0-4.05.4-5.5 1.5V6.5c1.45-1.1 3.55-1.5 5.5-1.5s4.05.4 5.5 1.5c1.35-1.25 3.4-1.75 5.5-1.5V6c-.6-.35-1.25-.7-2-.85z" />
              </svg>
              FraudGuard AI
            </div>
            <div className="lp-footer-links">
              <a href="#anasayfa">Anasayfa</a>
              <a href="#hakkimizda">Hakkımızda</a>
              <a href="#cozumler">Çözümler</a>
              <a href="#ozellikler">Özellikler</a>
              <a href="#">Gizlilik Politikası</a>
              <a href="#">Hizmet Şartları</a>
            </div>
          </div>
          <div className="lp-footer-bottom">
            &copy; 2026 FraudGuard AI. Tüm hakları saklıdır.
          </div>
        </footer>
      </div>
    </div>
  );
}
