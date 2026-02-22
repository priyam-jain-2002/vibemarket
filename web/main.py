"""
Vibe-Leads Web Application

FastAPI-based web UI for managing leads, scraping, and outreach.
Uses htmx for interactive UI without complex JavaScript.
"""

import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Import routes (will be created)
from web.routes import dashboard, leads

# Initialize FastAPI app
app = FastAPI(
    title="Vibe-Leads",
    description="Quality-First Lead Generation System",
    version="0.9.0"
)

# CORS middleware (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup static files and templates
static_path = Path(__file__).parent / "static"
templates_path = Path(__file__).parent / "templates"

# Ensure directories exist
static_path.mkdir(parents=True, exist_ok=True)
templates_path.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
templates = Jinja2Templates(directory=str(templates_path))

# Make templates available to routes
app.state.templates = templates


# ============================================================================
# ROOT ROUTE
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Redirect to dashboard"""
    return RedirectResponse(url="/dashboard")


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.9.0",
        "service": "vibe-leads"
    }


# ============================================================================
# REGISTER ROUTES
# ============================================================================

# Dashboard routes
app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["dashboard"]
)

# Leads management routes
app.include_router(
    leads.router,
    prefix="/leads",
    tags=["leads"]
)

# TODO: Add these in later phases
# app.include_router(scrapers.router, prefix="/scrapers", tags=["scrapers"])
# app.include_router(email.router, prefix="/email", tags=["email"])
# app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 page"""
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "error": "Page not found", "code": 404},
        status_code=404
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    """Custom 500 page"""
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "error": "Internal server error", "code": 500},
        status_code=500
    )


# ============================================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("🚀 Vibe-Leads starting up...")

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Initialize database (creates tables if they don't exist)
    from storage.models import init_db
    init_db()

    print("✅ Database initialized")
    print("✅ Vibe-Leads ready! Open http://localhost:8000")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("👋 Vibe-Leads shutting down...")


if __name__ == "__main__":
    import uvicorn

    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                                ║
    ║                      🎯 VIBE-LEADS                            ║
    ║              Quality-First Lead Generation                     ║
    ║                                                                ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "web.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (development)
        log_level="info"
    )
