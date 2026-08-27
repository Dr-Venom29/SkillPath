import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { listRoles } from '../services/api';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';

export default function RolesList() {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    listRoles()
      .then(setRoles)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingState message="Loading career roles..." />;
  if (error) return <ErrorState message={error} />;

  return (
    <div className="page roles-list">
      <Link to="/" className="back-link">← Back</Link>

      <h1>Career Roles</h1>
      <p className="subtitle">Select a target career role to see its required skills and learning prerequisites.</p>

      <div className="role-grid">
        {roles.map((role) => (
          <Link key={role.id} to={`/roles/${role.id}`} className="role-card">
            <h3>{role.name}</h3>
            <p>{role.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
