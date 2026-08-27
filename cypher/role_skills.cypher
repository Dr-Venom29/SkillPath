// Query: Skills required by a role
// Parameters:
//   $role_id: The ID of the role
MATCH (r:Role {id: $role_id})-[:REQUIRES]->(s:Skill)
RETURN
  s.id AS id,
  s.name AS name,
  s.level AS level,
  s.description AS description
ORDER BY s.name;
