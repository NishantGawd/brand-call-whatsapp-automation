// src/pages/WhatsAppSettingsPage.tsx
import React from "react";

const WhatsAppSettingsPage: React.FC = () => {
  return (
    <div className="space-y-4">
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold tracking-tight">
          WhatsApp settings
        </h1>
        <p className="text-sm text-slate-400">
          In later phases we’ll add UI to manage WhatsApp templates, phone
          numbers and access tokens. For now these values are read from your
          backend <code>.env</code>.
        </p>
      </header>

      <section className="app-card p-4 md:p-6 max-w-2xl text-sm">
        <p className="text-slate-300 mb-3">
          To fully enable sending messages, configure these environment
          variables on the backend:
        </p>

        <ul className="space-y-1 font-mono text-xs bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3">
          <li>WHATSAPP_PHONE_NUMBER_ID</li>
          <li>WHATSAPP_ACCESS_TOKEN</li>
          <li>WHATSAPP_API_BASE_URL (optional, defaults to Meta API)</li>
        </ul>

        <p className="mt-4 text-sm text-slate-400">
          Once configured, the test endpoint{" "}
          <code className="font-mono text-slate-200">
            /api/v1/whatsapp-test/test
          </code>{" "}
          (Phase 3.2/3.3) will start sending real messages instead of logging
          warnings.
        </p>

        <p className="mt-4 text-xs text-slate-500">
          In a future phase we’ll add:
        </p>
        <ul className="mt-1 text-xs text-slate-400 list-disc list-inside space-y-1">
          <li>Multiple WhatsApp templates per tenant.</li>
          <li>Test-send UI from the dashboard.</li>
          <li>Per-tenant access token and phone number management.</li>
        </ul>
      </section>
    </div>
  );
};

export default WhatsAppSettingsPage;
