import React from "react";

const OverviewPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold text-white">Overview</h2>

      <p className="text-sm text-slate-300">
        This dashboard will eventually show key metrics like:
      </p>

      <ul className="list-disc space-y-1 pl-6 text-sm text-slate-300">
        <li>Total calls received.</li>
        <li>How many WhatsApp messages were triggered.</li>
        <li>Top-performing products (for future AI recommendations).</li>
      </ul>

      <p className="mt-4 text-xs text-slate-500">
        Right now this is just a placeholder. In later phases we will connect
        this to real analytics and AI-based recommendations.
      </p>
    </div>
  );
};

export default OverviewPage;
