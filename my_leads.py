#!/usr/bin/env python3
"""
My Leads - Add your real leads here and process them

Usage: python3 my_leads.py
"""

from processors.claude_processor import LeadProcessor
from storage.storage import LeadStorage
from datetime import datetime


# ============================================================================
# ADD YOUR LEADS HERE 👇
# ============================================================================

my_leads = [
    # Template - Copy this for each new lead
    {
        'id': '1',
        'name': 'Example Person',
        'title': 'Owner',               # Owner, Director, Founder, Manager
        'company': 'Example Company',
        'source': 'LinkedIn',            # LinkedIn, IndiaMART, Twitter, Email, etc.
        'date': datetime.now().strftime('%Y-%m-%d'),
        'content': '''
        Paste their EXACT post/message here. This is what Claude analyzes.

        Look for:
        - Problems they mention (pain points)
        - Specific details (numbers, examples)
        - Urgency indicators (ASAP, urgent, crisis)
        - Their exact words (don't summarize)

        Example:
        "Managing orders from 50+ dealers is absolute chaos. Using WhatsApp
        for orders, Excel for tracking. Lost 3 orders this week because
        messages got buried. Need a proper system urgently."
        ''',
        'url': 'https://linkedin.com/posts/...'  # Source URL (optional but helpful)
    },

    # Add more leads below (copy the template above)
    # {
    #     'id': '2',
    #     'name': 'Next Person',
    #     ...
    # },
]


# ============================================================================
# PROCESSING CODE (Don't change this unless you know what you're doing)
# ============================================================================

def main():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                   MY LEADS PROCESSOR                          ║
║              Quality Lead Analysis & Outreach                 ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    if not my_leads:
        print("❌ No leads found!")
        print("\n💡 Add your leads to the my_leads list above.")
        print("   Copy the template and fill in:")
        print("   - name, title, company")
        print("   - content (their actual post/message)")
        print("   - source and URL")
        return

    print(f"📊 Found {len(my_leads)} leads to process\n")

    # Initialize processor and storage
    processor = LeadProcessor(config_dir="config")
    storage = LeadStorage(data_dir="data")

    # Save raw leads
    storage.save_raw_leads(my_leads, source="my_leads")

    # Process all leads
    print("🤖 Analyzing leads with Claude AI...\n")
    results = processor.process_batch(my_leads)

    # Save results
    print("\n💾 Saving results...")
    storage.save_processed_results(results, source="my_leads")
    storage.save_qualified_leads(results, source="my_leads")
    storage.export_messages_for_outreach(results, source="my_leads")

    # Print summary
    print("\n" + "="*60)
    print("✅ PROCESSING COMPLETE!")
    print("="*60)

    # Get stats
    stats = storage.get_stats(results)
    print(f"\n📈 RESULTS:")
    print(f"   Total processed: {stats['total']}")
    print(f"   A+ leads: {stats['a_plus']} ({stats['a_plus_pct']:.1f}%)")
    print(f"   A leads: {stats['a']} ({stats['a_pct']:.1f}%)")
    print(f"   B leads: {stats['b']} ({stats['b_pct']:.1f}%)")
    print(f"   C leads: {stats['c']} ({stats['c_pct']:.1f}%)")
    print(f"   Errors: {stats['errors']}")

    qualified = stats['a_plus'] + stats['a']
    print(f"\n⭐ {qualified} QUALIFIED LEADS ready for outreach!")

    if qualified > 0:
        print(f"\n📧 Check these files:")
        print(f"   • data/qualified/qualified_my_leads_*.csv  (spreadsheet)")
        print(f"   • data/messages/batch_my_leads_*/  (ready-to-send messages)")
        print(f"\n💡 Open the .txt files in data/messages/ and start sending!")
    else:
        print(f"\n💡 No qualified leads this time. Try:")
        print(f"   • Look for leads with more specific pain points")
        print(f"   • Ensure they're decision makers (Owner, Director)")
        print(f"   • Check that content has urgency indicators")

    print("\n" + "="*60)
    print("🎯 Next steps:")
    print("   1. Review qualified leads in data/qualified/")
    print("   2. Open message files in data/messages/")
    print("   3. Customize messages slightly if needed")
    print("   4. Send to LinkedIn/Email")
    print("   5. Track responses!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
