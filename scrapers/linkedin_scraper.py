"""
LinkedIn Lead Scraper

Uses Playwright to automate LinkedIn search and lead extraction.

IMPORTANT DISCLAIMERS:
- Use your own LinkedIn account credentials
- Only scrapes publicly visible posts
- Respects rate limits to avoid detection
- User assumes all responsibility for ToS compliance
- LinkedIn may detect and restrict automated access

Recommended Usage:
- Max 50 leads per session
- Run once per day
- Use human-like delays (3-8 seconds)
- Don't run 24/7
"""

import os
import re
from typing import List, Dict, Optional
from datetime import datetime
from scrapers.base_scraper import BaseScraper


class LinkedInScraper(BaseScraper):
    """LinkedIn scraper using Playwright for stealth"""

    def __init__(self, headless: bool = False):
        """
        Initialize LinkedIn scraper

        Args:
            headless: Run browser in headless mode (default: False for better stealth)
        """
        super().__init__()
        self.headless = headless
        self.browser = None
        self.page = None
        self.logged_in = False

    def login(self, email: str, password: str) -> bool:
        """
        Login to LinkedIn

        Args:
            email: LinkedIn email
            password: LinkedIn password

        Returns:
            True if login successful
        """
        try:
            from playwright.sync_api import sync_playwright

            self.playwright = sync_playwright().start()

            # Launch browser with stealth settings
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                ]
            )

            # Create context with realistic user agent
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='America/New_York',
            )

            self.page = self.context.new_page()

            # Add stealth scripts
            self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            print("🔐 Logging into LinkedIn...")
            self.page.goto('https://www.linkedin.com/login', timeout=30000)
            self.human_delay(2, 4)

            # Fill login form
            self.page.fill('input[name="session_key"]', email)
            self.human_delay(0.5, 1.5)
            self.page.fill('input[name="session_password"]', password)
            self.human_delay(0.5, 1.5)

            # Click login
            self.page.click('button[type="submit"]')
            self.human_delay(5, 8)

            # Check if login successful
            if 'feed' in self.page.url or 'checkpoint' in self.page.url:
                print("✅ Login successful!")
                self.logged_in = True
                return True
            else:
                print("❌ Login failed - check credentials")
                return False

        except ImportError:
            print("❌ Playwright not installed. Run: pip install playwright && playwright install chromium")
            return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def search_posts(self, query: str, limit: int = 50, **filters) -> List[Dict]:
        """
        Search LinkedIn posts for keywords

        Args:
            query: Search query (e.g., "order management chaos")
            limit: Max posts to scrape (default: 50)
            **filters: Optional filters (not implemented yet)

        Returns:
            List of lead dicts
        """
        if not self.logged_in:
            raise ValueError("Must login first. Call login() before searching.")

        print(f"\n🔍 Searching LinkedIn for: '{query}'")
        print(f"   Target: {limit} leads")

        leads = []

        try:
            # Navigate to search (posts filter)
            search_url = f"https://www.linkedin.com/search/results/content/?keywords={query.replace(' ', '%20')}"
            self.page.goto(search_url, timeout=30000)
            self.human_delay(4, 7)

            # Scroll to load more posts
            scroll_count = min(limit // 10 + 1, 10)  # Max 10 scrolls
            for i in range(scroll_count):
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                self.human_delay(2, 4)
                print(f"   📜 Scrolling... ({i+1}/{scroll_count})")

            # Extract posts
            posts = self.page.query_selector_all('.feed-shared-update-v2')
            print(f"   Found {len(posts)} posts on page")

            for idx, post in enumerate(posts[:limit]):
                try:
                    # Extract post data
                    lead = self._extract_post_data(post)
                    if lead:
                        leads.append(lead)
                        print(f"   ✅ Lead {len(leads)}: {lead['name']} - {lead['company']}")

                    self.human_delay(1, 3)

                except Exception as e:
                    print(f"   ⚠️  Error extracting post {idx}: {e}")
                    continue

                if len(leads) >= limit:
                    break

            print(f"\n✅ Scraped {len(leads)} leads")
            self.leads_found = leads
            return leads

        except Exception as e:
            print(f"❌ Search error: {e}")
            return leads

    def _extract_post_data(self, post_element) -> Optional[Dict]:
        """
        Extract lead data from a post element

        Returns:
            Lead dict or None if extraction fails
        """
        try:
            # Name
            name_elem = post_element.query_selector('.feed-shared-actor__name')
            name = name_elem.inner_text().strip() if name_elem else 'Unknown'

            # Title
            title_elem = post_element.query_selector('.feed-shared-actor__description')
            title = title_elem.inner_text().strip() if title_elem else 'Unknown'

            # Extract company from title (often in format "Title at Company")
            company = 'Unknown'
            if ' at ' in title:
                parts = title.split(' at ')
                title = parts[0].strip()
                company = parts[1].strip()
            elif ' @ ' in title:
                parts = title.split(' @ ')
                title = parts[0].strip()
                company = parts[1].strip()

            # Post content
            content_elem = post_element.query_selector('.feed-shared-text')
            content = content_elem.inner_text().strip() if content_elem else ''

            # Post URL
            link_elem = post_element.query_selector('.feed-shared-actor__container-link')
            profile_url = link_elem.get_attribute('href') if link_elem else ''

            # Only include posts with actual content
            if not content or len(content) < 50:
                return None

            return {
                'id': f"linkedin_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.leads_found)}",
                'name': name,
                'title': title,
                'company': company,
                'source': 'LinkedIn',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'content': content,
                'url': profile_url,
            }

        except Exception as e:
            return None

    def enrich_lead(self, lead: Dict) -> Dict:
        """
        Enrich lead with profile data

        Args:
            lead: Basic lead from search

        Returns:
            Enhanced lead with more context
        """
        # TODO: Visit profile page and extract:
        # - Company size
        # - Industry
        # - Location
        # - Recent activity

        # For now, just return the lead as-is
        # This avoids extra page loads and detection risk
        return lead

    def close(self):
        """Close browser and cleanup"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()

        print("🔒 Browser closed")


if __name__ == "__main__":
    # Example usage
    scraper = LinkedInScraper(headless=False)

    # Login (use env vars for security)
    email = os.getenv('LINKEDIN_EMAIL', '')
    password = os.getenv('LINKEDIN_PASSWORD', '')

    if not email or not password:
        print("Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env")
        exit(1)

    if scraper.login(email, password):
        # Search for leads
        leads = scraper.search_posts(
            query="order management chaos India",
            limit=10
        )

        # Print results
        print(f"\n📊 Found {len(leads)} leads:")
        for lead in leads:
            print(f"  - {lead['name']} ({lead['title']} at {lead['company']})")

        scraper.close()
