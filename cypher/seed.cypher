// 1. Create Skill Nodes
MERGE (s_http:Skill {id: "http", name: "HTTP", description: "Hypertext Transfer Protocol, the foundation of data communication for the World Wide Web.", level: "Beginner"})
MERGE (s_rest:Skill {id: "rest-apis", name: "REST APIs", description: "Representational State Transfer APIs, standard architectural style for web services.", level: "Intermediate"})
MERGE (s_python:Skill {id: "python", name: "Python", description: "Python programming language, widely used for general-purpose programming and data science.", level: "Beginner"})
MERGE (s_sql:Skill {id: "sql", name: "SQL", description: "Structured Query Language, standard language for database management.", level: "Beginner"})
MERGE (s_auth:Skill {id: "authentication", name: "Authentication", description: "Mechanisms for verifying the identity of a user or process (OAuth, JWT, Session).", level: "Intermediate"})

// 2. Create Role Nodes
MERGE (r_backend:Role {id: "backend-developer", name: "Backend Developer", description: "Responsible for server-side web application logic and integration of frontend work."})

// 3. Create Course Nodes
MERGE (c_py_fund:Course {id: "python-fundamentals", name: "Python Fundamentals", description: "A comprehensive introduction to Python basics, syntax, and scripting."})

// 4. Create Project Nodes
MERGE (p_rest_proj:Project {id: "rest-api-project", name: "REST API Project", description: "Build a complete backend RESTful API with database connectivity."})

// 5. Establish (:Skill)-[:PREREQUISITE_OF]->(:Skill)
MERGE (s_http)-[:PREREQUISITE_OF]->(s_rest)

// 6. Establish (:Role)-[:REQUIRES]->(:Skill)
MERGE (r_backend)-[:REQUIRES]->(s_python)
MERGE (r_backend)-[:REQUIRES]->(s_rest)
MERGE (r_backend)-[:REQUIRES]->(s_sql)

// 7. Establish (:Course)-[:TEACHES]->(:Skill)
MERGE (c_py_fund)-[:TEACHES]->(s_python)

// 8. Establish (:Project)-[:BUILDS]->(:Skill)
MERGE (p_rest_proj)-[:BUILDS]->(s_rest)

// 9. Establish (:Skill)-[:RELATED_TO]->(:Skill)
MERGE (s_rest)-[:RELATED_TO]->(s_auth)
