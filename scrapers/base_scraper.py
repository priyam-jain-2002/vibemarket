"""
Base Scraper Abstract Class

Defines the interface for all lead scrapers
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import time
import random


class BaseScraper(ABC):
    """Abstract base class for lead scrapers"""

    def __init__(self):
        self.leads_found = []
        self.session_id = None

    @abstractmethod
    def login(self, email: str, password: str) -> bool:
        """
        Login to the platform
        Returns True if successful
        """
        pass

    @abstractmethod
    def search_posts(self, query: str, limit: int = 50, **filters) -> List[Dict]:
        """
        Search for posts matching query

        Args:
            query: Search keywords
            limit: Max number of posts to find
            **filters: Platform-specific filters (date, location, industry, etc.)

        Returns:
            List of lead dicts with: name, title, company, content, url, source
        """
        pass

    @abstractmethod
    def enrich_lead(self, lead: Dict) -> Dict:
        """
        Enrich lead with additional profile/company data

        Args:
            lead: Basic lead dict from search

        Returns:
            Enhanced lead dict with more context
        """
        pass

    def human_delay(self, min_seconds: float = 3.0, max_seconds: float = 8.0):
        """
        Random delay to mimic human behavior
        Avoids detection as bot
        """
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    def close(self):
        """Cleanup resources (browser, sessions, etc.)"""
        pass
