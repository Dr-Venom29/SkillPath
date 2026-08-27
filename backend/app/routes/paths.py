"""
Path routes – thin HTTP layer.

Validates HTTP parameters, calls the service, converts domain
exceptions to HTTP status codes.  Contains no business logic.
"""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from ..services.path_service import find_learning_path, PathNotFoundError
from ..services.skill_service import SkillNotFoundError

router = APIRouter()


@router.get("/paths")
async def learning_path(
    from_id: str = Query(..., alias="from", min_length=1),
    to_id: str = Query(..., alias="to", min_length=1),
):
    try:
        result = find_learning_path(from_id, to_id)
        result["found"] = True
        return result
    except SkillNotFoundError as e:
        return JSONResponse(status_code=404, content={"error": str(e)})
    except PathNotFoundError:
        return {
            "found": False,
            "source": from_id,
            "target": to_id,
            "nodes": [],
            "relationships": [],
            "depth": 0,
        }
