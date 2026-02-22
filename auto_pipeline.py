"""
Automated Lead Generation Pipeline

Complete automation loop:
1. Find leads (LinkedIn scraper)
2. Get backgrounds (enrich profile data)
3. Analyze with AI (quality scoring)
4. Generate personalized messages

Usage:
    python3 auto_pipeline.py

Configuration:
    Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env
"""

import os
import sys
from datetime import datetime
from scrapers.linkedin_scraper import LinkedInScraper
from processors.claude_processor import LeadProcessor
from storage.storage import LeadStorage


def main():
    print("=" * 80)
    print("🤖 AUTOMATED LEAD GENERATION PIPELINE")
    print("=" * 80)
    print()

    # Configuration
    SEARCH_QUERY = os.getenv('LEAD_SEARCH_QUERY', 'order management chaos India')
    LEAD_LIMIT = int(os.getenv('LEAD_LIMIT', '20'))
    LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL', '')
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD', '')

    if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
        print("❌ Missing LinkedIn credentials!")
        print("   Add to .env:")
        print("   LINKEDIN_EMAIL=your-email@example.com")
        print("   LINKEDIN_PASSWORD=your-password")
        print()
        sys.exit(1)

    # Initialize components
    scraper = LinkedInScraper(headless=False)  # headless=True to hide browser
    processor = LeadProcessor(config_dir="config")
    storage = LeadStorage(data_dir="data")

    try:
        # =====================================================================
        # STEP 1: FIND LEADS
        # =====================================================================
        print("📍 STEP 1: FINDING LEADS")
        print(f"   Query: {SEARCH_QUERY}")
        print(f"   Limit: {LEAD_LIMIT}")
        print()

        if not scraper.login(LINKEDIN_EMAIL, LINKEDIN_PASSWORD):
            print("❌ Login failed. Exiting.")
            return

        leads = scraper.search_posts(query=SEARCH_QUERY, limit=LEAD_LIMIT)

        if not leads:
            print("⚠️  No leads found. Try different keywords.")
            return

        print(f"✅ Found {len(leads)} leads")
        print()

        # Save raw leads
        raw_filename = storage.save_raw_leads(leads, source="linkedin_auto")
        print(f"💾 Saved raw leads: {raw_filename}")
        print()

        # =====================================================================
        # STEP 2: ENRICH BACKGROUNDS (Optional - currently minimal)
        # =====================================================================
        print("📍 STEP 2: ENRICHING LEAD BACKGROUNDS")
        print("   (Skipping for now to avoid extra page loads)")
        print()

        # enriched_leads = [scraper.enrich_lead(lead) for lead in leads]

        # =====================================================================
        # STEP 3: AI ANALYSIS
        # =====================================================================
        print("📍 STEP 3: AI ANALYSIS & QUALIFICATION")
        print()

        results = processor.process_batch(leads)

        # =====================================================================
        # STEP 4: SAVE RESULTS
        # =====================================================================
        print("\n📍 STEP 4: SAVING RESULTS")
        print()

        # Save processed results
        processed_filename = storage.save_processed_results(results)
        print(f"💾 Processed: {processed_filename}")

        # Save qualified leads
        qualified = [r for r in results if r['analysis'].get('score') in ['A+', 'A']]
        if qualified:
            json_file, csv_file = storage.save_qualified_leads(results)
            print(f"💾 Qualified: {json_file}")
            print(f"💾 CSV: {csv_file}")

            # Export messages
            message_dir = storage.export_messages_for_outreach(results)
            print(f"💾 Messages: {message_dir}")
        else:
            print("⚠️  No qualified leads (A+/A)")

        # =====================================================================
        # FINAL SUMMARY
        # =====================================================================
        print("\n" + "=" * 80)
        print("🎯 PIPELINE COMPLETE")
        print("=" * 80)

        stats = {
            'found': len(leads),
            'a_plus': sum(1 for r in results if r['analysis'].get('score') == 'A+'),
            'a': sum(1 for r in results if r['analysis'].get('score') == 'A'),
            'b': sum(1 for r in results if r['analysis'].get('score') == 'B'),
            'c': sum(1 for r in results if r['analysis'].get('score') == 'C'),
            'error': sum(1 for r in results if r['analysis'].get('score') == 'ERROR'),
        }

        print(f"Leads found: {stats['found']}")
        print(f"Qualified (A+/A): {stats['a_plus'] + stats['a']}")
        print(f"  - A+ leads: {stats['a_plus']}")
        print(f"  - A leads: {stats['a']}")
        print(f"Not qualified (B/C): {stats['b'] + stats['c']}")
        print()
        print("✅ Check 'data/messages/' for outreach-ready messages!")
        print("=" * 80)

    except KeyboardInterrupt:
        print("\n⚠️  Pipeline interrupted by user")

    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cleanup
        scraper.close()
        print("\n🔒 Cleanup complete")


if __name__ == "__main__":
    main()
