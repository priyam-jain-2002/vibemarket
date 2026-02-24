import os
import sys
from scrapers.reddit_scraper import RedditScraper
from processors.claude_processor import LeadProcessor
from storage.storage import LeadStorage

def main():
    print("=" * 80)
    print("🤖 REDDIT LEAD GENERATION PIPELINE")
    print("=" * 80)
    
    SEARCH_QUERY = 'excel inventory tracking nightmare'
    LEAD_LIMIT = 5
    
    scraper = RedditScraper()
    storage = LeadStorage(data_dir="data")

    # Step 1: Scrape Reddit
    print(f"\n📍 STEP 1: FINDING LEADS ON REDDIT")
    print(f"   Query: '{SEARCH_QUERY}'")
    
    leads = scraper.search_posts(query=SEARCH_QUERY, limit=LEAD_LIMIT)
    
    if not leads:
        print("⚠️  No leads found. Try a different query.")
        scraper.close()
        return
        
    storage.save_raw_leads(leads, source="reddit_only")
    scraper.close()
    
    # Step 2: AI Processing (Personalized Message)
    print("\n📍 STEP 2: AI ANALYSIS & PERSONALIZED OUTREACH")
    print("   Initializing LLM (Make sure Ollama is running or API keys are set)...")
    
    try:
        processor = LeadProcessor(config_dir="config")
        results = processor.process_batch(leads)
        
        storage.save_processed_results(results)
        
        qualified = [r for r in results if r['analysis'].get('score') in ['A+', 'A', 'B']]
        
        if qualified:
            storage.save_qualified_leads(results)
            msg_dir = storage.export_messages_for_outreach(results)
            print(f"\n✅ Created {len(qualified)} personalized messages!")
            print(f"   📁 Check folder: {msg_dir}")
        else:
            print("\n⚠️ No highly qualified leads found in this batch (No A+ or A leads).")
            print("   Try adjusting the search query or pain points config.")

    except Exception as e:
        print(f"\n❌ AI Processing failed: {e}")
        print("💡 Solution: Make sure your LLM provider is active.")
        print("   - If using Ollama: Run 'ollama serve' in another terminal")
        print("   - If using Anthropic/OpenAI: Add the API key to .env")

if __name__ == "__main__":
    main()
