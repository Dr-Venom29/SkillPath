// Query 2: Retrieve full graph context for a skill
// Parameters:
//   $skill_id: The ID of the skill
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
    s.id AS id,
    s.name AS name,
    s.description AS description,
    s.level AS level,
    [p in prereqs WHERE p IS NOT NULL | {id: p.id, name: p.name, level: p.level}] AS prerequisites,
    [d in dependents WHERE d IS NOT NULL | {id: d.id, name: d.name, level: d.level}] AS dependents,
    [r in related WHERE r IS NOT NULL | {id: r.id, name: r.name, level: r.level}] AS related,
    [c in courses WHERE c IS NOT NULL | {id: c.id, name: c.name, description: c.description}] AS courses,
    [p in projects WHERE p IS NOT NULL | {id: p.id, name: p.name, description: p.description}] AS projects,
    [r in roles WHERE r IS NOT NULL | {id: r.id, name: r.name, description: r.description}] AS roles
