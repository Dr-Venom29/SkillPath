"""
Health check endpoints.
Provides a simple /api/health route that reports application and database status.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..db.driver import verify_connection

router = APIRouter()

@router.get("/health", response_model=dict)
async def health_check():
    """Return health status of the API and database connection.
    If the Neo4j driver cannot verify connectivity, report "unhealthy".
    """
    try:
        verify_connection()
        db_status = "connected"
        app_status = "healthy"
    except Exception as e:
        # Log the exception details for debugging
        print(f"Database health check failed: {type(e).__name__}: {e}")
        db_status = "unavailable"
        app_status = "unhealthy"
        return JSONResponse(status_code=503, content={"status": app_status, "database": db_status})
    return JSONResponse(content={"status": app_status, "database": db_status})
