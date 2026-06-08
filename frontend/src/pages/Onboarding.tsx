import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BrainCircuit, Github, Target, Briefcase, Loader2, Sparkles } from 'lucide-react';

export default function Onboarding() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    github: '',
    targetRole: 'GenAI Engineer',
    skills: ''
  });
  const [isSyncing, setIsSyncing] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSyncing(true);

    try {
      // 1. Create User
      const userRes = await fetch('http://localhost:8000/api/v1/profile/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: formData.name, email: formData.email, github_username: formData.github })
      });
      
      let userId = 1; // fallback
      if (userRes.ok) {
        const user = await userRes.json();
        userId = user.id;
      }

      // 2. Trigger GitHub Ingestion if provided
      if (formData.github) {
        await fetch(`http://localhost:8000/api/v1/ingest/github?user_id=${userId}&username=${formData.github}`, {
          method: 'POST'
        });
      }

      // 3. Save manual skills if provided
      if (formData.skills && formData.skills.trim() !== '') {
        await fetch(`http://localhost:8000/api/v1/profile/${userId}/skills`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ skills: formData.skills })
        });
      }
      
      // Simulate slight delay for effect
      setTimeout(() => {
        setIsSyncing(false);
        navigate('/dashboard'); // Redirect to Dashboard
      }, 1500);

    } catch (error) {
      console.error('Error during onboarding syncing', error);
      setIsSyncing(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="max-w-xl w-full">
        <div className="text-center mb-10">
          <BrainCircuit className="w-12 h-12 text-brand-500 mx-auto mb-4" />
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-brand-400 to-brand-600 mb-2">
            Initialize Digital Twin
          </h1>
          <p className="text-gray-400">Connect your profiles to generate personalized career intelligence.</p>
        </div>

        <form onSubmit={handleSubmit} className="glass-panel space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">Full Name</label>
            <div className="relative">
              <UserIcon className="absolute left-3 top-3 w-5 h-5 text-gray-500" />
              <input 
                type="text" 
                required
                className="w-full bg-gray-900/50 border border-gray-800 rounded-lg py-2.5 pl-10 pr-4 focus:outline-none focus:border-brand-500/50 text-white"
                placeholder="John Doe"
                value={formData.name}
                onChange={e => setFormData({...formData, name: e.target.value})}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">GitHub Username</label>
            <div className="relative">
              <Github className="absolute left-3 top-3 w-5 h-5 text-gray-500" />
              <input 
                type="text" 
                className="w-full bg-gray-900/50 border border-gray-800 rounded-lg py-2.5 pl-10 pr-4 focus:outline-none focus:border-brand-500/50 text-white"
                placeholder="torvalds"
                value={formData.github}
                onChange={e => setFormData({...formData, github: e.target.value})}
              />
            </div>
            <p className="text-xs text-gray-500 mt-1">Used to calculate your Developer Strength Score.</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">Target Role</label>
            <div className="relative">
              <Target className="absolute left-3 top-3 w-5 h-5 text-gray-500" />
              <select 
                className="w-full bg-gray-900/50 border border-gray-800 rounded-lg py-2.5 pl-10 pr-4 focus:outline-none focus:border-brand-500/50 text-white appearance-none"
                value={formData.targetRole}
                onChange={e => setFormData({...formData, targetRole: e.target.value})}
              >
                <option>Data Scientist</option>
                <option>ML Engineer</option>
                <option>GenAI Engineer</option>
                <option>Data Analyst</option>
                <option>AI Engineer</option>
                <option>MLOps Engineer</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">Current Top Skills (comma separated)</label>
            <div className="relative">
              <Briefcase className="absolute left-3 top-3 w-5 h-5 text-gray-500" />
              <input 
                type="text" 
                className="w-full bg-gray-900/50 border border-gray-800 rounded-lg py-2.5 pl-10 pr-4 focus:outline-none focus:border-brand-500/50 text-white"
                placeholder="Python, React, Machine Learning..."
                value={formData.skills}
                onChange={e => setFormData({...formData, skills: e.target.value})}
              />
            </div>
          </div>

          <button 
            type="submit" 
            disabled={isSyncing}
            className="w-full bg-brand-600 hover:bg-brand-500 text-white font-medium py-3 rounded-lg transition-colors flex items-center justify-center mt-8 disabled:opacity-50"
          >
            {isSyncing ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Syncing Intelligence...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5 mr-2" />
                Generate Digital Twin
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}

function UserIcon({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
    </svg>
  );
}
