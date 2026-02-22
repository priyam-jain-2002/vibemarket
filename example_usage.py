"""
Example: Process Leads from Manual Collection
This shows how to use vibe-leads with manually collected leads
"""

import json
from processors.claude_processor import LeadProcessor
from storage.storage import LeadStorage


def main():
    # Initialize
    processor = LeadProcessor(config_dir="config")
    storage = LeadStorage(data_dir="data")
    
    # Example: Manually collected leads
    # You would collect these from LinkedIn, IndiaMART, etc.
    sample_leads = [
        {
            'id': 'linkedin_001',
            'name': 'Rajesh Kumar',
            'title': 'Owner',
            'company': 'Kumar Auto Parts Pvt Ltd',
            'source': 'LinkedIn',
            'date': '2026-02-10',
            'content': '''Managing orders from 50+ dealers is absolute chaos. Using WhatsApp for orders, 
            Excel for tracking, phone calls for urgent stuff. Lost 3 orders last week alone due to 
            miscommunication between sales and warehouse. There has to be a better way to handle this.''',
            'url': 'https://linkedin.com/posts/example1'
        },
        {
            'id': 'linkedin_002',
            'name': 'Priya Sharma',
            'title': 'Operations Manager',
            'company': 'Sharma Electronics Distribution',
            'source': 'LinkedIn',
            'date': '2026-02-10',
            'content': '''Looking for inventory tracking solutions. We have 3 warehouses and manual 
            stock counting is failing us. Any recommendations from fellow distributors?''',
            'url': 'https://linkedin.com/posts/example2'
        },
        {
            'id': 'indiamart_001',
            'name': 'Amit Patel',
            'title': 'Managing Director',
            'company': 'Patel Industrial Supplies',
            'source': 'IndiaMART',
            'date': '2026-02-09',
            'content': '''Our dealer network is growing fast but our systems can't keep up. 
            Managing 80+ dealers manually with calls and WhatsApp. Need automated solution urgently.
            Operations team of 8 people can't handle this scale anymore.''',
            'url': 'https://indiamart.com/example3'
        },
        {
            'id': 'linkedin_003',
            'name': 'Student Research',
            'title': 'MBA Student',
            'company': 'IIM Bangalore',
            'source': 'LinkedIn',
            'date': '2026-02-10',
            'content': '''Doing research on supply chain management for my thesis. 
            Looking to interview suppliers about their operations.''',
            'url': 'https://linkedin.com/posts/example4'
        },
        {
            'id': 'linkedin_004',
            'name': 'Vikram Singh',
            'title': 'Supplier',
            'company': 'Singh Bearings',
            'source': 'LinkedIn',
            'date': '2026-02-08',
            'content': '''Thinking about maybe upgrading our systems someday. 
            Current process works okay I guess.''',
            'url': 'https://linkedin.com/posts/example5'
        }
    ]
    
    print("\n" + "="*80)
    print("VIBE-LEADS: Quality-First Lead Generation")
    print("="*80)
    
    # Save raw leads
    storage.save_raw_leads(sample_leads, source="manual_collection")
    
    # Process leads
    results = processor.process_batch(sample_leads)
    
    # Save results
    storage.save_processed_results(results)
    storage.save_qualified_leads(results)
    storage.export_messages_for_outreach(results)
    
    # Print summary
    stats = storage.get_stats(results)
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"Total leads processed: {stats['total']}")
    print(f"Qualified (A+/A): {stats['qualified']} ({stats['qualification_rate']:.1f}%)")
    print(f"  - A+ leads: {stats['a_plus']}")
    print(f"  - A leads: {stats['a']}")
    print(f"Not qualified (B/C): {stats['b'] + stats['c']}")
    print("\n✅ Check the 'data/messages' folder for outreach-ready messages!")
    print("="*80)


if __name__ == "__main__":
    main()
