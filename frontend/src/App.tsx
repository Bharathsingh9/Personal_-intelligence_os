import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import CopilotHub from './pages/CopilotHub';
import Onboarding from './pages/Onboarding';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-950 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-gray-900 via-gray-950 to-black text-white">
        <Routes>
          <Route path="/" element={<Onboarding />} />
          <Route path="/hub" element={<CopilotHub />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
