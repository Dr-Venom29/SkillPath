import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import SkillDetails from './pages/SkillDetails';
import RoleDetails from './pages/RoleDetails';
import LearningPath from './pages/LearningPath';
import './App.css';

export default function App() {
  return (
    <BrowserRouter>
      <nav className="nav">
        <Link to="/" className="nav-brand">SkillPath</Link>
        <div className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/paths">Learning Path</Link>
        </div>
      </nav>

      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/skills/:skillId" element={<SkillDetails />} />
          <Route path="/roles/:roleId" element={<RoleDetails />} />
          <Route path="/paths" element={<LearningPath />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
