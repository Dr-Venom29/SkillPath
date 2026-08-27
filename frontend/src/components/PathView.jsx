import { Link } from 'react-router-dom';

/**
 * PathView – renders a learning path as a vertical step sequence.
 *
 * Found:     clickable nodes with arrows and step count
 * Not found: helpful message explaining why
 */
export default function PathView({ path }) {
  if (!path) return null;

  if (!path.found) {
    return (
      <div className="path-not-found">
        <h3>No learning path found</h3>
        <p>
          <strong>{path.source}</strong> cannot reach <strong>{path.target}</strong> through
          the available prerequisite relationships.
        </p>
        <p>Try choosing a different starting or target skill.</p>
      </div>
    );
  }

  return (
    <div className="path-result">
      <div className="path-result-header">
        <h2>Learning Path</h2>
        <span className="path-step-count">
          {path.depth} {path.depth === 1 ? 'step' : 'steps'}
        </span>
      </div>
      <div className="path-nodes">
        {path.nodes.map((node, i) => (
          <div key={node.id} className="path-step">
            <Link to={`/skills/${node.id}`} className="path-node">
              <span className="path-node-name">{node.name}</span>
              <span className="path-node-type">{node.type}</span>
            </Link>
            {i < path.nodes.length - 1 && (
              <div className="path-arrow">↓</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
