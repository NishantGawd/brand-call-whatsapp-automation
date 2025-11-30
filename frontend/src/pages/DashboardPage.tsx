// src/pages/DashboardPage.tsx
import React from "react";
import { useAuth } from "../context/AuthContext";

const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const tenantId = user?.tenant_id ?? user?.tenant_id ?? "—";

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">
          Welcome back,{" "}
          <span className="text-emerald-300">
            {user?.email ?? "Dealer owner"}
          </span>
        </h1>
        <p className="text-sm text-slate-400">
          Tenant ID <span className="font-mono text-slate-200">{tenantId}</span>{" "}
          · This overview will grow as we add analytics in later phases.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <section className="app-card p-4 md:p-5">
          <h2 className="text-sm font-semibold text-slate-200 mb-2">
            Calls & automations
          </h2>
          <p className="text-xs text-slate-400 mb-3">
            Check recent calls received from your webhook integration and see
            which ones triggered WhatsApp automation.
          </p>
          <ul className="space-y-1 text-xs text-slate-300">
            <li>• See inbound calls from Phase 3.x webhook.</li>
            <li>• Filter by status and duration.</li>
            <li>• Verify which calls queued WhatsApp messages.</li>
          </ul>
        </section>

        <section className="app-card p-4 md:p-5">
          <h2 className="text-sm font-semibold text-slate-200 mb-2">
            Product catalog
          </h2>
          <p className="text-xs text-slate-400 mb-3">
            Manage the inventory that will be recommended after calls.
          </p>
          <ul className="space-y-1 text-xs text-slate-300">
            <li>• Browse the products for this tenant.</li>
            <li>• Future: CSV bulk upload for large catalogs.</li>
            <li>• Used by the WhatsApp follow-up message.</li>
          </ul>
        </section>

        <section className="app-card p-4 md:p-5">
          <h2 className="text-sm font-semibold text-slate-200 mb-2">
            Automation controls
          </h2>
          <p className="text-xs text-slate-400 mb-3">
            Fine-tune when WhatsApp should be sent after a call.
          </p>
          <ul className="space-y-1 text-xs text-slate-300">
            <li>• Enable/disable automation per tenant.</li>
            <li>• Set minimum call duration threshold.</li>
            <li>• Configure WhatsApp credentials from your .env.</li>
          </ul>
        </section>
      </div>
    </div>
  );
};

export default DashboardPage;
