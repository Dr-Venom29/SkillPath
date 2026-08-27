"""
Role routes – thin HTTP layer.

Validates HTTP parameters, calls the service, converts domain
exceptions to HTTP status codes.  Contains no business logic.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..services.role_service import (
    list_roles,
    get_role_requirements,
    get_role_prerequisite_graph,
    RoleNotFoundError,
)

router = APIRouter()


@router.get("/roles")
async def roles_list():
    return list_roles()


@router.get("/roles/{role_id}")
async def role_detail(role_id: str):
    try:
        skills = get_role_requirements(role_id)
        return {"role_id": role_id, "required_skills": skills}
    except RoleNotFoundError:
        return JSONResponse(status_code=404, content={"error": f"Role '{role_id}' not found"})


@router.get("/roles/{role_id}/graph")
async def role_graph(role_id: str):
    try:
        return get_role_prerequisite_graph(role_id)
    except RoleNotFoundError:
        return JSONResponse(status_code=404, content={"error": f"Role '{role_id}' not found"})
