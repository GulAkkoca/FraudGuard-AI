import { LineChart } from "lucide-react";
import { formatCurrency } from "../utils/formatters.js";

export default function PriceAnalysisCard({ product }) {
  const history = product.price_history || [];
  const prices = history.map((item) => item.price);
  const maxPrice = Math.max(...prices, product.original_price || 0, product.current_price || 0, 1);

  return (
    <section className="surface price-card">
      <div className="section-title">
        <LineChart size={19} />
        <h2>Fiyat Analizi</h2>
      </div>
      <div className="price-bars">
        {history.length ? (
          history.map((item, index) => (
            <div key={`${item.price}-${index}`}>
              <span style={{ height: `${Math.max((item.price / maxPrice) * 100, 8)}%` }} />
              <small>{formatCurrency(item.price)}</small>
            </div>
          ))
        ) : (
          <p>Fiyat geçmişi yok.</p>
        )}
      </div>
    </section>
  );
}

