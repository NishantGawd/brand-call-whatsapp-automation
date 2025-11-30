// src/pages/CallsPage.tsx
import React, { useEffect, useState } from "react";
import { listCalls, type Call } from "../api/calls";

const statusBadgeClasses: Record<string, string> = {
  completed: "bg-emerald-500/15 text-emerald-300 border-emerald-500/40",
  answered: "bg-emerald-500/15 text-emerald-300 border-emerald-500/40",
  failed: "bg-rose-500/10 text-rose-300 border-rose-500/40",
  ringing: "bg-amber-500/10 text-amber-300 border-amber-500/40",
};

const CallsPage: React.FC = () => {
  const [calls, setCalls] = useState<Call[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await listCalls();
        setCalls(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load calls. Try again.");
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, []);

  return (
    <div className="space-y-4">
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold tracking-tight">Recent calls</h1>
        <p className="text-sm text-slate-400">
          These records come from your webhook endpoint in Phase 3.x. You can
          verify which calls triggered WhatsApp automation.
        </p>
      </header>

      <section className="app-card p-4 md:p-5">
        {loading && <p className="text-sm text-slate-400">Loading calls…</p>}
        {error && <p className="text-sm text-rose-300 mb-2">{error}</p>}
        {!loading && !error && calls.length === 0 && (
          <p className="text-sm text-slate-400">
            No calls yet. Trigger the webhook endpoint and refresh.
          </p>
        )}

        {!loading && !error && calls.length > 0 && (
          <div className="overflow-x-auto">
            <table className="app-table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>From</th>
                  <th>To</th>
                  <th>Status</th>
                  <th>Duration</th>
                  <th>Automation</th>
                </tr>
              </thead>
              <tbody>
                {calls.map((call) => {
                  const status = call.call_status?.toLowerCase() ?? "";
                  const badge = statusBadgeClasses[status] ?? "bg-slate-800/80";
                  return (
                    <tr key={call.id}>
                      <td className="text-xs text-slate-300 whitespace-nowrap">
                        {call.created_at
                          ? new Date(call.created_at).toLocaleString()
                          : "—"}
                      </td>
                      <td className="text-xs text-slate-200">
                        {call.caller_number ?? "—"}
                      </td>
                      <td className="text-xs text-slate-200">
                        {call.receiver_number ?? "—"}
                      </td>
                      <td className="text-xs">
                        <span
                          className={`inline-flex items-center rounded-full border px-2 py-0.5 text-[11px] font-medium ${badge}`}
                        >
                          {call.call_status ?? "unknown"}
                        </span>
                      </td>
                      <td className="text-xs text-slate-300">
                        {call.call_duration_seconds ?? 0}s
                      </td>
                      <td className="text-xs">
                        {call.should_trigger_automation ? (
                          <span className="inline-flex items-center rounded-full bg-emerald-500/10 px-2 py-0.5 text-[11px] font-medium text-emerald-300 border border-emerald-500/40">
                            ✅ WhatsApp queued
                          </span>
                        ) : (
                          <span className="inline-flex items-center rounded-full bg-slate-800/80 px-2 py-0.5 text-[11px] font-medium text-slate-300 border border-slate-700/80">
                            — Not triggered
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
};

export default CallsPage;
