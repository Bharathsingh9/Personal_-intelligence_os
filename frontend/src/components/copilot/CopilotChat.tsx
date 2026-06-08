import React, { useState } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';

export default function CopilotChat() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hi! I am your AI Career Copilot. I can generate learning roadmaps or recommend high-impact projects based on your profile gaps. What would you like to explore?' }
  ]);
  const [input, setInput] = useState('');
  
  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { sender: 'user', text: input }]);
    
    setTimeout(() => {
      let botResponse = "I've analyzed your profile.";
      if (input.toLowerCase().includes('roadmap') || input.toLowerCase().includes('learn')) {
        botResponse = "I've generated a personalized 30-day learning roadmap focusing on LangGraph and Vector Databases.";
      } else if (input.toLowerCase().includes('project') || input.toLowerCase().includes('build')) {
        botResponse = "I found some great projects you can build to apply these skills.";
      } else if (input.toLowerCase().includes('simulate') || input.toLowerCase().includes('if i learn')) {
        botResponse = "I ran the career simulator. Learning these skills will boost your Readiness Score by +13.5%.";
      }
      setMessages(prev => [...prev, { sender: 'bot', text: botResponse }]);
    }, 1000);
    
    setInput('');
  };

  return (
    <div className="glass-panel flex flex-col h-[500px] border border-brand-500/30 shadow-[0_0_15px_rgba(20,184,166,0.1)]">
      <div className="flex items-center space-x-2 border-b border-gray-800 pb-3 mb-4">
        <Sparkles className="w-5 h-5 text-brand-400" />
        <h2 className="text-lg font-bold">Multi-Agent Copilot</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2 custom-scrollbar">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex items-start space-x-2 max-w-[80%] ${msg.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.sender === 'user' ? 'bg-blue-900/50 text-blue-400' : 'bg-brand-900/50 text-brand-400'}`}>
                {msg.sender === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>
              <div className={`p-3 rounded-lg text-sm ${msg.sender === 'user' ? 'bg-blue-900/20 text-gray-200 border border-blue-800/30' : 'bg-gray-800/50 text-gray-300 border border-gray-700/50'}`}>
                {msg.text}
              </div>
            </div>
          </div>
        ))}
      </div>
      
      <div className="relative">
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask for a roadmap or project..." 
          className="w-full bg-gray-900 border border-gray-700 rounded-full py-3 pl-4 pr-12 text-sm focus:outline-none focus:border-brand-500 transition-colors text-white"
        />
        <button 
          onClick={handleSend}
          className="absolute right-2 top-1.5 p-1.5 bg-brand-600 hover:bg-brand-500 text-white rounded-full transition-colors"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
