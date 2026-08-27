import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getRoleDetails, getRoleGraph } from '../services/api';
import SkillCard from '../components/SkillCard';
import SkillGraph from '../components/SkillGraph';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';

function formatRoleName(id) {
  return id.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function RoleDetails() {
  const { roleId } = useParams();
  const [role, setRole] = useState(null);
  const [roleGraph, setRoleGraph] = useState([]);
  const [showPrereqs, setShowPrereqs] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    Promise.all([
      getRoleDetails(roleId),
      getRoleGraph(roleId).catch(() => []),
    ])
      .then(([roleData, graphData]) => {
        setRole(roleData);
        setRoleGraph(graphData);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [roleId]);

  if (loading) return <LoadingState message="Loading role details..." />;
  if (error) return <ErrorState title="Role not found" message={error} />;
  if (!role) return <ErrorState title="Role not found" message="Role not found. Browse all career roles." />;

  const skills = role.required_skills || [];

  const filteredChains = roleGraph
    .filter((row) => row.prerequisite_chain && row.prerequisite_chain.length > 1)
    .map((row) => ({
      target_skill_name: row.target_skill_name,
      skill_chain: row.prerequisite_chain,
      depth: row.depth,
    }));

  return (
    <div className="page role-details">
      <Link to="/roles" className="back-link">← Back to Roles</Link>

      <header className="role-header">
        <h1>{formatRoleName(role.role_id)}</h1>
        <p className="role-meta">
          {skills.length} required skill{skills.length !== 1 ? 's' : ''}
        </p>
      </header>

      {/* Required Skills Checklist */}
      <section className="detail-section">
        <h2>Required skills</h2>
        <div className="divider" />
        <div className="required-skills-checklist">
          {skills.map((skill) => (
            <div key={skill.id} className="checklist-item">
              <span className="checkmark">✓</span>
              <Link to={`/skills/${skill.id}`} className="checklist-name">
                {skill.name}
              </Link>
              <span className={`level level-${skill.level?.toLowerCase()}`}>
                {skill.level}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* Full Cards View */}
      <section className="detail-section">
        <h2>Skill Details</h2>
        <div className="divider" />
        <div className="skill-grid">
          {skills.map((skill) => (
            <SkillCard key={skill.id} skill={skill} />
          ))}
        </div>
      </section>

      {/* Explore Prerequisites */}
      {filteredChains.length > 0 && (
        <section className="detail-section">
          <div className="prereq-toggle-header">
            <h2>Explore learning prerequisites</h2>
            <button
              type="button"
              className="toggle-button"
              onClick={() => setShowPrereqs(!showPrereqs)}
            >
              {showPrereqs ? 'Hide prerequisite graph' : 'Show prerequisite graph'}
            </button>
          </div>
          <div className="divider" />
          {showPrereqs && (
            <div className="role-prereq-graph">
              <p className="section-sub">
                Prerequisite chains required before mastering the core skills for this role:
              </p>
              <SkillGraph chains={filteredChains} />
            </div>
          )}
        </section>
      )}
    </div>
  );
}
