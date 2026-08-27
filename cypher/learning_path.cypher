// Query 8: Learning Path (Finds learning path between two skills and returns structured graph)
// Parameters:
//   $from_id: ID of the starting skill
//   $to_id: ID of the target skill
MATCH path = (a:Skill {id: $from_id})-[:PREREQUISITE_OF*1..10]->(b:Skill {id: $to_id})
WITH path,
     [node IN nodes(path) | {id: node.id, name: node.name, type: labels(node)[0]}] AS nodes,
     [rel IN relationships(path) | {from: startNode(rel).id, to: endNode(rel).id, type: type(rel)}] AS relationships
RETURN nodes, relationships, length(path) AS depth
ORDER BY depth
LIMIT 1
