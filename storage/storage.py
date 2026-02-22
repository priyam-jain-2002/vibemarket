"""
Storage Module
Handles saving leads, analysis results, and generated messages
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict
from pathlib import Path


class LeadStorage:
    def __init__(self, data_dir: str = "data"):
        """Initialize storage with data directory"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.raw_dir = self.data_dir / "raw_leads"
        self.processed_dir = self.data_dir / "processed"
        self.qualified_dir = self.data_dir / "qualified"
        self.messages_dir = self.data_dir / "messages"
        
        for dir in [self.raw_dir, self.processed_dir, self.qualified_dir, self.messages_dir]:
            dir.mkdir(exist_ok=True)
    
    def save_raw_leads(self, leads: List[Dict], source: str) -> str:
        """Save raw scraped leads"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source}_{timestamp}.json"
        filepath = self.raw_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(leads, f, indent=2, default=str)
        
        print(f"✅ Saved {len(leads)} raw leads to {filepath}")
        return str(filepath)
    
    def save_processed_results(self, results: List[Dict]) -> str:
        """Save processed results with analysis"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"processed_{timestamp}.json"
        filepath = self.processed_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"✅ Saved processed results to {filepath}")
        return str(filepath)
    
    def save_qualified_leads(self, results: List[Dict]) -> str:
        """Save only A+ and A leads with their messages"""
        qualified = [r for r in results if r['analysis'].get('score') in ['A+', 'A']]
        
        if not qualified:
            print("⚠️  No qualified leads to save")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        json_file = self.qualified_dir / f"qualified_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(qualified, f, indent=2, default=str)
        
        # Save as CSV for easy review
        csv_file = self.qualified_dir / f"qualified_{timestamp}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'score', 'name', 'title', 'company', 'source', 
                'pain_points', 'urgency', 'authority', 'message', 'url'
            ])
            writer.writeheader()
            
            for r in qualified:
                writer.writerow({
                    'score': r['analysis']['score'],
                    'name': r['lead'].get('name', ''),
                    'title': r['lead'].get('title', ''),
                    'company': r['lead'].get('company', ''),
                    'source': r['lead'].get('source', ''),
                    'pain_points': ', '.join(r['analysis'].get('pain_points', [])),
                    'urgency': r['analysis'].get('urgency', ''),
                    'authority': r['analysis'].get('authority', ''),
                    'message': r.get('message', ''),
                    'url': r['lead'].get('url', '')
                })
        
        print(f"✅ Saved {len(qualified)} qualified leads")
        print(f"   JSON: {json_file}")
        print(f"   CSV: {csv_file}")
        return str(csv_file)
    
    def export_messages_for_outreach(self, results: List[Dict]) -> str:
        """
        Export messages in a format ready for outreach
        One file per lead for easy copy-paste
        """
        qualified = [r for r in results if r.get('message')]
        
        if not qualified:
            print("⚠️  No messages to export")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_dir = self.messages_dir / f"batch_{timestamp}"
        batch_dir.mkdir(exist_ok=True)
        
        # Create individual message files
        for i, result in enumerate(qualified, 1):
            lead = result['lead']
            analysis = result['analysis']
            message = result['message']
            
            # Safe filename
            name = lead.get('name', 'unknown').replace(' ', '_').replace('/', '_')
            score = analysis['score']
            filename = f"{score}_{i:02d}_{name}.txt"
            
            filepath = batch_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"TO: {lead.get('name', 'Unknown')}\n")
                f.write(f"TITLE: {lead.get('title', 'Unknown')}\n")
                f.write(f"COMPANY: {lead.get('company', 'Unknown')}\n")
                f.write(f"SOURCE: {lead.get('source', 'Unknown')}\n")
                f.write(f"URL: {lead.get('url', '')}\n")
                f.write(f"SCORE: {score}\n")
                f.write(f"PAIN POINTS: {', '.join(analysis.get('pain_points', []))}\n")
                f.write(f"\n{'='*60}\n")
                f.write(f"ORIGINAL POST:\n")
                f.write(f"{lead.get('content', '')}\n")
                f.write(f"\n{'='*60}\n")
                f.write(f"OUTREACH MESSAGE:\n\n")
                f.write(message)
                f.write(f"\n\n{'='*60}\n")
                f.write(f"ANALYSIS:\n")
                f.write(f"{analysis.get('reasoning', '')}\n")
        
        # Create summary file
        summary_file = batch_dir / "SUMMARY.txt"
        with open(summary_file, 'w') as f:
            f.write(f"OUTREACH BATCH - {timestamp}\n")
            f.write(f"{'='*60}\n\n")
            f.write(f"Total messages: {len(qualified)}\n")
            
            a_plus = sum(1 for r in qualified if r['analysis']['score'] == 'A+')
            a_leads = sum(1 for r in qualified if r['analysis']['score'] == 'A')
            
            f.write(f"A+ leads: {a_plus}\n")
            f.write(f"A leads: {a_leads}\n\n")
            f.write(f"{'='*60}\n\n")
            f.write("FILES:\n")
            for i, result in enumerate(qualified, 1):
                lead = result['lead']
                score = result['analysis']['score']
                f.write(f"{i}. [{score}] {lead.get('name', 'Unknown')} - {lead.get('company', 'Unknown')}\n")
        
        print(f"✅ Exported {len(qualified)} messages to {batch_dir}")
        print(f"   Each message in separate file for easy copy-paste")
        print(f"   See {summary_file} for overview")
        
        return str(batch_dir)
    
    def get_stats(self, results: List[Dict]) -> Dict:
        """Generate statistics from results"""
        total = len(results)
        if total == 0:
            return {}
        
        scores = [r['analysis'].get('score', 'ERROR') for r in results]
        
        stats = {
            'total': total,
            'a_plus': scores.count('A+'),
            'a': scores.count('A'),
            'b': scores.count('B'),
            'c': scores.count('C'),
            'errors': scores.count('ERROR'),
            'qualified': scores.count('A+') + scores.count('A'),
            'qualification_rate': (scores.count('A+') + scores.count('A')) / total * 100
        }
        
        return stats


if __name__ == "__main__":
    # Test storage
    storage = LeadStorage()
    
    # Test data
    test_results = [
        {
            'lead': {'name': 'Test User', 'company': 'Test Co', 'source': 'LinkedIn', 'url': 'http://test.com'},
            'analysis': {'score': 'A+', 'pain_points': ['Order Chaos'], 'urgency': 'HIGH', 'authority': 'DECISION_MAKER'},
            'message': 'Test message here'
        }
    ]
    
    storage.save_qualified_leads(test_results)
    storage.export_messages_for_outreach(test_results)
