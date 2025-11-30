// src/components/LoadingState.tsx
import React from "react";
import type { ReactNode } from "react";

interface LoadingStateProps {
  isLoading: boolean;
  error?: string | null;
  children: ReactNode;
}

const LoadingState: React.FC<LoadingStateProps> = ({
  isLoading,
  error,
  children,
}) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12 text-slate-400">
        <div className="h-5 w-5 mr-3 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
        <span>Loading…</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-red-500/60 bg-red-950/40 px-4 py-3 text-sm text-red-200">
        {error}
      </div>
    );
  }

  return <>{children}</>;
};

export default LoadingState;
