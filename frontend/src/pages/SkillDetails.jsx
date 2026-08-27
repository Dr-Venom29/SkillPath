import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getSkillDetails, getPrerequisites, getNextSkills } from '../services/api';
import SkillCard from '../components/SkillCard';
import SkillGraph from '../components/SkillGraph';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';

export default function SkillDetails() {
  const { skillId } = useParams();
  const [skill, setSkill] = useState(null);
  const [prereqs, setPrereqs] = useState(null);
  const [nextSkills, setNextSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    Promise.all([
      getSkillDetails(skillId),
      getPrerequisites(skillId),
      getNextSkills(skillId).catch(() => ({ nextSkills: [] })),
    ])
      .then(([s, p, n]) => {
        setSkill(s);
        setPrereqs(p);
        setNextSkills(n.nextSkills || []);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [skillId]);

  if (loading) return <LoadingState message="Loading skill details..." />;
  if (error) return <ErrorState title="Skill not found" message={error} />;
  if (!skill) return <ErrorState title="Skill not found" message="Skill not found. Try searching for Python, React, or SQL." />;

  const hasPrereqs = prereqs && prereqs.direct.length > 0;
  const hasChain = prereqs && prereqs.chain.length > 0;
  const hasNext = nextSkills && nextSkills.length > 0;
  const hasRelated = skill.related && skill.related.length > 0;
  const hasCourses = skill.courses && skill.courses.length > 0;
  const hasProjects = skill.projects && skill.projects.length > 0;
  const hasRoles = skill.roles && skill.roles.length > 0;

  return (
    <div className="page skill-details">
      <Link to="/" className="back-link">← Back to search</Link>

      {/* Header */}
      <header className="skill-header">
        <h1>{skill.name}</h1>
        <span className={`level level-${skill.level?.toLowerCase()}`}>
          {skill.level}
        </span>
      </header>
      <p className="skill-description">{skill.description}</p>

      {/* Prerequisites */}
      {hasPrereqs && (
        <section className="detail-section">
          <h2>Prerequisites</h2>
          <div className="divider" />
          <div className="skill-grid">
            {prereqs.direct.map((s) => <SkillCard key={s.id} skill={s} />)}
          </div>
        </section>
      )}

      {/* Prerequisite Chain */}
      {hasChain && (
        <section className="detail-section">
          <h2>Prerequisite Chain</h2>
          <div className="divider" />
          <SkillGraph chains={prereqs.chain} targetSkillId={skillId} />
        </section>
      )}

      {/* Next Recommended Skills */}
      {hasNext && (
        <section className="detail-section">
          <h2>Next Recommended Skills</h2>
          <p className="section-sub">Skills that directly build upon {skill.name}:</p>
          <div className="divider" />
          <div className="skill-grid">
            {nextSkills.map((s) => <SkillCard key={s.id} skill={s} />)}
          </div>
        </section>
      )}

      {/* Used by Roles */}
      {hasRoles && (
        <section className="detail-section">
          <h2>Used by Roles</h2>
          <div className="divider" />
          <div className="role-grid">
            {skill.roles.map((r) => (
              <Link key={r.id} to={`/roles/${r.id}`} className="role-card">
                <h3>{r.name}</h3>
                {r.description && <p>{r.description}</p>}
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Courses */}
      {hasCourses && (
        <section className="detail-section">
          <h2>Courses Teaching This Skill</h2>
          <div className="divider" />
          <ul className="resource-list">
            {skill.courses.map((c) => (
              <li key={c.id}>
                <strong>{c.name}</strong>
                {c.description && <span> — {c.description}</span>}
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Projects */}
      {hasProjects && (
        <section className="detail-section">
          <h2>Projects Building This Skill</h2>
          <div className="divider" />
          <ul className="resource-list">
            {skill.projects.map((p) => (
              <li key={p.id}>
                <strong>{p.name}</strong>
                {p.description && <span> — {p.description}</span>}
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Related Skills */}
      {hasRelated && (
        <section className="detail-section">
          <h2>Related / Complementary Skills</h2>
          <div className="divider" />
          <div className="skill-grid">
            {skill.related.map((s) => <SkillCard key={s.id} skill={s} />)}
          </div>
        </section>
      )}
    </div>
  );
}
