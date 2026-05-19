import React, { useState, useRef, useEffect } from 'react';
import { ChevronRight, ArrowUpRight, Lock, Plus, Minus } from 'lucide-react';
import './LandingPage.css';
import { allFaqs } from './FAQPage.jsx';

export default function LandingPage({ onEnterApp, onGoToFAQ }) {
  const [showContent, setShowContent] = useState(false);
  const [openFaqId, setOpenFaqId] = useState(null);
  const [heroUrl, setHeroUrl] = useState('');
  const [headerClicked, setHeaderClicked] = useState(false);
  const [activeBlog, setActiveBlog] = useState(null);
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
              <a href="#Nasıl Çalışır" className="lp-nav-item">Nasıl Çalışır?</a>
              <a href="#FraudGuard AI Neleri Yakalar?" className="lp-nav-item">FraudGuard AI Neleri Yakalar?</a>
              <a href="#neden-fraudguard" className="lp-nav-item">Neden Fraud Guard</a>
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
              <div className="lp-card lp-glass-card lp-card-security" onClick={() => setActiveBlog('shield')}>
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
              <div className="lp-card lp-white-card lp-card-ai" onClick={() => setActiveBlog('gemini')}>
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
                
                <div className="lp-card lp-glass-card lp-card-stats" onClick={() => setActiveBlog('stats')}>
                  <h2>33<span>%</span></h2>
                  <p>E-ticaretteki yorumların %33'ünün<br />şüpheli veya yanıltıcı olduğunu biliyor muydunuz?</p>
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


        <section id="cozumler" className="lp-section lp-how-it-works-section">
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

        <section id="FraudGuard AI Neleri Yakalar?" className="lp-section">
          <div className="lp-section-content">
            <h2>FraudGuard AI Neleri Yakalar?</h2>
            <div className="lp-features-grid">
              <div className="lp-feature-item">
                <h3>Şüpheli Yorum Kalıpları</h3>
                <p>Benzer, kısa, aşırı genel veya zamanlama açısından olağan dışı yorumları analiz eder.</p>
              </div>
              <div className="lp-feature-item">
                <h3>Aşırı İndirim Sinyalleri</h3>
                <p>Güncel fiyat, eski fiyat ve varsa fiyat geçmişi üzerinden indirim güvenini değerlendirir.</p>
              </div>
              <div className="lp-feature-item">
                <h3>Satıcı Güven Sinyalleri</h3>
                <p>Satıcı adı, puanı, doğrulama bilgisi ve eksik satıcı verilerini kontrol eder.</p>
              </div>
              <div className="lp-feature-item">
                <h3>Ürün-Yorum Çelişkileri</h3>
                <p>Ürün açıklamasında vaat edilen özelliklerle yorumlardaki kullanıcı deneyimlerini karşılaştırır.</p>
              </div>
              <div className="lp-feature-item">
                <h3>Eksik Veri Uyarıları</h3>
                <p>Bilmediği şeyi uydurmaz; eksik alanları açıkça analiz notu olarak gösterir.</p>
              </div>
            </div>
          </div>
        </section>

        <section id="neden-fraudguard" className="lp-section">
          <div className="lp-section-content">
            <h2>Neden FraudGuard AI?</h2>
            <div className="lp-features-grid">
              <div className="lp-feature-item">
                <h3>Tek Linkle Güven Analizi</h3>
                <p>Ürün linkini gir, saniyeler içinde güven raporunu al.</p>
              </div>
              <div className="lp-feature-item">
                <h3>Sadece Yorumlara Bakmaz</h3>
                <p>Yorum, fiyat, satıcı ve ürün açıklamasını birlikte değerlendirir.</p>
              </div>
              <div className="lp-feature-item">
                <h3>Kanıta Dayalı Trust Score</h3>
                <p>Her skor reason code ve evidence kartlarıyla açıklanır.</p>
              </div>
              <div className="lp-feature-item">
                <h3>Gemini Açıklama Katmanı</h3>
                <p>Gemini skoru değiştirmez; agent sonuçlarını anlaşılır rapora dönüştürür.</p>
              </div>
              <div className="lp-feature-item">
                <h3>Eksik Veriyi Saklamaz</h3>
                <p>Fiyat geçmişi veya satıcı doğrulaması yoksa bunu açıkça gösterir.</p>
              </div>
            </div>
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
              <a href="#Nasıl Çalışır">Nasıl Çalışır?</a>
              <a href="#neden-fraudguard">Neden Fraud Guard</a>
              <a href="#FraudGuard AI Neleri Yakalar?">FraudGuard AI Neleri Yakalar?</a>
              <a href="#faq">FAQ</a>
            </div>
          </div>
          <div className="lp-footer-bottom">
            &copy; 2026 FraudGuard AI. Tüm hakları saklıdır.
          </div>
        </footer>
      </div>

      {/* Premium Blog Modal Overlay */}
      {activeBlog && (
        <div className="lp-blog-modal-backdrop" onClick={() => setActiveBlog(null)}>
          <div className="lp-blog-modal" onClick={(e) => e.stopPropagation()}>
            <button className="lp-blog-close" onClick={() => setActiveBlog(null)}>×</button>

            <div className="lp-blog-header">
              <span className="lp-blog-badge">
                {activeBlog === 'shield' ? 'Mühendislik' : activeBlog === 'gemini' ? 'Yapay Zeka' : 'Veri Analizi'}
              </span>
              <h1>
                {activeBlog === 'shield' && 'Review Shield: Sahte Yorum Dedektörü'}
                {activeBlog === 'gemini' && 'Gemini Trust Agent: Akıllı Anlamlandırma'}
                {activeBlog === 'stats' && '%33 Tehlikesi: E-Ticaretteki Büyük Aldatmaca'}
              </h1>
              <p className="lp-blog-subtitle">
                {activeBlog === 'shield' && 'Yapay zeka tabanlı algoritmalarımızla e-ticaret sitelerindeki şüpheli yorum paternlerini nasıl tespit ediyoruz?'}
                {activeBlog === 'gemini' && 'Çoklu risk ajanlarının teknik çıktılarını insan diline çeviren gelişmiş orkestrasyon mekanizması.'}
                {activeBlog === 'stats' && 'Neden online mağazalarda okuduğunuz neredeyse her iki yorumdan biri yanıltıcı olabilir?'}
              </p>
            </div>

            <div className="lp-blog-body">
              {activeBlog === 'shield' && (
                <div>
                  <p>İnternet alışverişinde en büyük güven kaynağımız diğer kullanıcıların yaptığı yorumlardır. Ancak bu yorumların ne kadarı samimi?</p>
                  <p><strong>Review Shield (Yorum Kalkanı)</strong>, e-ticaret sitelerinden çektiği verileri yapay zeka destekli özel kural motorlarından geçirerek sahte ve manipüle edilmiş yorum paternlerini açığa çıkarır.</p>
                  <h3>Nasıl Algılıyoruz?</h3>
                  <ul>
                    <li><strong>Yorum Patlaması (Review Burst):</strong> Bir ürünün belirli bir tarihte aniden olağan dışı sayıda yorum alıp almadığını ölçer.</li>
                    <li><strong>Semantik Benzerlik Analizi:</strong> Bot hesaplar veya bot-kampanyalar genellikle aynı şablon metinleri tekrar tekrar kullanırlar. Algoritmamız tüm yorum çiftlerinin benzerlik oranını hesaplar.</li>
                    <li><strong>Mantıksız Tekrar Alım (Nonsensical Repeat Buy):</strong> Tüketilemeyen, tek seferlik bir ürün (örneğin termos veya telefon kılıfı) için "sürekli stok yapıyorum, her ay alıyorum" yazan şüpheli yorumları cımbızla yakalar.</li>
                    <li><strong>Kısa ve Genel İfadeler:</strong> Ürünle hiçbir ilgisi olmayan, sadece puan yükseltmek için girilmiş genel kalıpları ("harika ürün", "teşekkürler", "kaliteli") tespit eder.</li>
                  </ul>
                </div>
              )}
              {activeBlog === 'gemini' && (
                <div>
                  <p>Güven analizi sadece ham verileri toplamakla bitmez. Kullanıcının neden bir ürüne güvenmesi veya şüpheyle yaklaşması gerektiğini net bir şekilde anlaması gerekir.</p>
                  <p><strong>Gemini Trust Agent</strong>, tüm teknik ajanlarımızdan (Review, Price, Seller, Consistency) gelen ham metrikleri ve kanıtları toplayan, üst düzey bir yapay zeka orkestratörüdür.</p>
                  <h3>Neden Farklı?</h3>
                  <ul>
                    <li><strong>İnsan Dilinde Raporlama:</strong> Size sadece kuru bir "30 risk puanı" demez. Gemini, bulguları harmanlayarak size dostça bir dille ürünün artılarını ve eksilerini açıklar.</li>
                    <li><strong>Öne Çıkan Riskler:</strong> Üründeki potansiyel tehlikeleri liste halinde sunar, böylece gözünüzden hiçbir ayrıntı kaçmaz.</li>
                    <li><strong>Önerilen Aksiyon:</strong> "Bu ürünü alırken son yorumları kontrol edin" veya "Satıcı puanı düşük olduğu için dikkat edin" gibi net tavsiyeler verir.</li>
                    <li><strong>Akıllı Fallback Yapısı:</strong> API bağlantısı kopsa veya kotalar dolsa bile sistemin kural tabanlı motoru çalışmaya devam eder ve size kesintisiz bir açıklama üretir.</li>
                  </ul>
                </div>
              )}
              {activeBlog === 'stats' && (
                <div>
                  <p>Her gün ziyaret ettiğimiz dev e-ticaret platformlarındaki yorumların şaşırtıcı bir kısmının aslında organik olmadığını biliyor muydunuz?</p>
                  <p>Akademik araştırmalar ve büyük e-ticaret analiz firmalarının raporları, dijital pazar yerlerindeki yorumların <strong>%33'ünün</strong> şüpheli, taraflı veya doğrudan sahte (satın alınmış) olduğunu ortaya koyuyor.</p>
                  <h3>Sistem Nasıl Manipüle Ediliyor?</h3>
                  <ul>
                    <li><strong>Ücretsiz Ürün Karşılığı Yorum:</strong> Satıcılar, kullanıcılara ürün hediye ederek karşılığında 5 yıldızlı olumlu yorumlar yazdırıyor.</li>
                    <li><strong>Kazanılmış Yorum Ajansları:</strong> Profesyonel gruplar, binlerce sahte hesap üzerinden sipariş verip anında olumlu değerlendirmeler yayınlıyor.</li>
                    <li><strong>Rakip Karalama Kampanyaları:</strong> Rakip markalar, rakiplerinin ürünlerine organize şekilde 1 yıldız vererek puan düşürmeye çalışıyor.</li>
                  </ul>
                  <p>FraudGuard AI, bu asimetrik bilgi savaşında tüketicinin yanında durur. Gerçek kullanıcı deneyimini sahte gürültüden arındırır.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
