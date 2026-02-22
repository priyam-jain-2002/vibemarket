"""
Database operations for Vibe-Leads.

This module provides CRUD operations and database utilities.
Keeps things simple for personal use while maintaining good practices.
"""

import os
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
from sqlalchemy import func, desc, and_, or_
from sqlalchemy.orm import Session

from storage.models import (
    init_db,
    Lead,
    LeadStatusHistory,
    EmailSend,
    ScraperSession,
    LeadTag
)


# Global session factory (initialized on first use)
_SessionLocal = None
_engine = None


def get_session_factory():
    """Get or create session factory"""
    global _SessionLocal, _engine
    if _SessionLocal is None:
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        _engine, _SessionLocal = init_db('sqlite:///data/vibe-leads.db')
    return _SessionLocal


@contextmanager
def get_db():
    """
    Context manager for database sessions.

    Usage:
        with get_db() as db:
            lead = db.query(Lead).first()
    """
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ============================================================================
# LEAD OPERATIONS
# ============================================================================

def create_lead(db: Session, lead_data: Dict[str, Any]) -> Lead:
    """
    Create a new lead in the database.

    Args:
        db: Database session
        lead_data: Dictionary with lead information

    Returns:
        Created Lead object
    """
    lead = Lead(**lead_data)
    db.add(lead)
    db.flush()  # Get the ID without committing

    # Create initial status history entry
    history = LeadStatusHistory(
        lead_id=lead.id,
        old_status=None,
        new_status='new',
        notes='Lead created'
    )
    db.add(history)
    db.commit()
    db.refresh(lead)
    return lead


def get_lead_by_id(db: Session, lead_id: int) -> Optional[Lead]:
    """Get a lead by ID"""
    return db.query(Lead).filter(Lead.id == lead_id).first()


def get_lead_by_external_id(db: Session, external_id: str) -> Optional[Lead]:
    """Get a lead by external ID (URL, LinkedIn post ID, etc.)"""
    return db.query(Lead).filter(Lead.external_id == external_id).first()


def get_all_leads(db: Session, limit: int = 100, offset: int = 0,
                  filters: Optional[Dict] = None) -> List[Lead]:
    """
    Get leads with optional filtering.

    Args:
        db: Database session
        limit: Max number of results
        offset: Skip this many results
        filters: Optional filters dict with keys:
            - score: Filter by score ('A+', 'A', 'B', 'C')
            - status: Filter by status
            - source: Filter by source
            - search: Search in name, company, content
            - date_from: Created after this date
            - date_to: Created before this date

    Returns:
        List of Lead objects
    """
    query = db.query(Lead)

    if filters:
        if 'score' in filters and filters['score']:
            query = query.filter(Lead.score == filters['score'])

        if 'status' in filters and filters['status']:
            query = query.filter(Lead.status == filters['status'])

        if 'source' in filters and filters['source']:
            query = query.filter(Lead.source == filters['source'])

        if 'search' in filters and filters['search']:
            search_term = f"%{filters['search']}%"
            query = query.filter(
                or_(
                    Lead.name.like(search_term),
                    Lead.company.like(search_term),
                    Lead.content.like(search_term)
                )
            )

        if 'date_from' in filters and filters['date_from']:
            query = query.filter(Lead.created_at >= filters['date_from'])

        if 'date_to' in filters and filters['date_to']:
            query = query.filter(Lead.created_at <= filters['date_to'])

    # Order by most recent first
    query = query.order_by(desc(Lead.created_at))

    return query.offset(offset).limit(limit).all()


