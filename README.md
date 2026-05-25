# FraudGuard AI - Sahte Yorum ve Urun Guven Analizi

FraudGuard AI, e-ticaret urun linklerini analiz ederek sahte yorum, sisirilmis indirim, riskli satici ve urun aciklamasi-yorum uyumsuzluklarini tespit eden coklu agent tabanli bir karar destek sistemidir.

Proje, kullaniciya yalnizca bir puan gostermek yerine bu puanin neden olustugunu kanitlariyla aciklar. Boylece tuketici, yuksek puanli veya buyuk indirimli gorunen bir urunun gercekten guvenilir olup olmadigini daha bilincli degerlendirebilir.

## Problem

Online alisveriste kullanicilar genellikle su sinyallere guvenir:

- Yuksek yildiz puani
- Cok sayida olumlu yorum
- Buyuk indirim orani
- Guvenilir gorunen satici profili

Ancak bu sinyaller manipule edilebilir. Sahte yorumlar, tekrar eden yorum kaliplari, yapay indirimler, yeni veya dogrulanmamis saticilar ve urun aciklamasiyla celisen kullanici deneyimleri tuketiciyi yaniltabilir.

FraudGuard AI bu problemi cozmek icin urunu birden fazla risk katmanindan gecirir ve sonuc olarak aciklanabilir bir `Trust Score` uretir.

## Ana Ozellikler

- **URL veya demo urun analizi:** Kullanici canli bir urun linki girebilir ya da hazir demo senaryolarindan birini secebilir.
- **Trust Score:** Urun icin 0-100 araliginda guven skoru uretilir.
- **Coklu risk agent mimarisi:** Yorum, fiyat, satici ve tutarlilik riskleri ayri agent'lar tarafindan analiz edilir.
- **Gemini Trust Orchestrator:** Agent ciktilari ve kanitlar kullanici dostu bir rapora donusturulur.
- **Score Breakdown:** Final skorun hangi agent katkilarindan olustugu gorsel olarak aciklanir.
- **Evidence Cards:** Karari etkileyen somut kanitlar listelenir.
- **Missing Data Warning:** Eksik veri varsa analiz sinirlari seffaf sekilde gosterilir.
- **Agent Timeline:** Hangi agent'in ne kadar risk buldugu kullaniciya adim adim sunulur.

## Sistem Mimarisi

FraudGuard AI iki ana katmandan olusur:

### Frontend

Frontend, React ve Vite ile gelistirilmis kullanici arayuzudur.

Kullanicinin gordugu ana ekranlar:

- Landing page
- Urun analiz dashboard'u
- Demo urun secimi
- Trust Score karti
- Risk seviyesi rozeti
- Puan kirilimi
- Gemini guven raporu
- Kanit ve eksik veri kartlari

Kullanilan temel teknolojiler:

- React
- Vite
- Lucide React
- CSS tabanli ozel arayuz

### Backend

Backend, FastAPI tabanli analiz servisidir. Urun verisini alir, agent'lari calistirir, skor motorunu uygular ve frontend'e standart bir rapor doner.

Kullanilan temel teknolojiler:

- FastAPI
- Pydantic
- HTTPX
- Python rule engine
- Google Gemini entegrasyonu
- Trendyol ve Amazon scraper servisleri

## Analiz Akisi

1. Kullanici bir urun linki girer veya demo urun secer.
2. Backend URL'yi dogrular ve urun verisini cikarmaya calisir.
3. Desteklenen kaynaklarda canli scraping denenir.
4. Demo link veya fallback veri varsa kontrollu urun senaryosu kullanilir.
5. Urun verisi dort risk agent'ina gonderilir.
6. Agent'lar kendi risk skorlarini, reason code'larini ve kanitlarini uretir.
7. Rule Engine agent skorlarini agirlikli olarak birlestirir.
8. Score Fusion final `Trust Score` ve risk seviyesini olusturur.
9. Gemini Trust Orchestrator kanitlari kullanici dostu aciklamaya cevirir.
10. Frontend raporu skor, agent timeline, kanit ve eksik veri uyarilariyla gosterir.

