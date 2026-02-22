"""
SQLAlchemy models for Vibe-Leads database.

This module defines the database schema for leads, analytics, and tracking.
Uses SQLite for simplicity (perfect for personal use).
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Lead(Base):
    """
    Main lead table - stores all lead information and analysis results.
    """
    __tablename__ = 'leads'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Unique identifier (URL or external ID)
    external_id = Column(String(500), unique=True, nullable=True, index=True)

    # Lead basic info
    name = Column(String(200), nullable=False)
    title = Column(String(200), nullable=True)
    company = Column(String(200), nullable=True)
    email = Column(String(200), nullable=True)
    phone = Column(String(50), nullable=True)
    location = Column(String(200), nullable=True)

    # Source information
    source = Column(String(50), nullable=False, index=True)  # 'linkedin', 'manual', 'twitter', etc.
    url = Column(Text, nullable=True)  # Source URL (LinkedIn post, etc.)

    # Content
    content = Column(Text, nullable=True)  # Original post/content that contains pain points

    # AI Analysis results
    score = Column(String(10), nullable=True, index=True)  # 'A+', 'A', 'B', 'C'
    pain_points = Column(JSON, nullable=True)  # List of detected pain points
    pain_clarity = Column(String(20), nullable=True)  # 'EXPLICIT', 'IMPLICIT', 'NONE'
    urgency = Column(String(20), nullable=True)  # 'HIGH', 'MEDIUM', 'LOW', 'NONE'
    authority = Column(String(50), nullable=True)  # 'DECISION_MAKER', 'INFLUENCER', 'UNKNOWN', 'LOW'
    specificity_score = Column(Integer, nullable=True)  # 1-10
    industry_fit = Column(Boolean, nullable=True)
    size_fit = Column(Boolean, nullable=True)

    # Full analysis JSON (for reference)
    analysis_raw = Column(JSON, nullable=True)

    # Generated outreach message
    outreach_message = Column(Text, nullable=True)

    # Lead lifecycle status
    status = Column(String(50), default='new', index=True)
    # Possible values: 'new', 'analyzed', 'contacted', 'replied', 'won', 'lost', 'archived'

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    analyzed_at = Column(DateTime, nullable=True)
    contacted_at = Column(DateTime, nullable=True)
    replied_at = Column(DateTime, nullable=True)
    won_at = Column(DateTime, nullable=True)
    lost_at = Column(DateTime, nullable=True)

    # Relationships
    status_history = relationship("LeadStatusHistory", back_populates="lead", cascade="all, delete-orphan")
    email_sends = relationship("EmailSend", back_populates="lead", cascade="all, delete-orphan")
    tags = relationship("LeadTag", back_populates="lead", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Lead(id={self.id}, name='{self.name}', score='{self.score}', status='{self.status}')>"

    def to_dict(self):
        """Convert lead to dictionary (for JSON serialization)"""
        return {
            'id': self.id,
            'external_id': self.external_id,
            'name': self.name,
            'title': self.title,
            'company': self.company,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'source': self.source,
            'url': self.url,
            'content': self.content,
            'score': self.score,
            'pain_points': self.pain_points,
            'pain_clarity': self.pain_clarity,
            'urgency': self.urgency,
            'authority': self.authority,
            'specificity_score': self.specificity_score,
            'outreach_message': self.outreach_message,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'analyzed_at': self.analyzed_at.isoformat() if self.analyzed_at else None,
            'contacted_at': self.contacted_at.isoformat() if self.contacted_at else None,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None,
        }


class LeadStatusHistory(Base):
    """
    Tracks all status changes for leads (audit trail).
    """
    __tablename__ = 'lead_status_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey('leads.id', ondelete='CASCADE'), nullable=False, index=True)

    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(Text, nullable=True)

    # Relationships
    lead = relationship("Lead", back_populates="status_history")

    def __repr__(self):
        return f"<LeadStatusHistory(lead_id={self.lead_id}, {self.old_status} → {self.new_status})>"


class EmailSend(Base):
    """
    Tracks all emails sent to leads.
    """
    __tablename__ = 'email_sends'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey('leads.id', ondelete='CASCADE'), nullable=False, index=True)

    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Email tracking
    opened = Column(Boolean, default=False)
    replied = Column(Boolean, default=False)
    replied_at = Column(DateTime, nullable=True)
    reply_content = Column(Text, nullable=True)

    # Email metadata
    email_to = Column(String(200), nullable=True)
    email_from = Column(String(200), nullable=True)

    # Relationships
    lead = relationship("Lead", back_populates="email_sends")

    def __repr__(self):
        return f"<EmailSend(id={self.id}, lead_id={self.lead_id}, sent_at={self.sent_at})>"


class ScraperSession(Base):
    """
    Tracks scraping sessions (for monitoring and debugging).
    """
    __tablename__ = 'scraper_sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)

    source = Column(String(50), nullable=False, index=True)  # 'linkedin', 'twitter', etc.
    search_query = Column(String(500), nullable=True)

    # Results
    leads_found = Column(Integer, default=0)
    leads_imported = Column(Integer, default=0)
    leads_duplicates = Column(Integer, default=0)

    # Timing
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True)

    # Status
    status = Column(String(50), default='running', index=True)  # 'running', 'completed', 'failed', 'cancelled'
    error_message = Column(Text, nullable=True)

    # Configuration snapshot (for reproducibility)
    config_snapshot = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<ScraperSession(id={self.id}, source='{self.source}', status='{self.status}')>"

    @property
    def duration_seconds(self):
        """Calculate session duration"""
        if self.completed_at and self.started_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


class LeadTag(Base):
    """
    Tags for organizing and filtering leads.
    """
    __tablename__ = 'lead_tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey('leads.id', ondelete='CASCADE'), nullable=False, index=True)

    tag = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    lead = relationship("Lead", back_populates="tags")

    def __repr__(self):
        return f"<LeadTag(lead_id={self.lead_id}, tag='{self.tag}')>"


# Database initialization helper
def init_db(database_url='sqlite:///data/vibe-leads.db'):
    """
    Initialize the database - create all tables.

    Args:
        database_url: SQLAlchemy database URL

    Returns:
        engine, sessionmaker
    """
    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return engine, SessionLocal


if __name__ == '__main__':
    # Test: Create database
    print("Creating database schema...")
    engine, SessionLocal = init_db('sqlite:///data/vibe-leads.db')
    print("✅ Database schema created successfully!")
    print(f"Tables: {', '.join(Base.metadata.tables.keys())}")
