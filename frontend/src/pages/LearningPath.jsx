import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { findLearningPath, listSkills } from '../services/api';
import PathView from '../components/PathView';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';

export default function LearningPath() {
  const [searchParams] = useSearchParams();
  const initialFrom = searchParams.get('from') || 'css';
  const initialTo = searchParams.get('to') || 'css-animations';

  const [skillsList, setSkillsList] = useState([]);
  const [fromId, setFromId] = useState(initialFrom);
  const [toId, setToId] = useState(initialTo);
  const [path, setPath] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load all skills for dropdowns
  useEffect(() => {
    listSkills()
      .then(setSkillsList)
      .catch(() => {});
  }, []);

  // Auto-search if URL params or initial defaults are ready
  useEffect(() => {
    if (fromId && toId) {
      doSearch(fromId, toId);
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  function doSearch(from, to) {
    setLoading(true);
    setError(null);
    setPath(null);
    findLearningPath(from, to)
      .then(setPath)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }

  function handleSubmit(e) {
    e.preventDefault();
    const from = fromId.trim();
    const to = toId.trim();
    if (from && to) doSearch(from, to);
  }

  return (
    <div className="page learning-path">
      <Link to="/" className="back-link">← Back</Link>

      <h1>Find Learning Path</h1>
      <p>Discover the shortest prerequisite path between any two skills.</p>

      <form onSubmit={handleSubmit} className="path-form">
        <div className="form-row">
          <label>
            From
            {skillsList.length > 0 ? (
              <select value={fromId} onChange={(e) => setFromId(e.target.value)}>
                <option value="">Select starting skill...</option>
                {skillsList.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name} ({s.level})
                  </option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                value={fromId}
                onChange={(e) => setFromId(e.target.value)}
                placeholder="e.g. python"
              />
            )}
          </label>

          <span className="form-arrow">→</span>

          <label>
            To
            {skillsList.length > 0 ? (
              <select value={toId} onChange={(e) => setToId(e.target.value)}>
                <option value="">Select target skill...</option>
                {skillsList.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name} ({s.level})
                  </option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                value={toId}
                onChange={(e) => setToId(e.target.value)}
                placeholder="e.g. react"
              />
            )}
          </label>
        </div>

        <button type="submit" disabled={loading || !fromId || !toId}>
          {loading ? 'Finding...' : 'Find Path'}
        </button>
      </form>

      {loading && <LoadingState message="Finding the shortest learning path..." />}
      {error && <ErrorState message={error} />}
      {path && <PathView path={path} />}
    </div>
  );
}
