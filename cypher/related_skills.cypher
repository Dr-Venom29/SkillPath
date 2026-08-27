// Query 7: Related Skills (Undirected connection)
// Parameters:
//   $skill_id: The ID of the skill
MATCH (s:Skill {id: $skill_id})-[:RELATED_TO]-(r:Skill)
RETURN
    r.id AS id,
    r.name AS name,
    r.level AS level
ORDER BY r.name
