import json
import os
import google.generativeai as genai
from models.agent_schema import AgentOutput
from models.product_schema import Product
from models.response_schema import GeminiExplanation


def build_trust_explanation(product: Product, agent_outputs: list[AgentOutput]) -> GeminiExplanation:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return _fallback_explanation()

    genai.configure(api_key=api_key)
    
    # Kural motorundan gelen riski de Gemini'ye bildirelim
    from services.rule_engine import calculate_rule_risk
    rule_risk = calculate_rule_risk(agent_outputs)
    
    missing_fields = sorted(list(set(field for output in agent_outputs for field in output.missing_fields)))
    reason_codes = sorted(list(set(code for output in agent_outputs for code in output.reason_codes)))
    evidence = [item for output in agent_outputs for item in output.evidence]

    prompt = f"""Sen FraudGuard AI için Gemini Trust Orchestrator'sın.
Sadece verilen kanıtlara dayan.
Yeni bilgi uydurma.
Eksik verileri açıkça belirt.
Cevabı aşağıdaki JSON formatında döndür.
Dil Türkçe olsun.

JSON Formatı:
{{
  "gemini_risk": 74,
  "summary": "kısa özet",
  "user_friendly_explanation": "kullanıcı dostu detaylı açıklama",
  "key_concerns": ["risk 1", "risk 2"],
  "recommended_action": "önerilen aksiyon",
  "confidence": 86
}}

VERİLER:
Ürün Adı: {product.name}
Kategori: {product.category}
Fiyat: {product.current_price}
Rule Risk Puanı: {rule_risk}
Eksik Veriler: {missing_fields}
Hata Kodları (Reason Codes): {reason_codes}
Kanıtlar (Evidence): {evidence}
"""

    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(response_mime_type="application/json")
        )
        data = json.loads(response.text)
        
        return GeminiExplanation(
            summary=data.get("summary", "Özet alınamadı."),
            user_friendly_explanation=data.get("user_friendly_explanation", "Açıklama alınamadı."),
            key_concerns=data.get("key_concerns", []),
            recommended_action=data.get("recommended_action", "Dikkatli inceleyin."),
            confidence=data.get("confidence"),
            gemini_risk=data.get("gemini_risk")
        )
    except Exception as e:
        print(f"Gemini API Hatası: {e}")
        return _fallback_explanation()


def _fallback_explanation() -> GeminiExplanation:
    return GeminiExplanation(
        summary="Gemini açıklaması alınamadı.",
        user_friendly_explanation="Sistem rule-based analiz sonucunu göstermektedir.",
        key_concerns=[],
        recommended_action="Kanıt kartlarını inceleyin.",
        confidence=None,
        gemini_risk=None,
    )

