import React from 'react';
import { Map } from 'lucide-react';

export default function RoadmapView() {
  const weeks = [
    { week: 1, topic: "Vector Databases", desc: "Learn ChromaDB and Pinecone integrations." },
    { week: 2, topic: "RAG Systems", desc: "Build a document retrieval chain." },
    { week: 3, topic: "LangGraph", desc: "Create a stateful multi-agent flow." },
    { week: 4, topic: "Agentic AI", desc: "Build a final AI Copilot project." },
  ];

  return (
    <div className="glass-panel">
      <div className="flex items-center space-x-2 border-b border-gray-800 pb-3 mb-4">
        <Map className="w-5 h-5 text-blue-400" />
        <h2 className="text-lg font-bold">30-Day Learning Roadmap</h2>
      </div>
      
      <div className="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-gray-700 before:to-transparent">
        {weeks.map((w, i) => (
          <div key={i} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
            <div className="flex items-center justify-center w-10 h-10 rounded-full border border-gray-700 bg-gray-900 text-brand-400 font-bold shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-[0_0_10px_rgba(20,184,166,0.2)]">
              W{w.week}
            </div>
            
            <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border border-gray-800 bg-gray-900/50 hover:border-brand-500/30 transition-colors">
              <h3 className="font-bold text-gray-200 mb-1">{w.topic}</h3>
              <p className="text-sm text-gray-400">{w.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
