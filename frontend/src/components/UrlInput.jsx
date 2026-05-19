import { Link, Search } from "lucide-react";

export default function UrlInput({ url, onUrlChange, onSubmit, loading }) {
  return (
    <form className="url-form" onSubmit={onSubmit}>
      <label htmlFor="product-url">Ürün linki</label>
      <div className="input-row">
        <Link aria-hidden="true" size={18} />
        <input
          id="product-url"
          value={url}
          onChange={(event) => onUrlChange(event.target.value)}
          placeholder="Ürün linkini buraya yapıştırın..."
        />
        <button type="submit" disabled={loading} title="Analiz Et">
          <Search aria-hidden="true" size={18} />
          <span>Analiz Et</span>
        </button>
      </div>
    </form>
  );
}

