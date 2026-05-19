import React, { useState, useEffect } from 'react';
import { ArrowLeft, Search, Plus, Minus } from 'lucide-react';
import './FAQPage.css';

export const allFaqs = [
  {
    id: 1,
    question: "FraudGuard AI ürünün kesin sahte olduğunu söyler mi?",
    answer: "Hayır. FraudGuard AI kesin sahte ürün kararı vermez. Üründeki şüpheli güven sinyallerini analiz eder ve kullanıcıya risk seviyesi sunar.",
    showOnLanding: true
  },
  {
    id: 2,
    question: "Trust Score ne anlama gelir?",
    answer: "Trust Score, ürünün yorum, fiyat, satıcı ve açıklama tutarlılığına göre 0–100 arasında hesaplanan güven skorudur. Skor yükseldikçe ürün daha güvenilir görünür.",
    showOnLanding: true
  },
  {
    id: 3,
    question: "Fiyat geçmişi yoksa sistem ne yapar?",
    answer: "Fiyat geçmişi yoksa sistem bunu eksik veri olarak gösterir. Bu durumda kesin “sahte indirim” demez; sadece indirimin doğrulanamadığını belirtir.",
    showOnLanding: true
  },
  {
    id: 4,
    question: "FraudGuard AI yorumları nasıl analiz eder?",
    answer: "Sistem yorumların benzerliğine, kısalığına, genel ifadeler içerip içermediğine, puan dağılımına ve yorumların ürün açıklamasıyla uyumuna bakar.",
    showOnLanding: true
  },
  {
    id: 5,
    question: "Canlı ürün linkleri her zaman çalışır mı?",
    answer: "Canlı ürün sayfaları değişken olduğu için her linkten veri çıkarma garanti edilmez. Bu nedenle sistem canlı extraction başarısız olursa fallback/demo veriyle çalışmaya devam edecek şekilde tasarlanmıştır.",
    showOnLanding: false
  },
  {
    id: 6,
    question: "Gemini burada ne işe yarıyor?",
    answer: "Gemini, ürün verilerini yapılandırmaya ve risk agent’larının sonuçlarını kullanıcı dostu bir açıklamaya dönüştürmeye yardımcı olur. Ancak sistem yalnızca Gemini’ye dayanmaz; rule-based risk agent’ları da çalışır.",
    showOnLanding: false
  },
  {
    id: 7,
    question: "FraudGuard AI hangi sitelerde çalışır?",
    answer: "MVP aşamasında öncelik Trendyol canlı extraction ve kontrollü demo ürün senaryolarıdır. İleride farklı e-ticaret platformları eklenebilir.",
    showOnLanding: false
  },
  {
    id: 8,
    question: "Kullanıcı hesabı gerekiyor mu?",
    answer: "MVP’de kullanıcı hesabı gerekmez. Kullanıcı yalnızca ürün linkini girerek analiz başlatabilir.",
    showOnLanding: false
  }
];

export default function FAQPage({ onBackToLanding, onEnterApp }) {
  const [openId, setOpenId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const toggleFaq = (id) => {
    setOpenId(openId === id ? null : id);
  };

  const filteredFaqs = allFaqs.filter(faq => 
    faq.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
    faq.answer.toLowerCase().includes(searchQuery.toLowerCase())
  );

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="faq-page-container">
      {/* Background patterns */}
      <div className="faq-bg-gradient"></div>
      
      <div className="faq-inner">
        <header className="faq-header">
          <button className="faq-btn-back" onClick={onBackToLanding}>
            <ArrowLeft size={18} />
            <span>Geri Dön</span>
          </button>
          
          <div className="faq-logo" onClick={onBackToLanding}>
            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
              <path d="M21 5c-1.11-.35-2.33-.5-3.5-.5-1.95 0-4.05.4-5.5 1.5-1.45-1.1-3.55-1.5-5.5-1.5S2.45 5 1 6v14.65c0 .25.25.5.5.5.1 0 .15-.05.25-.05C3.1 20.45 5.05 20 6.5 20c1.95 0 4.05.4 5.5 1.5 1.35-.85 3.1-1.3 4.85-1.45.15-.05.35-.05.5-.05.25 0 .5.25.5.5V6c-.6-.35-1.25-.7-2-.85V19c-1.1-.35-2.3-.5-3.5-.5-1.95 0-4.05.4-5.5 1.5V6.5c1.45-1.1 3.55-1.5 5.5-1.5s4.05.4 5.5 1.5c1.35-1.25 3.4-1.75 5.5-1.5V6c-.6-.35-1.25-.7-2-.85z" />
            </svg>
            <span>FraudGuard AI</span>
          </div>

          <button className="faq-btn-enter" onClick={onEnterApp}>
            Ürün Analiz Et
          </button>
        </header>

        <main className="faq-main">
          <div className="faq-title-area">
            <h1>Sıkça Sorulan Sorular</h1>
            <p>FraudGuard AI hakkında merak ettiğiniz tüm soruların cevapları bu sayfada.</p>
          </div>

          {/* Search bar */}
          <div className="faq-search-wrapper">
            <Search className="faq-search-icon" size={20} />
            <input 
              type="text" 
              placeholder="Sorularda arama yapın..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="faq-search-input"
            />
          </div>

          {/* FAQ Accordion List */}
          <div className="faq-accordion-list">
            {filteredFaqs.length > 0 ? (
              filteredFaqs.map((faq) => {
                const isOpen = openId === faq.id;
                return (
                  <div 
                    key={faq.id} 
                    className={`faq-item-card ${isOpen ? 'active' : ''}`}
                    onClick={() => toggleFaq(faq.id)}
                  >
                    <div className="faq-item-question">
                      <span className="faq-toggle-icon">
                        {isOpen ? <Minus size={20} /> : <Plus size={20} />}
                      </span>
                      <h3>{faq.question}</h3>
                    </div>
                    
                    <div className={`faq-item-answer ${isOpen ? 'show' : ''}`}>
                      <p>{faq.answer}</p>
                    </div>
                  </div>
                );
              })
            ) : (
              <div className="faq-no-results">
                Aramanızla eşleşen bir soru bulunamadı.
              </div>
            )}
          </div>
        </main>
      </div>

      <footer className="faq-footer">
        &copy; 2026 FraudGuard AI. Tüm hakları saklıdır.
      </footer>
    </div>
  );
}
