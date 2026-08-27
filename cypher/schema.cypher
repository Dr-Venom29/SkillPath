// Skill constraints and indexes
CREATE CONSTRAINT skill_id_unique FOR (s:Skill) REQUIRE s.id IS UNIQUE;
CREATE INDEX skill_name_idx FOR (s:Skill) ON (s.name);

// Role constraints and indexes
CREATE CONSTRAINT role_id_unique FOR (r:Role) REQUIRE r.id IS UNIQUE;
CREATE INDEX role_name_idx FOR (r:Role) ON (r.name);

// Course constraints and indexes
CREATE CONSTRAINT course_id_unique FOR (c:Course) REQUIRE c.id IS UNIQUE;
CREATE INDEX course_name_idx FOR (c:Course) ON (c.name);

// Project constraints and indexes
CREATE CONSTRAINT project_id_unique FOR (p:Project) REQUIRE p.id IS UNIQUE;
CREATE INDEX project_name_idx FOR (p:Project) ON (p.name);
