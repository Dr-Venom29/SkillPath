import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getRoleDetails } from '../services/api';
import SkillCard from '../components/SkillCard';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';

function formatRoleName(id) {
  return id.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function RoleDetails() {
  const { roleId } = useParams();
  const [role, setRole] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getRoleDetails(roleId)
      .then(setRole)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [roleId]);

  if (loading) return <LoadingState message="Loading role..." />;
  if (error) return <ErrorState message={error} />;
  if (!role) return <ErrorState message="Role not found." />;

  const skills = role.required_skills;

  return (
    <div className="page role-details">
      <Link to="/" className="back-link">← Back</Link>

      <h1>{formatRoleName(role.role_id)}</h1>
      <p className="role-meta">
        {skills.length} required skill{skills.length !== 1 ? 's' : ''}
      </p>

      <section className="detail-section">
        <h2>Required Skills</h2>
        <div className="divider" />
        <div className="skill-grid">
          {skills.map((skill) => (
            <SkillCard key={skill.id} skill={skill} />
          ))}
        </div>
      </section>

      <Link to={`/roles/${roleId}/graph`} className="role-graph-link">
        Explore prerequisite graph →
      </Link>
    </div>
  );
}