def count_leads(db: Session, filters: Optional[Dict] = None) -> int:
    """Count leads with optional filters (same filters as get_all_leads)"""
    query = db.query(func.count(Lead.id))

    if filters:
        if 'score' in filters and filters['score']:
            query = query.filter(Lead.score == filters['score'])
        if 'status' in filters and filters['status']:
            query = query.filter(Lead.status == filters['status'])
        if 'source' in filters and filters['source']:
            query = query.filter(Lead.source == filters['source'])
        if 'search' in filters and filters['search']:
            search_term = f"%{filters['search']}%"
            query = query.filter(
                or_(
                    Lead.name.like(search_term),
                    Lead.company.like(search_term),
                    Lead.content.like(search_term)
                )
            )
        if 'date_from' in filters and filters['date_from']:
            query = query.filter(Lead.created_at >= filters['date_from'])
        if 'date_to' in filters and filters['date_to']:
            query = query.filter(Lead.created_at <= filters['date_to'])

    return query.scalar()


def update_lead(db: Session, lead_id: int, update_data: Dict[str, Any]) -> Optional[Lead]:
    """Update a lead's information"""
    lead = get_lead_by_id(db, lead_id)
    if not lead:
        return None

    for key, value in update_data.items():
        if hasattr(lead, key):
            setattr(lead, key, value)

    db.commit()
    db.refresh(lead)
    return lead


def update_lead_status(db: Session, lead_id: int, new_status: str, notes: Optional[str] = None) -> Optional[Lead]:
    """
    Update lead status and log the change.

    Args:
        db: Database session
        lead_id: Lead ID
        new_status: New status value
        notes: Optional notes about the status change

    Returns:
        Updated Lead object or None if not found
    """
    lead = get_lead_by_id(db, lead_id)
    if not lead:
        return None

    old_status = lead.status
    lead.status = new_status

    # Update relevant timestamps
    if new_status == 'analyzed' and not lead.analyzed_at:
        lead.analyzed_at = datetime.utcnow()
    elif new_status == 'contacted' and not lead.contacted_at:
        lead.contacted_at = datetime.utcnow()
    elif new_status == 'replied' and not lead.replied_at:
        lead.replied_at = datetime.utcnow()
    elif new_status == 'won' and not lead.won_at:
        lead.won_at = datetime.utcnow()
    elif new_status == 'lost' and not lead.lost_at:
        lead.lost_at = datetime.utcnow()

    # Log status change
    history = LeadStatusHistory(
        lead_id=lead_id,
        old_status=old_status,
        new_status=new_status,
        notes=notes or f"Status changed from {old_status} to {new_status}"
    )
    db.add(history)

    db.commit()
    db.refresh(lead)
    return lead


def save_lead_analysis(db: Session, lead_id: int, analysis: Dict[str, Any], message: Optional[str] = None):
    """
    Save Claude AI analysis results to a lead.

    Args:
        db: Database session
        lead_id: Lead ID
        analysis: Analysis dict from LeadProcessor
        message: Generated outreach message
    """
    lead = get_lead_by_id(db, lead_id)
    if not lead:
        return None

    # Update lead with analysis
    lead.score = analysis.get('score')
    lead.pain_points = analysis.get('pain_points')
    lead.pain_clarity = analysis.get('pain_clarity')
    lead.urgency = analysis.get('urgency')
    lead.authority = analysis.get('authority')
    lead.specificity_score = analysis.get('specificity_score')
    lead.industry_fit = analysis.get('industry_fit')
    lead.size_fit = analysis.get('size_fit')
    lead.analysis_raw = analysis
    lead.outreach_message = message
    lead.analyzed_at = datetime.utcnow()

    # Update status to 'analyzed'
    if lead.status == 'new':
        update_lead_status(db, lead_id, 'analyzed', notes='Lead analyzed by Claude AI')
    else:
        db.commit()

    db.refresh(lead)
    return lead


def delete_lead(db: Session, lead_id: int) -> bool:
    """Delete a lead (cascades to history, emails, tags)"""
    lead = get_lead_by_id(db, lead_id)
    if not lead:
        return False

    db.delete(lead)
    db.commit()
    return True


# ============================================================================
# EMAIL OPERATIONS
# ============================================================================

