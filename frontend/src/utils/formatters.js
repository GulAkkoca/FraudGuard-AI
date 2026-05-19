export function formatCurrency(value) {
  if (value === null || value === undefined) return "-";
  return new Intl.NumberFormat("tr-TR", {
    style: "currency",
    currency: "TRY",
    maximumFractionDigits: 0,
  }).format(value);
}

export function formatPercent(value) {
  if (value === null || value === undefined) return "-";
  return `%${Math.round(value)}`;
}