## Risk Agent'lari

### Review Risk Agent

Yorumlar uzerinden sahte veya manipule edilmis yorum sinyallerini arar.

Kontrol ettigi sinyaller:

- Birbirine cok benzeyen yorumlar
- Cok kisa veya genel yorumlar
- Ayni gun yogun yorum patlamasi
- Urunle mantiksiz tekrar satin alma ifadeleri
- Yuksek yildiz puaniyla birlikte gelen manipulasyon sinyalleri

### Price Anomaly Agent

Fiyat ve indirim verisini analiz eder.

Kontrol ettigi sinyaller:

- Asiri yuksek indirim orani
- Gecmis ortalamaya gore sisirilmis orijinal fiyat
- Gercek fiyat dususu olmadan indirim gosterilmesi
- Fiyat gecmisi eksikligi

### Seller Risk Agent

Satici profiline gore risk uretir.

Kontrol ettigi sinyaller:

- Dusuk satici puani
- Dogrulanmamis satici
- Cok yeni satici hesabi
- Yuksek iade orani
- Eksik satici bilgisi

### Product Consistency Agent

Urun aciklamasi ile yorumlar arasindaki celiskileri inceler.

Kontrol ettigi sinyaller:

- "Su gecirmez" iddiasina karsi su gecirme sikayetleri
- "Orijinal" iddiasina karsi sahte/IMEI/garanti sikayetleri
- "Premium" iddiasina karsi kalite sikayetleri
- Aciklama verisinin eksikligi

## Gemini Trust Orchestrator

Gemini Trust Orchestrator final karari tek basina vermez. Karar temel olarak deterministic rule engine tarafindan uretilir.

Gemini'nin gorevi:

- Agent kanitlarini kullanici dostu dile cevirmek
- Yorum metinlerini ikinci bir goz olarak incelemek
- Riskleri kisa ve anlasilir sekilde ozetlemek
- Kullanicinin ne yapmasi gerektigini aciklamak

Gemini API anahtari yoksa sistem rule-based fallback aciklama uretir. Bu sayede uygulama Gemini olmadan da calismaya devam eder.

## Trust Score Hesaplama

Final guven skoru su mantikla uretilir:

```text
Trust Score = 100 - weighted risk - missing data penalty
```

Agent agirliklari:

| Agent | Agirlik |
| --- | ---: |
| Review Risk Agent | %35 |
| Price Anomaly Agent | %25 |
| Seller Risk Agent | %25 |
| Product Consistency Agent | %15 |

Risk seviyeleri:

| Trust Score | Risk Seviyesi | Anlam |
| ---: | --- | --- |
| 75-100 | Low | Genel olarak guvenilir |
| 50-74 | Medium | Dikkat edilmesi gereken orta risk |
| 30-49 | High | Belirgin risk sinyalleri var |
| 0-29 | Critical | Cok yuksek risk, uzak durulmasi onerilir |

## Demo Senaryolari

Proje icinde kontrollu demo urunleri bulunur. Bu urunler farkli risk davranislarini gostermek icin tasarlanmistir.

| Urun ID | Senaryo | Gosterilen Risk |
| --- | --- | --- |
| `p001` | Dusuk risk | Guvenilir urun davranisi |
| `p002` | Sahte yorum suphesi | Benzer ve genel yorum kaliplari |
| `p003` | Sahte indirim | Sisirilmis orijinal fiyat / indirim anomalisi |
| `p004` | Satici riski | Dusuk puanli, yeni veya dogrulanmamis satici |
| `p005` | Aciklama-yorum tutarsizligi | Urun iddiasi ile yorum sikayetleri arasinda celiski |
| `p006` | Coklu kritik risk | Yorum, fiyat, satici ve tutarlilik risklerinin birlesmesi |
| `p007` | Orta risk | Karisik yorumlar ve orta seviye satici/fiyat riski |
| `p008` | Sinirda risk | Ek inceleme gerektiren borderline urun |

Onerilen demo akisi:

1. `p001` ile sistemin her urunu riskli isaretlemedigi gosterilir.
2. `p002` ile sahte yorum analizi anlatilir.
3. `p003` ile fiyat anomalisi gosterilir.
4. `p004` ile satici riski vurgulanir.
5. `p005` ile aciklama-yorum celiskisi aciklanir.
6. `p006` ile tum risklerin birlestigi kritik senaryo sunulur.

## Proje Yapisi

```text
.
├── backend/
│   ├── agents/
│   │   ├── review_agent.py
│   │   ├── price_anomaly_agent.py
│   │   ├── seller_risk_agent.py
│   │   └── consistency_agent.py
│   ├── data/
│   │   ├── fallback_products.json
│   │   └── sample_links.json
│   ├── models/
│   │   ├── product_schema.py
│   │   ├── agent_schema.py
│   │   └── response_schema.py
│   ├── services/
│   │   ├── rule_engine.py
│   │   ├── score_fusion.py
│   │   ├── gemini_trust_orchestrator.py
│   │   ├── url_ingestion_service.py
│   │   └── scrapers/
│   ├── tests/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   └── styles/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── Fraud AI/
│   └── scenario_notes.md
└── README.md
```

## Gereksinimler

- Python 3.12+
- Node.js 18+
- npm
- Opsiyonel: Google Gemini API anahtari

Opsiyonel Gemini kullanimi icin backend tarafinda `.env` dosyasina su deger eklenebilir:

```env
GEMINI_API_KEY=your_api_key_here
```

Gemini anahtari yoksa uygulama rule-based aciklama moduyla calismaya devam eder.

## Backend Kurulumu ve Calistirma

Kok dizinden backend klasorune gecin:

```bash
cd backend
```

Sanal ortam olusturun:

```bash
python -m venv venv
```

Windows PowerShell icin sanal ortami aktif edin:

```bash
venv\Scripts\activate
```

Bagimliliklari yukleyin:

```bash
pip install -r requirements.txt
```

Backend API'yi calistirin:

```bash
uvicorn main:app --reload
```

Varsayilan backend adresi:

```text
http://127.0.0.1:8000
```

## Frontend Kurulumu ve Calistirma

Yeni bir terminalde frontend klasorune gecin:

```bash
cd frontend
```

Bagimliliklari yukleyin:

```bash
npm install
```

Frontend gelistirme sunucusunu baslatin:

```bash
npm run dev
```

Varsayilan frontend adresi:

```text
http://127.0.0.1:5173
```

Frontend API adresini varsayilan olarak `http://127.0.0.1:8000` kabul eder. Gerekirse `VITE_API_BASE_URL` ile degistirilebilir.

## API Endpointleri

### Health Check

```http
GET /health
```

Ornek cevap:

```json
{
  "status": "ok",
  "service": "FraudGuard AI Backend"
}
```

### Canli URL Analizi

```http
POST /analyze-url
```

Ornek istek:

```json
{
  "url": "https://www.trendyol.com/ornek-urun-p-123456"
}
```

Ornek cevap alanlari:

```json
{
  "source": "live_url",
  "extraction_status": "success",
  "trust_score": 72,
  "risk_level": "Medium",
  "reason_codes": ["HIGH_DISCOUNT"],
  "evidence": ["Yuksek indirim orani tespit edildi."],
  "agent_outputs": [],
  "gemini_used": true
}
```

### Demo Urun Analizi

```http
POST /analyze-demo/{product_id}
```

Ornek:

```http
POST /analyze-demo/p003
```

Bu endpoint kontrollu demo verisiyle analiz uretir ve sunum sirasinda stabil demo akisi saglar.

## Testler

Backend testleri kok dizinden su komutla calistirilabilir:

```bash
backend\venv\Scripts\python.exe -m pytest backend\tests
```

Mevcut test kapsami:

- Agent testleri
- Endpoint testleri
- Trendyol scraper parser testleri
- Fiyat ve yorum risk senaryolari

Frontend production build icin:

```bash
cd frontend
npm run build
```
