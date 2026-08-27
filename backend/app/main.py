"""
FastAPI application entry point.
Registers routes, manages the Neo4j driver lifecycle,
handles CORS permissions, and manages global error responses.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db.driver import create_driver, close_driver, verify_connection
from .routes import health, skills, roles, paths

app = FastAPI(title="SkillPath API", version="0.1.0")

# ---------------------------------------------------------------------------
# CORS Configuration – Allow production Netlify frontend and local dev
# ---------------------------------------------------------------------------

allow_origins = [
    "https://skillpath-demo.netlify.app",
    "http://localhost:5174",
    "http://localhost:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api")
app.include_router(skills.router, prefix="/api")
app.include_router(roles.router, prefix="/api")
app.include_router(paths.router, prefix="/api")


# ---------------------------------------------------------------------------
# Global error handler – never expose raw database exceptions
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch any unhandled exception and return a clean 500 response."""
    print(f"Unhandled error on {request.method} {request.url.path}: {type(exc).__name__}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error. Please try again later."},
    )


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------

@app.on_event("startup")
async def startup_event():
    create_driver(settings.COGNODB_URI, settings.COGNODB_USERNAME, settings.COGNODB_PASSWORD)
    try:
        verify_connection()
        print("CognoDB connection verified.")
    except Exception as e:
        print(f"CognoDB connection failed at startup: {type(e).__name__}: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    close_driver()
