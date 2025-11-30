// src/pages/LoginPage.tsx
import React, { useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const LoginPage: React.FC = () => {
  const { login, token, user, isLoading } = useAuth();

  const [email, setEmail] = useState("owner@gmail.com");
  const [password, setPassword] = useState("demo-password");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (token && user) {
    return <Navigate to="/" replace />;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await login(email, password);
    } catch (err) {
      console.error("Login failed:", err);
      setError("Invalid email or password. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[radial-gradient(circle_at_top,_#0f172a,_#020617)] px-4">
      <div className="w-full max-w-md app-card px-8 py-10">
        <div className="mb-6">
          <div className="inline-flex items-center gap-2 rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-300">
            <span className="text-lg">📞</span>
            <span>Dealer WhatsApp</span>
          </div>
          <h1 className="mt-4 text-2xl font-semibold tracking-tight text-white">
            WhatsApp Automation Dashboard
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Sign in with your demo owner account to continue.
          </p>
        </div>

        {error && (
          <div className="mb-4 rounded-xl bg-rose-500/10 border border-rose-500/40 px-3 py-2 text-sm text-rose-200">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label
              htmlFor="email"
              className="block text-xs font-medium text-slate-300 mb-1.5"
            >
              Email address
            </label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-900/70 px-3 py-2.5 text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              placeholder="owner@gmail.com"
              required
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-xs font-medium text-slate-300 mb-1.5"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-xl border border-slate-700 bg-slate-900/70 px-3 py-2.5 text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
              placeholder="demo-password"
              required
            />
          </div>

          <button
            type="submit"
            disabled={submitting || isLoading}
            className="w-full inline-flex items-center justify-center rounded-xl bg-emerald-500 px-4 py-2.5 text-sm font-semibold text-slate-950 shadow-lg shadow-emerald-500/30 hover:bg-emerald-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 focus:ring-offset-slate-950 disabled:opacity-60 disabled:cursor-not-allowed transition"
          >
            {submitting || isLoading ? "Signing in..." : "Sign in"}
          </button>

          <p className="text-xs text-slate-500 text-center mt-2">
            Demo credentials:{" "}
            <span className="font-mono text-slate-300">owner@gmail.com</span> /{" "}
            <span className="font-mono text-slate-300">demo-password</span>
          </p>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
