# SkillPath — Learning Dependency Explorer

SkillPath is a web-based learning path visualization and exploration tool. It helps users understand prerequisite chains, skill dependencies, project/course paths, and roles using a graph database.

## Core Features
1. **Search skills**: Quick lookup of skills.
2. **View skill details**: Descriptions, levels, associated entities.
3. **View prerequisites**: Inspect which skills are required prior to learning a skill.
4. **View related skills**: Check skills with `RELATED_TO` connections.
5. **Explore learning paths**: Discover the step-by-step path between two skills.
6. **View role requirements**: Learn what skills are required for a particular career role.
7. **Graph visualization**: Interactive graph view of nodes and relationships.

## Data Schema
### Node Types
- `Skill`
- `Role`
- `Course`
- `Project`

### Relationship Types
- `PREREQUISITE_OF` (Skill -> Skill)
- `REQUIRES` (Role -> Skill)
- `TEACHES` (Course -> Skill)
- `BUILDS` (Project -> Skill)
- `RELATED_TO` (Skill -> Skill)

## Project Structure
- `backend/`: API services and database query logic.
- `frontend/`: Web user interface.
- `cypher/`: Neo4j schema definitions, migration scripts, and database queries.
- `data/`: Sample datasets (JSON/CSV) for seeding.
