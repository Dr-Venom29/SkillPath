import { useState, useEffect } from 'react';
import { useSearchParams, Link, useNavigate } from 'react-router-dom';
import { searchSkills, listRoles } from '../services/api';
import SearchBar from '../components/SearchBar';
import SkillCard from '../components/SkillCard';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';

export default function Home() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const query = searchParams.get('q') || '';

  const [skills, setSkills] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Inline path finder state
  const [fromId, setFromId] = useState('');
  const [toId, setToId] = useState('');

  useEffect(() => {
    if (!query) { setSkills([]); return; }
    setLoading(true);
    setError(null);
    searchSkills(query)
      .then(setSkills)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [query]);

  useEffect(() => {
    listRoles().then(setRoles).catch(() => {});
  }, []);

  function handlePathSubmit(e) {
    e.preventDefault();
    const from = fromId.trim();
    const to = toId.trim();
    if (from && to) {
      navigate(`/paths?from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}`);
    }
  }

  return (
    <div className="page home">
      {/* Hero — only on landing */}
      {!query && (
        <div className="hero">
          <h1>SkillPath</h1>
          <p className="hero-tagline">Understand what to learn next.</p>
          <p className="hero-sub">
            Explore skills, prerequisites, and career requirements
            through their relationships.
          </p>
        </div>
      )}

      <SearchBar initialQuery={query} />

      {/* Search results */}
      {loading && <LoadingState message="Searching..." />}
      {error && <ErrorState message={error} />}

      {!loading && !error && query && (
        <section className="search-results">
          <h2>
            {skills.length === 0
              ? `No skills found for "${query}"`
              : `${skills.length} result${skills.length !== 1 ? 's' : ''} for "${query}"`}
          </h2>
          {skills.length > 0 && (
            <div className="skill-grid">
              {skills.map((s) => <SkillCard key={s.id} skill={s} />)}
            </div>
          )}
        </section>
      )}

      {/* Landing content — only when not searching */}
      {!query && (
        <>
          {/* Roles */}
          {roles.length > 0 && (
            <section className="roles-section">
              <h2>Explore by Role</h2>
              <div className="role-grid">
                {roles.map((role) => (
                  <Link key={role.id} to={`/roles/${role.id}`} className="role-card">
                    <h3>{role.name}</h3>
                    <p>{role.description}</p>
                  </Link>
                ))}
              </div>
            </section>
          )}

          {/* Inline path finder */}
          <section className="path-section">
            <h2>Find a Learning Path</h2>
            <form onSubmit={handlePathSubmit} className="path-form">
              <div className="form-row">
                <label>
                  Starting skill
                  <input
                    type="text"
                    value={fromId}
                    onChange={(e) => setFromId(e.target.value)}
                    placeholder="e.g. prog-fundamentals"
                  />
                </label>
                <span className="form-arrow">→</span>
                <label>
                  Target skill
                  <input
                    type="text"
                    value={toId}
                    onChange={(e) => setToId(e.target.value)}
                    placeholder="e.g. react"
                  />
                </label>
              </div>
              <button type="submit">Find Path</button>
            </form>
          </section>
        </>
      )}
    </div>
  );
}
