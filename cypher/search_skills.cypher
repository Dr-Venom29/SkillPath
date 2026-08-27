// Query 1: Search skills by name
// Parameters:
//   $query: The search term (substring, case-insensitive)
//   $limit: Max number of records to return
MATCH (s:Skill)
WHERE toLower(s.name) CONTAINS toLower($query)
RETURN
    s.id AS id,
    s.name AS name,
    s.description AS description,
    s.level AS level
ORDER BY s.name
LIMIT $limit
