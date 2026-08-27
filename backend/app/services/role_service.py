"""
Role service – application logic for role-related operations.

Validates inputs, calls the repository, handles not-found cases.
Contains no Cypher and no FastAPI response objects.
"""

from typing import Any, Dict, List
from ..repositories.graph_repository import (
    list_roles as _list_roles,
    get_role_requirements as _requirements,
    get_role_prerequisite_graph as _prereq_graph,
)


class RoleNotFoundError(Exception):
    """Raised when a role ID does not exist in the graph."""
    def __init__(self, role_id: str):
        self.role_id = role_id
        super().__init__(f"Role '{role_id}' not found")


def list_roles() -> List[Dict[str, Any]]:
    """Return all roles."""
    return _list_roles()


def get_role_requirements(role_id: str) -> List[Dict[str, Any]]:
    """Return skills directly required by a role.

    Raises RoleNotFoundError if the role returns no skills
    (which means the role ID does not exist).
    """
    role_id = role_id.strip()
    if not role_id:
        raise RoleNotFoundError(role_id)

    skills = _requirements(role_id)
    if not skills:
        raise RoleNotFoundError(role_id)
    return skills


def get_role_prerequisite_graph(role_id: str) -> List[Dict[str, Any]]:
    """Return required skills for a role together with their
    full prerequisite chains.

    Raises RoleNotFoundError if the role does not exist.
    """
    # Verify the role exists by checking requirements first
    get_role_requirements(role_id)
    return _prereq_graph(role_id)
