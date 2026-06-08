import React, { useState, useEffect } from 'react';
import { Github, Activity, Code, Loader2 } from 'lucide-react';

export default function GitHubIntelligence() {
  const [data, setData] = useState({
    developer_score: 85,
    tech_stack_detected: ["Python", "FastAPI", "React", "TypeScript", "Machine Learning"],
    strengths: ["Python", "Backend Development", "Machine Learning"],
    improvement_areas: ["Docker", "CI/CD", "Cloud Deployment"],
    activity_metrics: { total_repos: 12, estimated_commits: 600 }
  });
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchGitHubData = async () => {
      setIsLoading(true);
      try {
        const userId = 1;
        const res = await fetch(`http://localhost:8000/api/v1/intelligence/github/${userId}`, { method: 'POST' });
        if (res.ok) {
          const fetchedData = await res.json();
          setData({
            ...fetchedData,
            activity_metrics: fetchedData.activity_metrics || { total_repos: 0, estimated_commits: 0 }
          });
        }
      } catch (error) {
        console.error("Failed to fetch real GitHub intelligence", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchGitHubData();
  }, []);

  return (
    <div className="glass-panel hover:border-brand-500/30 transition-colors">
      <div className="flex items-center space-x-3 mb-4 border-b border-gray-800 pb-4">
        <Github className="w-6 h-6 text-brand-400" />
        <h2 className="text-xl font-semibold">GitHub Intelligence</h2>
        {isLoading && <Loader2 className="w-4 h-4 animate-spin text-gray-400 ml-2" />}
      </div>
      
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-800">
          <p className="text-sm text-gray-400">Developer Score</p>
          <p className="text-3xl font-bold text-brand-400">{data.developer_score}<span className="text-sm text-gray-500">/100</span></p>
        </div>
        <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-800">
          <p className="text-sm text-gray-400">Activity</p>
          <div className="flex items-center space-x-2 mt-1">
            <Activity className="w-4 h-4 text-green-400" />
            <p className="font-medium">{data.activity_metrics.estimated_commits} Commits</p>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <h3 className="text-sm text-gray-400 mb-2">Key Strengths</h3>
        <div className="flex flex-wrap gap-2">
          {data.strengths.map(s => (
            <span key={s} className="px-2 py-1 text-xs font-medium bg-green-900/30 text-green-400 rounded-md border border-green-500/20">{s}</span>
          ))}
        </div>
      </div>
      
      <div>
        <h3 className="text-sm text-gray-400 mb-2">Detected Tech Stack</h3>
        <div className="flex flex-wrap gap-2">
          {data.tech_stack_detected.map(s => (
            <span key={s} className="flex items-center px-2 py-1 text-xs font-medium bg-brand-900/20 text-brand-300 rounded-md border border-brand-500/20">
              <Code className="w-3 h-3 mr-1" /> {s}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
