import React, { useState, useEffect } from 'react';
import { User, Briefcase, Award, Code2, Target, BrainCircuit } from 'lucide-react';
import ReadinessRadar from '../components/analytics/ReadinessRadar';
import SkillGapList from '../components/analytics/SkillGapList';
import GitHubIntelligence from '../components/intelligence/GitHubIntelligence';
import LeetCodeIntelligence from '../components/intelligence/LeetCodeIntelligence';
import MarketTrends from '../components/intelligence/MarketTrends';

export default function Dashboard() {
  const [readinessData, setReadinessData] = useState<any[]>([
    { role_id: 1, role_name: 'Data Scientist', total_score: 87 },
    { role_id: 2, role_name: 'ML Engineer', total_score: 81 },
    { role_id: 3, role_name: 'GenAI Engineer', total_score: 66 },
    { role_id: 4, role_name: 'Data Analyst', total_score: 92 },
    { role_id: 5, role_name: 'AI Engineer', total_score: 72 },
    { role_id: 6, role_name: 'MLOps Engineer', total_score: 54 },
  ]);

  const [skillGaps, setSkillGaps] = useState<any[]>([
    { skill_name: 'LangGraph', impact_score: 8.4, is_core: true, recommended_order: 1 },
    { skill_name: 'Vector Databases', impact_score: 6.2, is_core: true, recommended_order: 2 },
    { skill_name: 'LLM Evaluation', impact_score: 5.1, is_core: true, recommended_order: 3 },
    { skill_name: 'Agentic AI', impact_score: 4.0, is_core: false, recommended_order: 4 },
  ]);

  useEffect(() => {
    const fetchIntelligence = async () => {
      try {
        const userId = 1;
        const roleId = 3; // GenAI Engineer target

        // Fetch Readiness
        const readinessRes = await fetch(`http://localhost:8000/api/v1/intelligence/readiness/${userId}`, { method: 'POST' });
        if (readinessRes.ok) {
          const rData = await readinessRes.json();
          if (rData && rData.length > 0) {
            const roleMap: Record<number, string> = {
              1: 'Data Scientist', 2: 'ML Engineer', 3: 'GenAI Engineer',
              4: 'Data Analyst', 5: 'AI Engineer', 6: 'MLOps Engineer'
            };
            setReadinessData(rData.map((r: any) => ({
              ...r,
              role_name: roleMap[r.role_id] || `Role ${r.role_id}`
            })));
          }
        }

        // Fetch Skill Gaps
        const gapsRes = await fetch(`http://localhost:8000/api/v1/intelligence/skill-gaps/${userId}?role_id=${roleId}`);
        if (gapsRes.ok) {
          const gData = await gapsRes.json();
          if (gData && gData.length > 0) {
            setSkillGaps(gData);
          }
        }
      } catch (error) {
        console.error("Failed to fetch real intelligence data:", error);
      }
    };

    fetchIntelligence();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <header className="mb-10 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-brand-400 to-brand-600">
            Career Digital Twin
          </h1>
          <p className="text-gray-400 mt-2">Unified intelligence from your Resume, GitHub, and LeetCode.</p>
        </div>
        <div className="flex items-center space-x-2 bg-brand-900/20 px-4 py-2 rounded-full border border-brand-500/20">
          <BrainCircuit className="w-5 h-5 text-brand-400" />
          <span className="text-sm font-medium text-brand-300">Phase 6 Intelligence Active</span>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <StatCard icon={<Code2 className="w-6 h-6 text-brand-400" />} title="Total Skills" value="24" />
        <StatCard icon={<Briefcase className="w-6 h-6 text-brand-400" />} title="Projects" value="12" />
        <StatCard icon={<Award className="w-6 h-6 text-brand-400" />} title="Certifications" value="3" />
        <StatCard icon={<Target className="w-6 h-6 text-brand-400" />} title="Best Role Match" value="Data Analyst" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <GitHubIntelligence />
        <LeetCodeIntelligence />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        <div className="glass-panel lg:col-span-1">
          <h2 className="text-xl font-semibold mb-2">Career Readiness</h2>
          <p className="text-sm text-gray-400 mb-6">Your compatibility score across target tech roles.</p>
          <ReadinessRadar data={readinessData} />
        </div>
        
        <div className="glass-panel lg:col-span-2">
          <div className="flex justify-between items-end mb-6 border-b border-gray-800 pb-4">
            <div>
              <h2 className="text-xl font-semibold">Skill Gap Analysis</h2>
              <p className="text-sm text-gray-400 mt-1">Discover what's holding you back.</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-400">Targeting Role</p>
              <p className="font-medium text-brand-400">GenAI Engineer (66% Ready)</p>
            </div>
          </div>
          <SkillGapList missingSkills={skillGaps} targetRole="GenAI Engineer" />
        </div>
      </div>
      
      <MarketTrends />
    </div>
  );
}

function StatCard({ icon, title, value }: { icon: React.ReactNode, title: string, value: string }) {
  return (
    <div className="glass-panel flex items-center space-x-4 hover:border-brand-500/50 transition-colors">
      <div className="p-3 bg-brand-900/30 rounded-lg">
        {icon}
      </div>
      <div>
        <p className="text-gray-400 text-sm">{title}</p>
        <p className="text-2xl font-bold">{value}</p>
      </div>
    </div>
  );
}
