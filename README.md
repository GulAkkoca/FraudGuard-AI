# FraudGuard AI

## Problem
Online alışverişte kullanıcılar sahte yorum, şüpheli indirim ve satıcı güveni konusunda karar vermekte zorlanır.

## Solution
FraudGuard AI ürün linki üzerinden çoklu güven sinyallerini analiz eder ve açıklanabilir Trust Score üretir.

## Core Features
- Link-based product analysis
- Review risk analysis
- Price / discount anomaly analysis
- Seller risk analysis
- Product consistency analysis
- Gemini Trust Orchestrator
- Evidence-based trust report

## Tech Stack
- **Backend:** FastAPI, Python
- **Frontend:** React + Vite + Tailwind
- **AI:** Gemini API (Google Generative AI)
- **Data:** JSON fallback dataset

## How to Run

**Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Demo Links
- https://demo.fraudguard.ai/smart-watch
- https://demo.fraudguard.ai/earbuds
- https://demo.fraudguard.ai/perfume

## Limitations
- Live extraction is experimental.
- MVP uses controlled demo mapping (fallback_products.json).
- The system does not claim definitive fraud, it reports trust signals.
