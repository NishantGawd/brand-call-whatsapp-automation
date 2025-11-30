// src/layouts/DashboardLayout.tsx
import React from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const navLinkBase =
  "flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-medium transition-colors";
const navLinkInactive =
  "text-slate-400 hover:text-slate-100 hover:bg-slate-800/70";
const navLinkActive =
  "text-emerald-300 bg-slate-900 border border-emerald-500/40 shadow-sm shadow-emerald-500/20";

const DashboardLayout: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  const tenantId = user?.tenant_id ?? user?.tenant_id ?? undefined;

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_#0f172a,_#020617)] text-slate-100">
      <div className="flex min-h-screen">
        {/* Sidebar */}
        <aside className="hidden md:flex w-64 flex-col border-r border-slate-800/80 bg-slate-950/80 backdrop-blur">
          <div className="px-5 pt-5 pb-4 border-b border-slate-800/80">
            <div className="inline-flex items-center gap-2 rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
              <span className="text-lg">📞</span>
              <span>Dealer WhatsApp</span>
            </div>
            <h1 className="mt-4 text-xl font-semibold tracking-tight">
              Automation Console
            </h1>
            <p className="mt-1 text-xs text-slate-400">
              Monitor calls, catalog and WhatsApp follow-ups.
            </p>
          </div>

          <nav className="flex-1 px-3 py-4 space-y-1">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                `${navLinkBase} ${isActive ? navLinkActive : navLinkInactive}`
              }
            >
              <span className="text-lg">📊</span>
              <span>Dashboard</span>
            </NavLink>

            <NavLink
              to="/calls"
              className={({ isActive }) =>
                `${navLinkBase} ${isActive ? navLinkActive : navLinkInactive}`
              }
            >
              <span className="text-lg">📞</span>
              <span>Calls</span>
            </NavLink>

            <NavLink
              to="/products"
              className={({ isActive }) =>
                `${navLinkBase} ${isActive ? navLinkActive : navLinkInactive}`
              }
            >
              <span className="text-lg">🛒</span>
              <span>Catalog</span>
            </NavLink>

            <NavLink
              to="/settings/automation"
              className={({ isActive }) =>
                `${navLinkBase} ${isActive ? navLinkActive : navLinkInactive}`
              }
            >
              <span className="text-lg">⚙️</span>
              <span>Automation</span>
            </NavLink>

            <NavLink
              to="/settings/whatsapp"
              className={({ isActive }) =>
                `${navLinkBase} ${isActive ? navLinkActive : navLinkInactive}`
              }
            >
              <span className="text-lg">💬</span>
              <span>WhatsApp</span>
            </NavLink>
          </nav>

          <div className="border-t border-slate-800/80 px-4 py-4 text-xs text-slate-400">
            <div className="mb-2">
              <p className="font-medium text-slate-200">
                {user?.email ?? "Owner"}
              </p>
              {tenantId && (
                <p className="text-slate-500">Tenant ID: {tenantId}</p>
              )}
            </div>
            <button
              onClick={handleLogout}
              className="inline-flex items-center gap-2 text-xs font-medium text-rose-300 hover:text-rose-200"
            >
              <span>🔒</span>
              <span>Log out</span>
            </button>
            <p className="mt-3 text-[11px] text-slate-500">
              © {new Date().getFullYear()} Brand Call Automation · Demo UI
            </p>
          </div>
        </aside>

        {/* Main content */}
        <div className="flex-1 flex flex-col">
          {/* Top bar (for mobile + title) */}
          <header className="flex items-center justify-between border-b border-slate-800/80 bg-slate-950/80 px-4 py-3 md:px-6 backdrop-blur">
            <div className="flex items-center gap-3">
              <div className="inline-flex items-center gap-2 rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300 md:hidden">
                <span className="text-lg">📞</span>
                <span>Dealer WhatsApp</span>
              </div>
              <h2 className="text-sm font-medium text-slate-300">
                Dealer WhatsApp Automation
              </h2>
            </div>

            <div className="flex items-center gap-3 text-xs">
              <div className="hidden sm:flex flex-col items-end">
                <span className="font-medium text-slate-200">
                  {user?.email ?? "owner@gmail.com"}
                </span>
                {tenantId && (
                  <span className="text-slate-500">Tenant {tenantId}</span>
                )}
              </div>
              <button
                onClick={handleLogout}
                className="inline-flex items-center gap-1 rounded-full bg-slate-900 px-3 py-1 text-xs font-medium text-slate-200 border border-slate-700 hover:border-rose-400 hover:text-rose-200 transition"
              >
                <span>🔒</span>
                <span>Logout</span>
              </button>
            </div>
          </header>

          {/* Page content */}
          <main className="flex-1 overflow-y-auto bg-gradient-to-b from-slate-950 via-slate-950 to-slate-950/95">
            <div className="mx-auto max-w-6xl px-4 py-6 md:px-8 md:py-8">
              <Outlet />
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;
