// Query 9: Multi-hop prerequisite ancestors for a skill (up to depth 5)
// Parameters:
//   $skill_id: ID of the target skill
MATCH path = (s:Skill {id: $skill_id})<-[:PREREQUISITE_OF*1..5]-(p:Skill)
RETURN path
