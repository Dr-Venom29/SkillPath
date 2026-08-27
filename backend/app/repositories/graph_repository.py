"""
Graph repository – data-access layer for CognoDB.

Every public method runs a single Cypher query and returns plain
Python dicts/lists.  No FastAPI imports, no HTTP exceptions, no
response formatting.

Architecture:
    Route → Service → **Repository** → Cypher → CognoDB

All queries use parameterized Cypher – never string interpolation.
"""

from typing import Any, Dict, List, Optional
from ..db.driver import get_session


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _run_read(query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Execute a read-only Cypher query and return all records as dicts."""
    with get_session() as session:
        result = session.run(query, parameters or {})
        return [record.data() for record in result]


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

def search_skills(query: str, limit: int = 25) -> List[Dict[str, Any]]:
    """Search skills by name (case-insensitive substring match).

    Mirrors: cypher/search_skills.cypher
    """
    cypher = """
        MATCH (s:Skill)
        WHERE toLower(s.name) CONTAINS toLower($query)
        RETURN
            s.id          AS id,
            s.name        AS name,
            s.description AS description,
            s.level       AS level
        ORDER BY s.name
        LIMIT $limit
    """
    return _run_read(cypher, {"query": query, "limit": limit})


def get_skill_details(skill_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve the full graph context for a single skill.

    Returns the skill properties plus collected prerequisites,
    dependents, related skills, courses, projects, and roles.

    Mirrors: cypher/skill_details.cypher
    """
    cypher = """
        MATCH (s:Skill {id: $skill_id})
        OPTIONAL MATCH (p:Skill)-[:PREREQUISITE_OF]->(s)
        WITH s, collect(DISTINCT p) AS prereqs
        OPTIONAL MATCH (s)-[:PREREQUISITE_OF]->(dep:Skill)
        WITH s, prereqs, collect(DISTINCT dep) AS dependents
        OPTIONAL MATCH (s)-[:RELATED_TO]-(rel:Skill)
        WITH s, prereqs, dependents, collect(DISTINCT rel) AS related
        OPTIONAL MATCH (c:Course)-[:TEACHES]->(s)
        WITH s, prereqs, dependents, related, collect(DISTINCT c) AS courses
        OPTIONAL MATCH (proj:Project)-[:BUILDS]->(s)
        WITH s, prereqs, dependents, related, courses, collect(DISTINCT proj) AS projects
        OPTIONAL MATCH (r:Role)-[:REQUIRES]->(s)
        WITH s, prereqs, dependents, related, courses, projects, collect(DISTINCT r) AS roles
        RETURN
            s.id          AS id,
            s.name        AS name,
            s.description AS description,
            s.level       AS level,
            [p in prereqs    WHERE p IS NOT NULL | {id: p.id, name: p.name, level: p.level}] AS prerequisites,
            [d in dependents WHERE d IS NOT NULL | {id: d.id, name: d.name, level: d.level}] AS dependents,
            [r in related    WHERE r IS NOT NULL | {id: r.id, name: r.name, level: r.level}] AS related,
            [c in courses    WHERE c IS NOT NULL | {id: c.id, name: c.name, description: c.description}] AS courses,
            [p in projects   WHERE p IS NOT NULL | {id: p.id, name: p.name, description: p.description}] AS projects,
            [r in roles      WHERE r IS NOT NULL | {id: r.id, name: r.name, description: r.description}] AS roles
    """
    rows = _run_read(cypher, {"skill_id": skill_id})
    return rows[0] if rows else None


# ---------------------------------------------------------------------------
# Prerequisites
# ---------------------------------------------------------------------------

def get_prerequisites(skill_id: str) -> List[Dict[str, Any]]:
    """Return the direct prerequisites for a skill.

    Mirrors: cypher/prerequisites.cypher (Query 3)
    """
    cypher = """
        MATCH (s:Skill {id: $skill_id})
        MATCH (p:Skill)-[:PREREQUISITE_OF]->(s)
        RETURN
            p.id    AS id,
            p.name  AS name,
            p.level AS level
        ORDER BY p.name
    """
    return _run_read(cypher, {"skill_id": skill_id})


def get_prerequisite_chain(skill_id: str) -> List[Dict[str, Any]]:
    """Return multi-hop prerequisite chains (up to depth 5).

    Mirrors: cypher/prerequisites.cypher (Query 4)
    """
    cypher = """
        MATCH path = (p:Skill)-[:PREREQUISITE_OF*1..5]->(s:Skill {id: $skill_id})
        RETURN
            [node in nodes(path) | {id: node.id, name: node.name, level: node.level}] AS skill_chain,
            length(path) AS depth
        ORDER BY depth
    """
    return _run_read(cypher, {"skill_id": skill_id})


# ---------------------------------------------------------------------------
# Related skills
# ---------------------------------------------------------------------------

def get_related_skills(skill_id: str) -> List[Dict[str, Any]]:
    """Return skills connected by an undirected RELATED_TO edge.

    Mirrors: cypher/related_skills.cypher
    """
    cypher = """
        MATCH (s:Skill {id: $skill_id})-[:RELATED_TO]-(r:Skill)
        RETURN
            r.id    AS id,
            r.name  AS name,
            r.level AS level
        ORDER BY r.name
    """
    return _run_read(cypher, {"skill_id": skill_id})


# ---------------------------------------------------------------------------
# Roles
# ---------------------------------------------------------------------------

def get_role_requirements(role_id: str) -> List[Dict[str, Any]]:
    """Return skills directly required by a role.

    Mirrors: cypher/role_requirements.cypher (Query 5)
    """
    cypher = """
        MATCH (r:Role {id: $role_id})-[:REQUIRES]->(s:Skill)
        RETURN
            s.id          AS id,
            s.name        AS name,
            s.level       AS level,
            s.description AS description
        ORDER BY s.name
    """
    return _run_read(cypher, {"role_id": role_id})


def get_role_prerequisite_graph(role_id: str) -> List[Dict[str, Any]]:
    """Return the required skills for a role together with their
    full prerequisite chains.

    Mirrors: cypher/role_requirements.cypher (Query 6)
    """
    cypher = """
        MATCH (r:Role {id: $role_id})-[:REQUIRES]->(s:Skill)
        OPTIONAL MATCH path = (p:Skill)-[:PREREQUISITE_OF*1..5]->(s)
        RETURN
            s.id   AS target_skill_id,
            s.name AS target_skill_name,
            [node in nodes(path) | {id: node.id, name: node.name, level: node.level}] AS prerequisite_chain,
            length(path) AS depth
        ORDER BY target_skill_name, depth
    """
    return _run_read(cypher, {"role_id": role_id})


# ---------------------------------------------------------------------------
# Learning paths
# ---------------------------------------------------------------------------

def find_learning_path(from_id: str, to_id: str) -> Optional[Dict[str, Any]]:
    """Find the shortest prerequisite-based learning path between two skills.

    Mirrors: cypher/learning_path.cypher
    """
    cypher = """
        MATCH path = (a:Skill {id: $from_id})-[:PREREQUISITE_OF*1..10]->(b:Skill {id: $to_id})
        WITH path,
             [node IN nodes(path) | {id: node.id, name: node.name, type: labels(node)[0]}] AS nodes,
             [rel  IN relationships(path) | {from: startNode(rel).id, to: endNode(rel).id, type: type(rel)}] AS relationships
        RETURN nodes, relationships, length(path) AS depth
        ORDER BY depth
        LIMIT 1
    """
    rows = _run_read(cypher, {"from_id": from_id, "to_id": to_id})
    return rows[0] if rows else None