def log_email_send(db: Session, lead_id: int, subject: str, body: str,
                   email_to: Optional[str] = None, email_from: Optional[str] = None) -> EmailSend:
    """Log an email send to a lead"""
    email = EmailSend(
        lead_id=lead_id,
        subject=subject,
        body=body,
        email_to=email_to,
        email_from=email_from
    )
    db.add(email)

    # Update lead status to 'contacted' if not already
    lead = get_lead_by_id(db, lead_id)
    if lead and lead.status in ['new', 'analyzed']:
        update_lead_status(db, lead_id, 'contacted', notes='Email sent')
    else:
        db.commit()

    db.refresh(email)
    return email


def mark_email_replied(db: Session, email_id: int, reply_content: Optional[str] = None) -> Optional[EmailSend]:
    """Mark an email as replied"""
    email = db.query(EmailSend).filter(EmailSend.id == email_id).first()
    if not email:
        return None

    email.replied = True
    email.replied_at = datetime.utcnow()
    email.reply_content = reply_content

    # Update lead status to 'replied'
    update_lead_status(db, email.lead_id, 'replied', notes='Lead replied to email')

    db.commit()
    db.refresh(email)
    return email


def get_emails_for_lead(db: Session, lead_id: int) -> List[EmailSend]:
    """Get all emails sent to a lead"""
    return db.query(EmailSend).filter(EmailSend.lead_id == lead_id).order_by(EmailSend.sent_at).all()


# ============================================================================
# SCRAPER SESSION OPERATIONS
# ============================================================================

