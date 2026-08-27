"""
FastAPI application entry point.
It registers routes and manages the Neo4j driver lifecycle.
"""

from fastapi import FastAPI
from .config import settings
from .db.driver import create_driver, close_driver, verify_connection
from .routes import health

app = FastAPI(title="SkillPath API", version="0.1.0")

# Include routers
app.include_router(health.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    # Initialize shared Neo4j driver
    create_driver(settings.COGNODB_URI, settings.COGNODB_USERNAME, settings.COGNODB_PASSWORD)
    # Verify connection – any exception will be logged but not crash the app
    try:
        verify_connection()
    except Exception:
        # Connection issues are handled in the health endpoint
        pass

@app.on_event("shutdown")
async def shutdown_event():
    close_driver()
