import requests
import urllib.parse
from typing import List, Dict, Optional
from datetime import datetime
from scrapers.base_scraper import BaseScraper
import time
import random

class RedditScraper(BaseScraper):
    """Reddit scraper using public search JSON API"""

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        # Use a custom user agent to prevent instant blocking
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.leads_found = []

    def login(self, username: str = "", password: str = "") -> bool:
        """Reddit public search doesn't require login"""
        return True

    def search_posts(self, query: str, limit: int = 50, **filters) -> List[Dict]:
        """
        Search Reddit for keywords

        Args:
            query: Search query (e.g., "order management chaos")
            limit: Max posts to scrape (default: 50)

        Returns:
            List of lead dicts
        """
        print(f"\n🔍 Searching Reddit for: '{query}'")
        print(f"   Target: {limit} leads")

        leads = []
        encoded_query = urllib.parse.quote(query)
        
        # We can search specific subs or globally. For this we will search globally.
        url = f"https://www.reddit.com/search.json?q={encoded_query}&sort=new&limit={limit}"

        try:
            self.human_delay(1, 3) # Be polite
            response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ Reddit API returned status {response.status_code}")
                return leads

            data = response.json()
            
            # Navigate Reddit's JSON structure
            posts = data.get('data', {}).get('children', [])
            print(f"   Found {len(posts)} posts in search results")

            for idx, post_wrapper in enumerate(posts[:limit]):
                try:
                    post_data = post_wrapper.get('data', {})
                    lead = self._extract_post_data(post_data)
                    
                    if lead:
                        leads.append(lead)
                        print(f"   ✅ Lead {len(leads)}: u/{lead['name']} - r/{post_data.get('subreddit', 'Unknown')}")
                        
                    if len(leads) >= limit:
                        break

                except Exception as e:
                    print(f"   ⚠️  Error extracting post {idx}: {e}")
                    continue

            print(f"\n✅ Scraped {len(leads)} leads from Reddit")
            self.leads_found.extend(leads)
            return leads

        except Exception as e:
            print(f"❌ Reddit Search error: {e}")
            return leads

    def _extract_post_data(self, post_data: dict) -> Optional[Dict]:
        """
        Extract lead data from a Reddit post object

        Returns:
            Lead dict or None if extraction fails
        """
        try:
            author = post_data.get('author', 'Unknown')
            subreddit = post_data.get('subreddit', 'Unknown')
            title = post_data.get('title', '')
            selftext = post_data.get('selftext', '')
            permalink = post_data.get('permalink', '')
            created_utc = post_data.get('created_utc', time.time())
            
            # Combine title and body for the analysis content
            full_content = f"{title}\n\n{selftext}".strip()

            # Ignore empty posts, removed posts, or very short posts
            if not full_content or full_content in ['[removed]', '[deleted]'] or len(full_content) < 50:
                return None

            profile_url = f"https://www.reddit.com{permalink}"

            return {
                'id': f"reddit_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.leads_found)}",
                'name': author,
                'title': f"Author on r/{subreddit}",
                'company': 'Unknown (Reddit)',
                'source': 'Reddit',
                'date': datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d'),
                'content': full_content,
                'url': profile_url,
            }

        except Exception as e:
            return None

    def enrich_lead(self, lead: Dict) -> Dict:
        """Enrich lead data (stub)"""
        return lead

    def close(self):
        """Cleanup network resources"""
        if self.session:
            self.session.close()
        print("🔒 Reddit Scraper closed")


if __name__ == "__main__":
    scraper = RedditScraper()
    leads = scraper.search_posts("inventory management chaos", limit=5)
    print(f"\n📊 Found {len(leads)} leads:")
    for lead in leads:
        print(f"  - {lead['name']} ({lead['title']})")
        print(f"    URL: {lead['url']}")
        print(f"    Snippet: {lead['content'][:100]}...\n")
    scraper.close()
