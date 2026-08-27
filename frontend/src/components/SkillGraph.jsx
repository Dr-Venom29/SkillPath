import { Link } from 'react-router-dom';

/**
 * SkillGraph – answers: "What does this skill depend on?"
 *
 * Renders prerequisite chains as vertical node sequences.
 * Each node is clickable. The last node (the target skill) is highlighted.
 */
export default function SkillGraph({ chains, targetSkillId }) {
  if (!chains || chains.length === 0) {
    return <p className="empty-state">No prerequisite chain found.</p>;
  }

  return (
    <div className="skill-graph">
      {chains.map((chain, i) => (
        <div key={i} className="chain-visual">
          {chain.skill_chain.map((node, j) => (
            <span key={node.id}>
              <Link
                to={`/skills/${node.id}`}
                className={`chain-node${node.id === targetSkillId ? ' chain-node-current' : ''}`}
              >
                {node.name}
              </Link>
              {j < chain.skill_chain.length - 1 && (
                <span className="chain-arrow"> → </span>
              )}
            </span>
          ))}
        </div>
      ))}
    </div>
  );
}
