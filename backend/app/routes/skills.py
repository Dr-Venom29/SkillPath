"""
Skill routes – thin HTTP layer.

Validates HTTP parameters, calls the service, converts domain
exceptions to HTTP status codes.  Contains no business logic.
"""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from ..services.skill_service import (
    list_skills,
    search_skills,
    get_skill_details,
    get_prerequisites,
    get_prerequisite_chain,
    get_related_skills,
    get_next_skills,
    SkillNotFoundError,
)

router = APIRouter()


@router.get("/skills")
async def get_all_skills():
    return list_skills()


@router.get("/skills/search")
async def search(q: str = Query(..., min_length=1), limit: int = Query(25, ge=1, le=100)):
    results = search_skills(q, limit)
    return results


@router.get("/skills/{skill_id}")
async def skill_detail(skill_id: str):
    try:
        return get_skill_details(skill_id)
    except SkillNotFoundError:
        return JSONResponse(status_code=404, content={"error": f"Skill '{skill_id}' not found"})


@router.get("/skills/{skill_id}/prerequisites")
async def skill_prerequisites(skill_id: str):
    try:
        return {
            "skill_id": skill_id,
            "direct": get_prerequisites(skill_id),
            "chain": get_prerequisite_chain(skill_id),
        }
    except SkillNotFoundError:
        return JSONResponse(status_code=404, content={"error": f"Skill '{skill_id}' not found"})


@router.get("/skills/{skill_id}/related")
async def skill_related(skill_id: str):
    try:
        return get_related_skills(skill_id)
    except SkillNotFoundError:
        return JSONResponse(status_code=404, content={"error": f"Skill '{skill_id}' not found"})


@router.get("/skills/{skill_id}/chain")
async def skill_chain(skill_id: str):
    try:
        return get_prerequisite_chain(skill_id)
    except SkillNotFoundError:
        return JSONResponse(status_code=404, content={"error": f"Skill '{skill_id}' not found"})


@router.get("/skills/{skill_id}/next")
async def skill_next(skill_id: str):
    try:
        return {
            "skill": skill_id,
            "nextSkills": get_next_skills(skill_id)
        }
    except SkillNotFoundError:
        return JSONResponse(status_code=404, content={"error": f"Skill '{skill_id}' not found"})
