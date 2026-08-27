"""
Path service – application logic for learning-path operations.

Validates that source and target skills exist, executes the path
query, and converts the graph result into application-level data.
Contains no Cypher and no FastAPI response objects.
"""

from typing import Any, Dict, Optional
from ..repositories.graph_repository import find_learning_path as _find_path
from .skill_service import get_skill_details, SkillNotFoundError


class PathNotFoundError(Exception):
    """Raised when no learning path exists between two skills."""
    def __init__(self, from_id: str, to_id: str):
        self.from_id = from_id
        self.to_id = to_id
        super().__init__(f"No learning path from '{from_id}' to '{to_id}'")


def find_learning_path(from_id: str, to_id: str) -> Dict[str, Any]:
    """Find the shortest prerequisite-based learning path.

    1. Validates that both source and target skills exist.
    2. Executes the path query via the repository.
    3. Converts the raw graph result into a clean response.

    Raises:
        SkillNotFoundError  – if either skill ID does not exist.
        PathNotFoundError   – if no prerequisite path connects them.
    """
    from_id = from_id.strip()
    to_id = to_id.strip()

    # Validate source and target exist
    source = get_skill_details(from_id)
    target = get_skill_details(to_id)

    # Execute path query
    result = _find_path(from_id, to_id)
    if result is None:
        raise PathNotFoundError(from_id, to_id)

    # Convert graph result into application-level data
    return {
        "source": {"id": source["id"], "name": source["name"]},
        "target": {"id": target["id"], "name": target["name"]},
        "nodes": result["nodes"],
        "relationships": result["relationships"],
        "depth": result["depth"],
    }
