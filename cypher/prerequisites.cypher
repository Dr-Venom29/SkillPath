// Query 3: Direct Prerequisites
// Parameters:
//   $skill_id: The ID of the target skill
MATCH (s:Skill {id: $skill_id})
MATCH (p:Skill)-[:PREREQUISITE_OF]->(s)
RETURN
    p.id AS id,
    p.name AS name,
    p.level AS level
ORDER BY p.name;

// Query 4: Multi-hop Prerequisites
// Parameters:
//   $skill_id: The ID of the target skill
MATCH path = (p:Skill)-[:PREREQUISITE_OF*1..5]->(s:Skill {id: $skill_id})
RETURN
    [node in nodes(path) | {id: node.id, name: node.name, level: node.level}] AS skill_chain,
    length(path) AS depth
ORDER BY depth;
