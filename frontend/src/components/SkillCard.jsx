import { Link } from 'react-router-dom';

export default function SkillCard({ skill }) {
  return (
    <Link to={`/skills/${skill.id}`} className="skill-card">
      <div className="skill-card-header">
        <h3>{skill.name}</h3>
        <span className={`level level-${skill.level?.toLowerCase()}`}>
          {skill.level}
        </span>
      </div>
      {skill.description && <p>{skill.description}</p>}
    </Link>
  );
}
