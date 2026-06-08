import React from 'react';
import { BrainCircuit } from 'lucide-react';
import CopilotChat from '../components/copilot/CopilotChat';
import RoadmapView from '../components/copilot/RoadmapView';
import SimulationView from '../components/copilot/SimulationView';

export default function CopilotHub() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <header className="mb-10 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-brand-400 to-brand-600">
            AI Career Copilot
          </h1>
          <p className="text-gray-400 mt-2">Multi-Agent Intelligence for Roadmaps, Projects, and Simulations.</p>
        </div>
        <div className="flex items-center space-x-2 bg-brand-900/20 px-4 py-2 rounded-full border border-brand-500/20">
          <BrainCircuit className="w-5 h-5 text-brand-400 animate-pulse" />
          <span className="text-sm font-medium text-brand-300">Agents Online</span>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Chat Copilot */}
        <div className="lg:col-span-1">
          <CopilotChat />
        </div>
        
        {/* Right Column: Dynamic Outputs */}
        <div className="lg:col-span-2 space-y-8">
          <div className="grid grid-cols-1 gap-8">
            <SimulationView />
          </div>
          
          <div className="grid grid-cols-1 gap-8">
            <RoadmapView />
          </div>
        </div>
      </div>
    </div>
  );
}
