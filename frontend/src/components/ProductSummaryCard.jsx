import { BadgeCheck, Package, Store } from "lucide-react";
import { formatCurrency, formatPercent } from "../utils/formatters.js";

export default function ProductSummaryCard({ product, source, status }) {
  return (
    <section className="surface product-summary">
      <div className="section-title">
        <Package size={19} />
        <h2>{product.name}</h2>
      </div>
      <div style={{ display: "flex", gap: "1.5rem", alignItems: "flex-start", flexWrap: "wrap" }}>
        {product.image_url && (
          <div style={{ 
            flexShrink: 0, 
            width: "120px", 
            height: "160px", 
            borderRadius: "8px", 
            overflow: "hidden", 
            border: "1px solid var(--line)",
            backgroundColor: "#fff"
          }}>
            <img 
              src={product.image_url} 
              alt={product.name} 
              style={{ width: "100%", height: "100%", objectFit: "contain" }} 
            />
          </div>
        )}
        <dl className="summary-grid" style={{ flexGrow: 1, margin: 0 }}>
          <div>
            <dt>Kategori</dt>
            <dd>{product.category || "-"}</dd>
          </div>
          <div>
            <dt>Güncel fiyat</dt>
            <dd>{formatCurrency(product.current_price)}</dd>
          </div>
          <div>
            <dt>Eski fiyat</dt>
            <dd>{formatCurrency(product.original_price)}</dd>
          </div>
          <div>
            <dt>İndirim</dt>
            <dd>{formatPercent(product.discount_percentage)}</dd>
          </div>
          <div>
            <dt>Satıcı</dt>
            <dd className="with-icon">
              <Store size={15} />
              {product.seller?.name || "-"}
            </dd>
          </div>
          <div>
            <dt>Veri durumu</dt>
            <dd className="with-icon">
              <BadgeCheck size={15} />
              {source} / {status}
            </dd>
          </div>
        </dl>
      </div>
    </section>
  );
}

