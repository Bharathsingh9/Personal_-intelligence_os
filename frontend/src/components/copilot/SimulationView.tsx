import React from 'react';
import { ArrowRight, TrendingUp } from 'lucide-react';

export default function SimulationView() {
  return (
    <div className="glass-panel h-full flex flex-col justify-center">
      <div className="flex items-center space-x-2 border-b border-gray-800 pb-3 mb-4">
        <TrendingUp className="w-5 h-5 text-purple-400" />
        <h2 className="text-lg font-bold">Career Simulator</h2>
      </div>
      
      <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-800 mb-4">
        <h3 className="text-sm text-gray-400 mb-4 text-center">Scenario: Add "LangGraph" & "Agentic AI"</h3>
        <div className="flex items-center justify-between">
          <div className="text-center">
            <p className="text-xs text-gray-500 mb-1">Current</p>
            <p className="text-4xl font-bold text-gray-300">66.0%</p>
          </div>
          <ArrowRight className="w-8 h-8 text-brand-500 animate-pulse" />
          <div className="text-center">
            <p className="text-xs text-gray-500 mb-1">Predicted</p>
            <p className="text-4xl font-bold text-green-400">79.5%</p>
          </div>
        </div>
        
        <div className="mt-6 flex justify-center">
          <div className="bg-green-900/20 px-4 py-2 rounded-lg border border-green-500/20 text-center inline-block">
            <p className="text-xs text-green-500 mb-1">Impact</p>
            <p className="text-xl font-bold text-green-400">+13.5%</p>
          </div>
        </div>
      </div>
      <p className="text-xs text-gray-500 italic text-center">Confidence Score: 85% based on target role requirements.</p>
    </div>
  );
}
