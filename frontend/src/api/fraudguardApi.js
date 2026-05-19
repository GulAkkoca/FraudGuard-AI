const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(payload?.detail || "Analiz tamamlanamadi.");
  }

  return response.json();
}

export function analyzeUrl(url) {
  return request("/analyze-url", {
    method: "POST",
    body: JSON.stringify({ url }),
  });
}

export function analyzeDemo(productId) {
  return request(`/analyze-demo/${productId}`, {
    method: "POST",
  });
}

