"""
Leads management routes for Vibe-Leads.

Handles lead CRUD operations, analysis, filtering, and status updates.
"""

from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from typing import Optional
from datetime import datetime

from storage.database import (
    get_db,
    get_all_leads,
    count_leads,
    get_lead_by_id,
    create_lead,
    update_lead,
    update_lead_status,
    delete_lead,
    get_tags_for_lead,
    add_tag_to_lead,
    save_lead_analysis
)
from processors.claude_processor import LeadProcessor

router = APIRouter()

# Initialize processor (will be used for analyzing leads)
processor = None  # Lazy load


def get_processor():
    """Get or create processor instance"""
    global processor
    if processor is None:
        processor = LeadProcessor(config_dir="config")
    return processor


@router.get("/", response_class=HTMLResponse)
async def leads_list(
    request: Request,
    page: int = 1,
    score: Optional[str] = None,
    status: Optional[str] = None,
    source: Optional[str] = None,
    search: Optional[str] = None
):
    """
    Leads list page with filtering and pagination.

    Query params:
    - page: Page number (default: 1)
    - score: Filter by score (A+, A, B, C)
    - status: Filter by status
    - source: Filter by source
    - search: Search in name, company, content
    """
    templates = request.app.state.templates

    # Pagination
    per_page = 20
    offset = (page - 1) * per_page

    # Build filters
    filters = {}
    if score:
        filters['score'] = score
    if status:
        filters['status'] = status
    if source:
        filters['source'] = source
    if search:
        filters['search'] = search

    with get_db() as db:
        # Get leads
        leads = get_all_leads(db, limit=per_page, offset=offset, filters=filters)

        # Get total count for pagination
        total_leads = count_leads(db, filters=filters)

    # Calculate pagination
    total_pages = (total_leads + per_page - 1) // per_page

    return templates.TemplateResponse(
        "leads_list.html",
        {
            "request": request,
            "leads": leads,
            "total_leads": total_leads,
            "page": page,
            "total_pages": total_pages,
            "filters": filters,
            "page": "leads"
        }
    )


@router.get("/{lead_id}", response_class=HTMLResponse)
async def lead_detail(request: Request, lead_id: int):
    """
    Lead detail page.

    Shows full lead information, analysis, message, and action buttons.
    """
    templates = request.app.state.templates

    with get_db() as db:
        lead = get_lead_by_id(db, lead_id)

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Get tags
        tags = get_tags_for_lead(db, lead_id)

        # Get status history
        status_history = lead.status_history

        # Get email history
        emails = lead.email_sends

    return templates.TemplateResponse(
        "lead_detail.html",
        {
            "request": request,
            "lead": lead,
            "tags": tags,
            "status_history": status_history,
            "emails": emails,
            "page": "leads"
        }
    )


@router.get("/new/form", response_class=HTMLResponse)
async def new_lead_form(request: Request):
    """Show form to add a new lead manually"""
    templates = request.app.state.templates

    return templates.TemplateResponse(
        "lead_form.html",
        {
            "request": request,
            "lead": None,  # No existing lead (new)
            "page": "leads"
        }
    )


@router.post("/new")
async def create_new_lead(
    request: Request,
    name: str = Form(...),
    title: Optional[str] = Form(None),
    company: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
    source: str = Form("manual")
):
    """
    Create a new lead manually.

    Form fields:
    - name: Lead name (required)
    - title: Job title
    - company: Company name
    - email: Email address
    - phone: Phone number
    - content: Lead content (post, message, etc.)
    - url: Source URL
    - source: Source type (default: manual)
    """
    with get_db() as db:
        lead_data = {
            'name': name,
            'title': title,
            'company': company,
            'email': email,
            'phone': phone,
            'content': content,
            'url': url,
            'source': source,
            'external_id': url if url else None  # Use URL as external ID
        }

        lead = create_lead(db, lead_data)

    # Redirect to lead detail page
    return RedirectResponse(url=f"/leads/{lead.id}", status_code=303)


@router.post("/{lead_id}/analyze")
async def analyze_lead(request: Request, lead_id: int):
    """
    Analyze a lead with Claude AI.

    This endpoint triggers the AI analysis and updates the lead.
    """
    with get_db() as db:
        lead = get_lead_by_id(db, lead_id)

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        # Convert to dict for processor
        lead_dict = {
            'id': lead.id,
            'name': lead.name,
            'title': lead.title,
            'company': lead.company,
            'source': lead.source,
            'url': lead.url,
            'content': lead.content,
            'date': lead.created_at.strftime('%Y-%m-%d') if lead.created_at else None
        }

        try:
            # Run analysis with Claude
            proc = get_processor()
            result = proc.process_lead(lead_dict)

            # Save results to database
            analysis = result.get('analysis', {})
            message = result.get('message')

            save_lead_analysis(db, lead_id, analysis, message)

            # Return success response (htmx will reload page)
            return JSONResponse({
                "success": True,
                "message": "Lead analyzed successfully",
                "score": analysis.get('score'),
                "lead_id": lead_id
            })

        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": str(e)
            }, status_code=500)


@router.post("/{lead_id}/status")
async def update_status(
    request: Request,
    lead_id: int,
    status: str = Form(...),
    notes: Optional[str] = Form(None)
):
    """
    Update lead status.

    Form fields:
    - status: New status value
    - notes: Optional notes about the change
    """
    with get_db() as db:
        lead = update_lead_status(db, lead_id, status, notes)

        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

    return JSONResponse({
        "success": True,
        "message": f"Status updated to {status}",
        "status": status
    })


@router.post("/{lead_id}/tag")
async def add_tag(
    request: Request,
    lead_id: int,
    tag: str = Form(...)
):
    """Add a tag to a lead"""
    with get_db() as db:
        lead = get_lead_by_id(db, lead_id)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")

        add_tag_to_lead(db, lead_id, tag)

    return JSONResponse({
        "success": True,
        "message": f"Tag '{tag}' added"
    })


@router.delete("/{lead_id}")
async def remove_lead(request: Request, lead_id: int):
    """Delete a lead"""
    with get_db() as db:
        success = delete_lead(db, lead_id)

        if not success:
            raise HTTPException(status_code=404, detail="Lead not found")

    return JSONResponse({
        "success": True,
        "message": "Lead deleted successfully"
    })
