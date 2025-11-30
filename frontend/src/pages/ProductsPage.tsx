// src/pages/ProductsPage.tsx
import React, { useEffect, useState } from "react";
import { listProducts, type Product } from "../api/products";

const ProductsPage: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await listProducts();
        setProducts(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load products. Try again.");
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, []);

  return (
    <div className="space-y-4">
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold tracking-tight">
          Catalog / products
        </h1>
        <p className="text-sm text-slate-400">
          This is the dealer inventory that gets promoted after calls. In later
          phases we’ll add CSV bulk upload and richer management tools.
        </p>
      </header>

      <section className="app-card p-4 md:p-5">
        {loading && <p className="text-sm text-slate-400">Loading products…</p>}
        {error && <p className="text-sm text-rose-300 mb-2">{error}</p>}
        {!loading && !error && products.length === 0 && (
          <p className="text-sm text-slate-400">
            No products yet. Use the backend product endpoints or a future CSV
            upload to add inventory.
          </p>
        )}

        {!loading && !error && products.length > 0 && (
          <div className="overflow-x-auto">
            <table className="app-table">
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Category</th>
                  <th>Tags</th>
                  <th className="text-right">Price</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {products.map((p) => (
                  <tr key={p.id}>
                    <td className="text-sm text-slate-100">
                      <div className="flex flex-col">
                        <span>{p.name}</span>
                        {p.description && (
                          <span className="text-xs text-slate-400 line-clamp-2">
                            {p.description}
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="text-xs text-slate-300">
                      {p.category ?? "—"}
                    </td>
                    <td className="text-xs text-slate-400">{p.tags ?? "—"}</td>
                    <td className="text-xs text-right text-slate-100 whitespace-nowrap">
                      {typeof p.price === "number"
                        ? `₹${p.price.toFixed(2)}`
                        : p.price
                        ? `₹${Number(p.price).toFixed(2)}`
                        : "—"}
                    </td>
                    <td className="text-xs">
                      {p.is_active ? (
                        <span className="inline-flex items-center rounded-full bg-emerald-500/10 px-2 py-0.5 text-[11px] font-medium text-emerald-300 border border-emerald-500/40">
                          Active
                        </span>
                      ) : (
                        <span className="inline-flex items-center rounded-full bg-slate-800/80 px-2 py-0.5 text-[11px] font-medium text-slate-300 border border-slate-700/80">
                          Inactive
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
};

export default ProductsPage;
