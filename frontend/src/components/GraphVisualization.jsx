import { useNavigate } from 'react-router-dom';

/**
 * GraphVisualization – pure visual rendering component.
 *
 * Receives `nodes` and `relationships` from API JSON responses and renders
 * an SVG node-edge graph. Does NOT make any network or database queries.
 *
 * Architecture:
 *   CognoDB → Backend → JSON → React → GraphVisualization
 *
 * Props:
 *   nodes: [{ id: string, name: string, type: string }, ...]
 *   relationships: [{ from: string, to: string, type: string }, ...]
 */
export default function GraphVisualization({ nodes = [], relationships = [] }) {
  const navigate = useNavigate();

  if (!nodes || nodes.length === 0) return null;

  // Calculate layout positions
  const nodeWidth = 160;
  const nodeHeight = 50;
  const verticalSpacing = 70;
  const svgWidth = 400;
  const totalHeight = nodes.length * (nodeHeight + verticalSpacing) - verticalSpacing + 60;

  // Compute (x, y) for each node ID in a linear or layered layout
  const nodePositions = {};
  nodes.forEach((node, index) => {
    nodePositions[node.id] = {
      x: svgWidth / 2,
      y: 40 + index * (nodeHeight + verticalSpacing),
    };
  });

  return (
    <div className="graph-visualization-container">
      <svg
        width="100%"
        height={totalHeight}
        viewBox={`0 0 ${svgWidth} ${totalHeight}`}
        className="graph-svg"
      >
        {/* SVG Marker Definitions for Directed Arrowheads */}
        <defs>
          <marker
            id="arrowhead"
            markerWidth="8"
            markerHeight="8"
            refX="4"
            refY="4"
            orient="auto"
          >
            <polygon points="0 0, 8 4, 0 8" fill="#2563eb" />
          </marker>
        </defs>

        {/* Directed Edges / Relationships */}
        {relationships.map((rel, idx) => {
          const fromPos = nodePositions[rel.from];
          const toPos = nodePositions[rel.to];

          if (!fromPos || !toPos) return null;

          const startY = fromPos.y + nodeHeight / 2;
          const endY = toPos.y - nodeHeight / 2 - 6;

          return (
            <g key={`edge-${idx}`} className="graph-edge-group">
              <line
                x1={fromPos.x}
                y1={startY}
                x2={toPos.x}
                y2={endY}
                stroke="#2563eb"
                strokeWidth="2"
                markerEnd="url(#arrowhead)"
              />
              {rel.type && (
                <text
                  x={fromPos.x + 8}
                  y={(startY + endY) / 2}
                  fill="#6b7280"
                  fontSize="10"
                  fontFamily="sans-serif"
                >
                  {rel.type}
                </text>
              )}
            </g>
          );
        })}

        {/* Graph Nodes */}
        {nodes.map((node) => {
          const pos = nodePositions[node.id];
          if (!pos) return null;

          return (
            <g
              key={`node-${node.id}`}
              className="graph-node-group"
              onClick={() => navigate(`/skills/${node.id}`)}
              style={{ cursor: 'pointer' }}
            >
              {/* Node Box */}
              <rect
                x={pos.x - nodeWidth / 2}
                y={pos.y - nodeHeight / 2}
                width={nodeWidth}
                height={nodeHeight}
                rx="8"
                ry="8"
                fill="#ffffff"
                stroke="#2563eb"
                strokeWidth="2"
                className="graph-node-rect"
              />
              {/* Node Name */}
              <text
                x={pos.x}
                y={pos.y - 4}
                textAnchor="middle"
                fill="#1a1a2e"
                fontSize="13"
                fontWeight="600"
                fontFamily="sans-serif"
              >
                {node.name.length > 20 ? `${node.name.substring(0, 18)}...` : node.name}
              </text>
              {/* Node Type Label */}
              <text
                x={pos.x}
                y={pos.y + 12}
                textAnchor="middle"
                fill="#9ca3af"
                fontSize="9"
                fontWeight="500"
                fontFamily="sans-serif"
              >
                {node.type || 'Skill'}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
