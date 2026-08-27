import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { findLearningPath } from '../services/api';
import PathView from '../components/PathView';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';

export default function LearningPath() {
  const [searchParams] = useSearchParams();
  const initialFrom = searchParams.get('from') || '';
  const initialTo = searchParams.get('to') || '';

  const [fromId, setFromId] = useState(initialFrom);
  const [toId, setToId] = useState(initialTo);
  const [path, setPath] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Auto-search if URL params are present
  useEffect(() => {
    if (initialFrom && initialTo) {
      doSearch(initialFrom, initialTo);
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
      <p>Discover the shortest prerequisite path between two skills.</p>

      <form onSubmit={handleSubmit} className="path-form">
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
        <button type="submit" disabled={loading}>
          {loading ? 'Finding...' : 'Find Path'}
        </button>
      </form>

      {loading && <LoadingState message="Finding path..." />}
      {error && <ErrorState message={error} />}
      {path && <PathView path={path} />}
    </div>
  );
}
