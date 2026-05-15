# FraudGuard AI Backend

FastAPI tabanli FraudGuard AI MVP backend mimarisi.

## SRS kapsamindan gelen ana moduller

- URL ingestion: demo link mapping, opsiyonel canli extraction, fallback data
- Gemini Product Extractor: ham metinden standart urun semasi
- Risk agents: review, price anomaly, seller risk, product consistency
- Rule Engine: agent risk skorlarini agirlikli birlestirme
- Gemini Trust Orchestrator: evidence tabanli kullanici aciklamasi
- Score Fusion: rule score + Gemini score ile final Trust Score

## Calistirma

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpointler

- `GET /health`
- `POST /analyze-url`
- `POST /analyze-demo/{product_id}`