def create_scraper_session(db: Session, source: str, search_query: Optional[str] = None,
                          config_snapshot: Optional[Dict] = None) -> ScraperSession:
    """Create a new scraper session"""
    session = ScraperSession(
        source=source,
        search_query=search_query,
        config_snapshot=config_snapshot
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def update_scraper_session(db: Session, session_id: int, update_data: Dict[str, Any]) -> Optional[ScraperSession]:
    """Update scraper session (for progress tracking)"""
    session = db.query(ScraperSession).filter(ScraperSession.id == session_id).first()
    if not session:
        return None

    for key, value in update_data.items():
        if hasattr(session, key):
            setattr(session, key, value)

    db.commit()
    db.refresh(session)
    return session


def complete_scraper_session(db: Session, session_id: int, status: str = 'completed',
                             error_message: Optional[str] = None) -> Optional[ScraperSession]:
    """Mark a scraper session as complete"""
    session = db.query(ScraperSession).filter(ScraperSession.id == session_id).first()
    if not session:
        return None

    session.completed_at = datetime.utcnow()
    session.status = status
    if error_message:
        session.error_message = error_message

    db.commit()
    db.refresh(session)
    return session


def get_recent_scraper_sessions(db: Session, limit: int = 10) -> List[ScraperSession]:
    """Get recent scraper sessions"""
    return db.query(ScraperSession).order_by(desc(ScraperSession.started_at)).limit(limit).all()


# ============================================================================
# TAG OPERATIONS
# ============================================================================

def add_tag_to_lead(db: Session, lead_id: int, tag: str) -> LeadTag:
    """Add a tag to a lead"""
    # Check if tag already exists
    existing = db.query(LeadTag).filter(
        and_(LeadTag.lead_id == lead_id, LeadTag.tag == tag)
    ).first()

    if existing:
        return existing

    lead_tag = LeadTag(lead_id=lead_id, tag=tag)
    db.add(lead_tag)
    db.commit()
    db.refresh(lead_tag)
    return lead_tag


def remove_tag_from_lead(db: Session, lead_id: int, tag: str) -> bool:
    """Remove a tag from a lead"""
    lead_tag = db.query(LeadTag).filter(
        and_(LeadTag.lead_id == lead_id, LeadTag.tag == tag)
    ).first()

    if not lead_tag:
        return False

    db.delete(lead_tag)
    db.commit()
    return True


def get_tags_for_lead(db: Session, lead_id: int) -> List[str]:
    """Get all tags for a lead"""
    tags = db.query(LeadTag).filter(LeadTag.lead_id == lead_id).all()
    return [tag.tag for tag in tags]


# ============================================================================
# ANALYTICS / STATS
# ============================================================================

def get_dashboard_stats(db: Session, days: int = 30) -> Dict[str, Any]:
    """
    Get dashboard statistics.

    Args:
        db: Database session
        days: Number of days to look back

    Returns:
        Dictionary with key metrics
    """
    date_cutoff = datetime.utcnow() - timedelta(days=days)

    # Total leads
    total_leads = db.query(func.count(Lead.id)).scalar()

    # Leads created in time period
    recent_leads = db.query(func.count(Lead.id)).filter(
        Lead.created_at >= date_cutoff
    ).scalar()

    # Analyzed today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    analyzed_today = db.query(func.count(Lead.id)).filter(
        Lead.analyzed_at >= today_start
    ).scalar()

    # Qualified leads (A+ and A)
    qualified_leads = db.query(func.count(Lead.id)).filter(
        Lead.score.in_(['A+', 'A'])
    ).scalar()

    # Contacted this week
    week_start = datetime.utcnow() - timedelta(days=7)
    contacted_this_week = db.query(func.count(Lead.id)).filter(
        Lead.contacted_at >= week_start
    ).scalar()

    # Replied leads
    replied_leads = db.query(func.count(Lead.id)).filter(
        Lead.status == 'replied'
    ).scalar()

    # Won leads
    won_leads = db.query(func.count(Lead.id)).filter(
        Lead.status == 'won'
    ).scalar()

    # Score distribution
    score_distribution = {}
    for score in ['A+', 'A', 'B', 'C']:
        count = db.query(func.count(Lead.id)).filter(Lead.score == score).scalar()
        score_distribution[score] = count

    # Source distribution
    source_results = db.query(
        Lead.source,
        func.count(Lead.id).label('count')
    ).group_by(Lead.source).all()
    source_distribution = {source: count for source, count in source_results}

    # Reply rate (if any contacted)
    contacted_total = db.query(func.count(Lead.id)).filter(
        Lead.contacted_at.isnot(None)
    ).scalar()
    reply_rate = (replied_leads / contacted_total * 100) if contacted_total > 0 else 0

    return {
        'total_leads': total_leads,
        'recent_leads': recent_leads,
        'analyzed_today': analyzed_today,
        'qualified_leads': qualified_leads,
        'contacted_this_week': contacted_this_week,
        'replied_leads': replied_leads,
        'won_leads': won_leads,
        'reply_rate': round(reply_rate, 1),
        'score_distribution': score_distribution,
        'source_distribution': source_distribution,
    }


def get_conversion_funnel(db: Session) -> Dict[str, int]:
    """Get conversion funnel metrics"""
    return {
        'new': db.query(func.count(Lead.id)).filter(Lead.status == 'new').scalar(),
        'analyzed': db.query(func.count(Lead.id)).filter(Lead.status == 'analyzed').scalar(),
        'contacted': db.query(func.count(Lead.id)).filter(Lead.status == 'contacted').scalar(),
        'replied': db.query(func.count(Lead.id)).filter(Lead.status == 'replied').scalar(),
        'won': db.query(func.count(Lead.id)).filter(Lead.status == 'won').scalar(),
    }


if __name__ == '__main__':
    # Test database operations
    print("Testing database operations...")

    with get_db() as db:
        # Create a test lead
        lead_data = {
            'name': 'Test Kumar',
            'title': 'Owner',
            'company': 'Test Industries',
            'source': 'manual',
            'content': 'Looking for order management solution...',
            'external_id': 'test-123'
        }

        lead = create_lead(db, lead_data)
        print(f"✅ Created lead: {lead}")

        # Get stats
        stats = get_dashboard_stats(db)
        print(f"✅ Dashboard stats: {stats}")

        print("\n✨ Database operations working correctly!")
