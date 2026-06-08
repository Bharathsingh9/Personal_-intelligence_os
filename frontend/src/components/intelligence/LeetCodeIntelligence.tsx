import React from 'react';
import { Terminal, Target, Brain } from 'lucide-react';

export default function LeetCodeIntelligence() {
  const data = {
    readiness_score: 82,
    dsa_strength_level: "Advanced",
    difficulty_distribution: { Easy: 120, Medium: 180, Hard: 35 },
    topic_mastery: {
      Strong: ["Arrays", "Dynamic Programming", "Sliding Window"],
      Weak: ["Graphs", "Segment Trees"]
    }
  };

  return (
    <div className="glass-panel hover:border-brand-500/30 transition-colors">
      <div className="flex items-center space-x-3 mb-4 border-b border-gray-800 pb-4">
        <Terminal className="w-6 h-6 text-brand-400" />
        <h2 className="text-xl font-semibold">LeetCode Intelligence</h2>
      </div>
      
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-800">
          <p className="text-sm text-gray-400">Problem Solving Score</p>
          <p className="text-3xl font-bold text-brand-400">{data.readiness_score}<span className="text-sm text-gray-500">/100</span></p>
        </div>
        <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-800">
          <p className="text-sm text-gray-400">DSA Level</p>
          <div className="flex items-center space-x-2 mt-1">
            <Target className="w-4 h-4 text-purple-400" />
            <p className="font-medium text-purple-400">{data.dsa_strength_level}</p>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <h3 className="text-sm text-gray-400 mb-2">Solved Problems</h3>
        <div className="flex space-x-4">
          <div className="text-center"><p className="text-lg font-bold text-green-400">{data.difficulty_distribution.Easy}</p><p className="text-xs text-gray-500">Easy</p></div>
          <div className="text-center"><p className="text-lg font-bold text-yellow-400">{data.difficulty_distribution.Medium}</p><p className="text-xs text-gray-500">Medium</p></div>
          <div className="text-center"><p className="text-lg font-bold text-red-400">{data.difficulty_distribution.Hard}</p><p className="text-xs text-gray-500">Hard</p></div>
        </div>
      </div>
      
      <div>
        <h3 className="text-sm text-gray-400 mb-2">Topic Mastery</h3>
        <div className="space-y-2">
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-green-500 font-medium">Strong:</span>
            {data.topic_mastery.Strong.map(s => (
              <span key={s} className="px-2 py-0.5 text-xs bg-gray-800 text-gray-300 rounded border border-gray-700">{s}</span>
            ))}
          </div>
          <div className="flex flex-wrap gap-2 mt-1">
            <span className="text-xs text-red-500 font-medium">Weak:</span>
            {data.topic_mastery.Weak.map(s => (
              <span key={s} className="px-2 py-0.5 text-xs bg-gray-800 text-gray-300 rounded border border-gray-700">{s}</span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
