import { useState } from 'react';
import { Link } from 'react-router-dom';
import GraphVisualization from './GraphVisualization';

/**
 * PathView – renders a learning path as a visual step sequence & SVG graph diagram.
 *
 * Architecture:
 *   CognoDB → Backend → JSON → React → PathView & GraphVisualization
 *
 * Props:
 *   path: { found, nodes, relationships, depth, source, target }
 */
export default function PathView({ path }) {
  const [viewMode, setViewMode] = useState('steps'); // 'steps' | 'graph'

  if (!path) return null;

  if (!path.found) {
    return (
      <div className="path-not-found">
        <h3>No learning path found</h3>
        <p>
          These skills aren't currently connected in the SkillPath graph.
        </p>
        <p>Try choosing a different starting or target skill.</p>
      </div>
    );
  }

  return (
    <div className="path-result">
      <div className="path-result-header">
        <h2>Learning Path</h2>
        <div className="path-header-right">
          <div className="view-toggle">
            <button
              type="button"
              className={viewMode === 'steps' ? 'active' : ''}
              onClick={() => setViewMode('steps')}
            >
              Step Sequence
            </button>
            <button
              type="button"
              className={viewMode === 'graph' ? 'active' : ''}
              onClick={() => setViewMode('graph')}
            >
              Graph Diagram
            </button>
          </div>
          <span className="path-step-count">
            {path.nodes.length} skills · {path.depth} {path.depth === 1 ? 'prerequisite link' : 'prerequisite links'}
          </span>
        </div>
      </div>

      {viewMode === 'steps' ? (
        <div className="path-nodes">
          {path.nodes.map((node, i) => (
            <div key={node.id} className="path-step">
              <Link to={`/skills/${node.id}`} className="path-node">
                <span className="path-node-name">{node.name}</span>
                <span className="path-node-type">{node.type || 'Skill'}</span>
              </Link>
              {i < path.nodes.length - 1 && (
                <div className="path-arrow">↓</div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <GraphVisualization nodes={path.nodes} relationships={path.relationships} />
      )}
    </div>
  );
}
