// Given a skill ID, find next recommended skills that depend on it
MATCH (s:Skill {id: $skill_id})-[:PREREQUISITE_OF]->(next:Skill)
RETURN
    next.id          AS id,
    next.name        AS name,
    next.description AS description,
    next.level       AS level
ORDER BY next.name
