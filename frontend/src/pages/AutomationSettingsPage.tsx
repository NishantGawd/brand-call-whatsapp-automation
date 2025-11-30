// src/pages/AutomationSettingsPage.tsx
import React, { useEffect, useState } from "react";
import {
  getAutomationSettings,
  updateAutomationSettings,
  type AutomationSettings,
} from "../api/automationSettings";

const AutomationSettingsPage: React.FC = () => {
  const [settings, setSettings] = useState<AutomationSettings | null>(null);
  const [enabled, setEnabled] = useState<boolean>(true);
  const [minDuration, setMinDuration] = useState<number>(10);
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getAutomationSettings();
        setSettings(data);
        setEnabled(Boolean(data.enabled));
        setMinDuration(Number(data.min_call_duration_seconds ?? 10) || 10);
      } catch (err) {
        console.error(err);
        setError("Failed to load automation settings.");
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    setError(null);
    try {
      const updated = await updateAutomationSettings({
        enabled,
        min_call_duration_seconds: minDuration,
      });
      setSettings(updated);
      setMessage("Settings saved successfully.");
    } catch (err) {
      console.error(err);
      setError("Failed to save settings. Try again.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-4">
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold tracking-tight">
          Automation settings
        </h1>
        <p className="text-sm text-slate-400">
          Control when WhatsApp follow-up messages are sent after a call.
        </p>
      </header>

      <section className="app-card p-4 md:p-5 max-w-xl">
        {loading && <p className="text-sm text-slate-400">Loading settings…</p>}
        {error && <p className="mb-3 text-sm text-rose-300">{error}</p>}
        {message && <p className="mb-3 text-sm text-emerald-300">{message}</p>}

        {!loading && (
          <form className="space-y-5" onSubmit={handleSave}>
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-medium text-slate-200">
                  Enable automation
                </p>
                <p className="text-xs text-slate-400">
                  Turn this off to pause WhatsApp messages for all calls.
                </p>
              </div>
              <button
                type="button"
                onClick={() => setEnabled((v) => !v)}
                className={`inline-flex h-8 w-14 items-center rounded-full border px-1 transition ${
                  enabled
                    ? "border-emerald-500/60 bg-emerald-500/20"
                    : "border-slate-600 bg-slate-800/80"
                }`}
              >
                <span
                  className={`h-6 w-6 rounded-full bg-white shadow transform transition ${
                    enabled ? "translate-x-6" : "translate-x-0"
                  }`}
                />
              </button>
            </div>

            <div className="space-y-2">
              <label
                htmlFor="min-duration"
                className="block text-sm font-medium text-slate-200"
              >
                Minimum call duration (seconds)
              </label>
              <input
                id="min-duration"
                type="number"
                min={0}
                value={minDuration}
                onChange={(e) => setMinDuration(Number(e.target.value) || 0)}
                className="w-full rounded-xl border border-slate-700 bg-slate-900/70 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              />
              <p className="text-xs text-slate-400">
                Only calls with duration greater than or equal to this value
                will trigger WhatsApp automation.
              </p>
            </div>

            <button
              type="submit"
              disabled={saving}
              className="inline-flex items-center rounded-xl bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 shadow-md shadow-emerald-500/30 hover:bg-emerald-400 disabled:opacity-60 disabled:cursor-not-allowed transition"
            >
              {saving ? "Saving…" : "Save changes"}
            </button>

            {settings && (
              <p className="text-[11px] text-slate-500 mt-2">
                Last loaded value: min {settings.min_call_duration_seconds ?? 0}
                s · enabled {String(settings.enabled ?? false)}.
              </p>
            )}
          </form>
        )}
      </section>
    </div>
  );
};

export default AutomationSettingsPage;
