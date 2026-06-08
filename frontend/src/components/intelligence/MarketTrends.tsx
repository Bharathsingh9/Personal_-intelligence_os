import React from 'react';
import { TrendingUp, Briefcase } from 'lucide-react';

export default function MarketTrends() {
  const trendsData = [
    { skill_name: "Agentic AI", target_role: "GenAI Engineer", weekly_growth: 230.5 },
    { skill_name: "Graph RAG", target_role: "GenAI Engineer", weekly_growth: 175.2 },
    { skill_name: "LangGraph", target_role: "AI Engineer", weekly_growth: 45.0 },
    { skill_name: "MLOps", target_role: "MLOps Engineer", weekly_growth: 15.0 },
  ];

  return (
    <div className="glass-panel col-span-full mt-8">
      <div className="flex items-center justify-between mb-6 border-b border-gray-800 pb-4">
        <div className="flex items-center space-x-3">
          <Briefcase className="w-6 h-6 text-brand-400" />
          <h2 className="text-xl font-semibold">Labor Market Intelligence</h2>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-400">
          <TrendingUp className="w-4 h-4 text-green-400" />
          <span>Real-time ETL active</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {trendsData.map((trend, idx) => (
          <div key={idx} className="bg-gray-900/50 p-4 rounded-xl border border-gray-800 relative overflow-hidden group hover:border-brand-500/50 transition-colors">
            <div className="absolute top-0 right-0 bg-green-500/10 text-green-400 px-3 py-1 rounded-bl-lg font-semibold text-sm">
              +{trend.weekly_growth}%
            </div>
            <h3 className="font-bold text-lg mt-2 text-gray-200">{trend.skill_name}</h3>
            <p className="text-sm text-brand-400/80 mt-1">{trend.target_role}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
