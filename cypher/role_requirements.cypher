// Query 5: Direct Role Requirements
// Parameters:
//   $role_id: The ID of the role
MATCH (r:Role {id: $role_id})-[:REQUIRES]->(s:Skill)
RETURN
    s.id AS id,
    s.name AS name,
    s.level AS level
ORDER BY s.name;

// Query 6: Role + Prerequisite Graph (Required skills plus their prerequisite paths)
// Parameters:
//   $role_id: The ID of the role
MATCH (r:Role {id: $role_id})-[:REQUIRES]->(s:Skill)
OPTIONAL MATCH path = (p:Skill)-[:PREREQUISITE_OF*1..5]->(s)
RETURN
    s.id AS target_skill_id,
    s.name AS target_skill_name,
    [node in nodes(path) | {id: node.id, name: node.name, level: node.level}] AS prerequisite_chain,
    length(path) AS depth
ORDER BY target_skill_name, depth;
