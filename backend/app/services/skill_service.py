"""
Skill service – application logic for skill-related operations.

Validates inputs, calls the repository, handles not-found cases.
Contains no Cypher and no FastAPI response objects.
"""

from typing import Any, Dict, List, Optional
from ..repositories.graph_repository import (
    list_skills as _list_skills,
    search_skills as _search,
    get_skill_details as _details,
    get_prerequisites as _prereqs,
    get_prerequisite_chain as _chain,
    get_related_skills as _related,
    get_next_skills as _next,
)


class SkillNotFoundError(Exception):
    """Raised when a skill ID does not exist in the graph."""
    def __init__(self, skill_id: str):
        self.skill_id = skill_id
        super().__init__(f"Skill '{skill_id}' not found")


def list_skills() -> List[Dict[str, Any]]:
    """Return all skills."""
    return _list_skills()


def search_skills(query: str, limit: int = 25) -> List[Dict[str, Any]]:
    """Search skills by name.

    Returns an empty list when nothing matches – that is not an error.
    """
    query = query.strip()
    if not query:
        return []
    limit = max(1, min(limit, 100))
    return _search(query, limit)


def get_skill_details(skill_id: str) -> Dict[str, Any]:
    """Return the full graph context for a skill.

    Raises SkillNotFoundError if the skill does not exist.
    """
    skill_id = skill_id.strip()
    if not skill_id:
        raise SkillNotFoundError(skill_id)

    result = _details(skill_id)
    if result is None:
        raise SkillNotFoundError(skill_id)
    return result


def get_prerequisites(skill_id: str) -> List[Dict[str, Any]]:
    """Return direct prerequisites for a skill.

    Raises SkillNotFoundError if the skill does not exist.
    """
    # Verify the skill exists first
    get_skill_details(skill_id)
    return _prereqs(skill_id)


def get_prerequisite_chain(skill_id: str) -> List[Dict[str, Any]]:
    """Return multi-hop prerequisite chains for a skill.

    Raises SkillNotFoundError if the skill does not exist.
    """
    get_skill_details(skill_id)
    return _chain(skill_id)


def get_related_skills(skill_id: str) -> List[Dict[str, Any]]:
    """Return skills connected by RELATED_TO edges.

    Raises SkillNotFoundError if the skill does not exist.
    """
    get_skill_details(skill_id)
    return _related(skill_id)


def get_next_skills(skill_id: str) -> List[Dict[str, Any]]:
    """Return next recommended skills that list this skill as a prerequisite.

    Raises SkillNotFoundError if the skill does not exist.
    """
    get_skill_details(skill_id)
    return _next(skill_id)
