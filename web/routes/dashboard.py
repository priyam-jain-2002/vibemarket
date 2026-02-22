"""
Dashboard routes for Vibe-Leads.

Main landing page with stats overview and recent leads.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from storage.database import get_db, get_dashboard_stats, get_all_leads, get_conversion_funnel

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Main dashboard page.

    Shows:
    - Key metrics (total leads, qualified, contacted, etc.)
    - Recent leads
    - Conversion funnel
    - Quick actions
    """
    templates = request.app.state.templates

    with get_db() as db:
        # Get dashboard statistics
        stats = get_dashboard_stats(db, days=30)

        # Get recent leads (last 10)
        recent_leads = get_all_leads(db, limit=10, offset=0)

        # Get conversion funnel
        funnel = get_conversion_funnel(db)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "stats": stats,
            "recent_leads": recent_leads,
            "funnel": funnel,
            "page": "dashboard"
        }
    )


@router.get("/stats")
async def get_stats():
    """
    API endpoint for dashboard stats (for htmx updates).

    Returns JSON with current statistics.
    """
    with get_db() as db:
        stats = get_dashboard_stats(db, days=30)
        funnel = get_conversion_funnel(db)

    return {
        "stats": stats,
        "funnel": funnel
    }
