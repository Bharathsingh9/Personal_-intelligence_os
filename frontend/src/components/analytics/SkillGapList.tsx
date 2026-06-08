import React from 'react';

interface MissingSkill {
  skill_name: string;
  impact_score: number;
  is_core: boolean;
  recommended_order: number;
}

export default function SkillGapList({ missingSkills, targetRole }: { missingSkills: MissingSkill[], targetRole: string }) {
  if (!missingSkills || missingSkills.length === 0) {
    return (
      <div className="text-gray-400 p-4 border border-gray-800 rounded-lg text-center bg-gray-900/30">
        You are fully qualified for {targetRole}!
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="font-medium text-lg">Recommended Learning Path for {targetRole}</h3>
      <div className="space-y-3">
        {missingSkills.map((skill, index) => (
          <div key={index} className="flex items-center justify-between p-3 border border-gray-800 rounded-lg bg-gray-900/40 hover:border-brand-500/30 transition-colors">
            <div className="flex items-center space-x-3">
              <div className="flex items-center justify-center w-6 h-6 rounded-full bg-brand-900/50 text-brand-400 text-xs font-bold border border-brand-500/20">
                {skill.recommended_order}
              </div>
              <div>
                <p className="font-medium text-gray-200">
                  {skill.skill_name}
                  {skill.is_core && <span className="ml-2 text-[10px] bg-red-900/30 text-red-400 px-2 py-0.5 rounded-full border border-red-500/20">CORE</span>}
                </p>
              </div>
            </div>
            <div className="text-sm font-semibold text-brand-400">
              +{skill.impact_score.toFixed(1)}%
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
