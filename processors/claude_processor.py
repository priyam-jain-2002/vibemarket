"""
AI-Powered Lead Processor
Analyzes leads for quality and generates vibe-matched outreach messages

Supports multiple LLM backends:
- Anthropic Claude (default)
- OpenAI GPT-4
- Google Gemini
- Ollama (local)
"""

import os
import re
import yaml
import json
from typing import Dict, List, Optional
from datetime import datetime
from processors.llm_backends import get_llm_backend


def extract_json(text: str) -> dict:
    """
    Robustly extract JSON from LLM output.
    Handles: ```json blocks, ``` blocks, raw JSON, JSON buried in text.
    """
    # Strip whitespace
    text = text.strip()

    # Try 1: ```json ... ```
    m = re.search(r'```json\s*([\s\S]*?)```', text)
    if m:
        return json.loads(m.group(1).strip())

    # Try 2: ``` ... ```
    m = re.search(r'```\s*([\s\S]*?)```', text)
    if m:
        candidate = m.group(1).strip()
        if candidate.startswith('{'):
            return json.loads(candidate)

    # Try 3: Find the first { ... } block (handles text before/after JSON)
    start = text.find('{')
    if start != -1:
        # Walk forward counting braces to find the matching close
        depth = 0
        for i, ch in enumerate(text[start:], start):
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
            if depth == 0:
                return json.loads(text[start:i+1])

    # Try 4: Raw JSON
    return json.loads(text)

class LeadProcessor:
    def __init__(self, config_dir: str = "config", llm_provider: Optional[str] = None):
        """
        Initialize with configuration files

        Args:
            config_dir: Path to configuration directory
            llm_provider: Force specific LLM ('claude', 'openai', 'gemini', 'ollama')
                         If None, auto-detects from available API keys
        """
        self.config_dir = config_dir
        self.company = self._load_yaml("company.yaml")
        self.audience = self._load_yaml("audience.yaml")
        self.pain_points = self._load_yaml("pain_points.yaml")

        # Initialize LLM backend (auto-detects or uses specified provider)
        self.llm = get_llm_backend(llm_provider)
    
    def _load_yaml(self, filename: str) -> dict:
        """Load YAML configuration file"""
        path = os.path.join(self.config_dir, filename)
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    def _build_analysis_prompt(self, lead: Dict) -> str:
        """
        Build the Claude prompt for lead analysis
        This is where the magic happens - quality comes from prompt quality
        """
        
        prompt = f"""You are an expert lead qualification analyst for B2B sales.

COMPANY CONTEXT:
Product: {self.company['company']['name']} - {self.company['company']['product']}
What we solve: {', '.join(self.company['value_propositions']['primary'])}

TARGET AUDIENCE:
- Industries: {', '.join(self.audience['audience']['industries']['high_priority'])}
- Titles: {', '.join(self.audience['audience']['titles']['primary'])}
- Location: {', '.join(self.audience['audience']['locations']['primary'])}

LEAD TO ANALYZE:
Name: {lead.get('name', 'Unknown')}
Title: {lead.get('title', 'Unknown')}
Company: {lead.get('company', 'Unknown')}
Source: {lead.get('source', 'Unknown')}
Date: {lead.get('date', 'Unknown')}

What they said:
\"\"\"{lead.get('content', '')}\"\"\"

YOUR TASK:
Analyze this lead with EXTREME RIGOR. We care about QUALITY over quantity.

1. PAIN POINT DETECTION:
   - Does this person explicitly or implicitly mention operational challenges?
   - Which specific pain points do they mention?
   - Rate pain clarity: EXPLICIT (they say it directly) / IMPLICIT (suggested) / NONE

2. URGENCY ASSESSMENT:
   - HIGH: Using words like "urgent", "crisis", "losing money", specific losses mentioned
   - MEDIUM: "struggling", "difficult", "need help", "looking for solution"
   - LOW: "exploring", "thinking about", "considering"
   - NONE: No urgency indicators

3. AUTHORITY EVALUATION:
   - DECISION_MAKER: Owner, Founder, Director, C-level
   - INFLUENCER: Manager, Head, Team Lead
   - UNKNOWN: Title unclear
   - LOW: Junior, Assistant, Student

4. SPECIFICITY SCORE (1-10):
   - 10 = Specific numbers, detailed problems, concrete examples
   - 5 = General problem statement
   - 1 = Vague or generic

5. INDUSTRY & SIZE FIT:
   - Is this in our target industry?
   - Right company size (MSME, 10-500 employees)?

6. LEAD SCORE:
   - A+ : Explicit pain + Decision maker + High urgency + Specific details
   - A  : Clear pain + Authority + Medium urgency
   - B  : Pain mentioned but lower urgency or unclear authority
   - C  : Weak signals, disqualify

7. DISQUALIFICATION CHECK:
   - Spam/promotional?
   - Student/researcher?
   - Wrong industry?
   - Not a real pain point?

OUTPUT: Reply with ONLY a valid JSON object. No explanation, no markdown, no text before or after.

Required fields:
- score: one of "A+", "A", "B", "C"
- pain_points: array of strings
- pain_clarity: one of "EXPLICIT", "IMPLICIT", "NONE"
- urgency: one of "HIGH", "MEDIUM", "LOW", "NONE"
- authority: one of "DECISION_MAKER", "INFLUENCER", "UNKNOWN", "LOW"
- specificity_score: integer 1-10
- industry_fit: true or false
- size_fit: true or false
- disqualify: true or false
- disqualify_reason: string (empty if not disqualified)
- reasoning: string (2-3 sentences)
- key_signals: array of strings
- missing_signals: array of strings

BE STRICT. Only A+ and A leads are worth pursuing. When in doubt, score lower.
"""
        
        return prompt
    
    def _build_message_prompt(self, lead: Dict, analysis: Dict) -> str:
        """
        Build prompt for generating vibe-matched outreach message
        Only called for A+ and A leads
        """
        
        # Get relevant pain point examples
        pain_points_section = self._get_pain_point_context(analysis['pain_points'])
        
        prompt = f"""You are an expert at writing personalized B2B outreach messages that feel authentic and helpful, not salesy.

COMPANY CONTEXT:
Product: {self.company['company']['name']} - {self.company['company']['product']}
Communication style: {self.company['communication_style']['tone']}
Language: {self.company['communication_style']['language']}

AVOID: {', '.join(self.company['communication_style']['avoid'])}
PREFER: {', '.join(self.company['communication_style']['prefer'])}

LEAD CONTEXT:
Name: {lead.get('name', 'Unknown')}
Title: {lead.get('title', 'Unknown')}
Company: {lead.get('company', 'Unknown')}

What they said:
\"\"\"{lead.get('content', '')}\"\"\"

ANALYSIS:
Pain points: {', '.join(analysis['pain_points'])}
Urgency: {analysis['urgency']}
Authority: {analysis['authority']}
Key signals: {', '.join(analysis.get('key_signals', []))}

{pain_points_section}

YOUR TASK:
Write a PERSONALIZED outreach message that:

1. MATCHES THEIR VIBE:
   - If frustrated/urgent → Acknowledge the pain, be direct
   - If exploring → Be helpful, provide options
   - If skeptical → Lead with proof/data
   - Mirror their communication style (formal vs casual)

2. REFERENCES THEIR SPECIFIC SITUATION:
   - Quote or paraphrase what they said
   - Show you actually read their post
   - Connect to their specific numbers/details if mentioned

3. POSITIONS VALUE WITHOUT SELLING:
   - Don't pitch the product
   - Share how similar companies solved this
   - Offer to "share the playbook" not "schedule a demo"

4. KEEPS IT BRIEF:
   - Under 150 words
   - 2-3 short paragraphs
   - Natural language, not corporate speak

5. ENDS WITH LOW-PRESSURE NEXT STEP:
   - "Happy to share what worked" not "Let's schedule a call"
   - "Can show you the approach" not "Book a demo"
   - Make it easy to say yes

EXAMPLE STRUCTURE:

[Reference their specific problem]

[Relevant proof point or similar situation]

[Low-pressure offer to help]

Return ONLY the message text, no extra formatting or explanation.
The message should feel like it's from a peer who genuinely wants to help, not a salesperson.
"""
        
        return prompt
    
    def _get_pain_point_context(self, detected_pains: List[str]) -> str:
        """Get relevant examples for detected pain points"""
        context_parts = []
        
        for pain in detected_pains:
            for pain_def in self.pain_points['pain_points']['primary_pains']:
                if pain.lower() in pain_def['name'].lower():
                    examples = pain_def.get('ideal_lead_examples', [])
                    if examples:
                        context_parts.append(f"\n{pain_def['name']} examples:")
                        context_parts.append('\n'.join(f"- {ex}" for ex in examples[:2]))
        
        return '\n'.join(context_parts) if context_parts else ""
    
    def analyze_lead(self, lead: Dict) -> Dict:
        """
        Analyze a single lead for quality
        Returns analysis with score and detailed reasoning
        """

        try:
            prompt = self._build_analysis_prompt(lead)

            # Use LLM backend (works with any configured LLM)
            response_text = self.llm.generate(
                prompt=prompt,
                system_message="You are an expert lead qualification analyst for B2B sales."
            )
            
            # Extract JSON from response (handles markdown blocks, raw JSON, etc.)
            analysis = extract_json(response_text)
            
            # Add metadata
            analysis['analyzed_at'] = datetime.now().isoformat()
            analysis['lead_id'] = lead.get('id', lead.get('url', 'unknown'))
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing lead: {e}")
            return {
                "score": "ERROR",
                "error": str(e),
                "analyzed_at": datetime.now().isoformat()
            }
    
    def generate_message(self, lead: Dict, analysis: Dict) -> Optional[str]:
        """
        Generate vibe-matched outreach message
        Only for A+ and A leads
        """

        if analysis['score'] not in ['A+', 'A', 'B']:
            return None

        try:
            prompt = self._build_message_prompt(lead, analysis)

            # Use LLM backend (works with any configured LLM)
            outreach_message = self.llm.generate(
                prompt=prompt,
                system_message="You are an expert at writing personalized, vibe-matched outreach messages."
            ).strip()

            # Strip common LLM preambles (local models often add these)
            preambles = [
                "here is the personalized outreach message:",
                "here is a personalized outreach message:",
                "here's the personalized outreach message:",
                "here's a personalized outreach message:",
                "here is the outreach message:",
                "sure, here is",
                "sure! here is",
            ]
            lower = outreach_message.lower()
            for p in preambles:
                if lower.startswith(p):
                    outreach_message = outreach_message[len(p):].strip()
                    break

            return outreach_message
            
        except Exception as e:
            print(f"Error generating message: {e}")
            return None
    
    def process_lead(self, lead: Dict) -> Dict:
        """
        Full processing pipeline for a single lead
        Returns complete analysis with message if qualified
        """
        
        print(f"\n📊 Analyzing: {lead.get('name', 'Unknown')}")
        
        # Step 1: Analyze quality
        analysis = self.analyze_lead(lead)
        
        if analysis.get('score') == 'ERROR':
            return {
                'lead': lead,
                'analysis': analysis,
                'message': None,
                'status': 'error'
            }
        
        print(f"   Score: {analysis['score']}")
        print(f"   Pain: {', '.join(analysis.get('pain_points', ['None']))}")
        print(f"   Urgency: {analysis.get('urgency', 'Unknown')}")
        
        # Step 2: Generate message if qualified
        message = None
        if analysis['score'] in ['A+', 'A', 'B']:
            print(f"   ✅ Qualified - Generating message...")
            message = self.generate_message(lead, analysis)
        else:
            print(f"   ❌ Not qualified - Skipping message generation")
        
        return {
            'lead': lead,
            'analysis': analysis,
            'message': message,
            'status': 'success',
            'processed_at': datetime.now().isoformat()
        }
    
    def process_batch(self, leads: List[Dict]) -> List[Dict]:
        """
        Process multiple leads
        Returns list of results
        """
        
        print(f"\n🚀 Processing {len(leads)} leads...")
        print("=" * 60)
        
        results = []
        stats = {
            'total': len(leads),
            'a_plus': 0,
            'a': 0,
            'b': 0,
            'c': 0,
            'error': 0
        }
        
        for lead in leads:
            result = self.process_lead(lead)
            results.append(result)
            
            # Update stats
            score = result['analysis'].get('score', 'ERROR')
            if score == 'A+':
                stats['a_plus'] += 1
            elif score == 'A':
                stats['a'] += 1
            elif score == 'B':
                stats['b'] += 1
            elif score == 'C':
                stats['c'] += 1
            else:
                stats['error'] += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("📈 BATCH RESULTS:")
        print(f"   Total processed: {stats['total']}")
        print(f"   A+ leads: {stats['a_plus']} ({stats['a_plus']/stats['total']*100:.1f}%)")
        print(f"   A leads: {stats['a']} ({stats['a']/stats['total']*100:.1f}%)")
        print(f"   B leads: {stats['b']} ({stats['b']/stats['total']*100:.1f}%)")
        print(f"   C leads: {stats['c']} ({stats['c']/stats['total']*100:.1f}%)")
        print(f"   Errors: {stats['error']}")
        print(f"   Messages generated: {stats['a_plus'] + stats['a']}")
        print("=" * 60)
        
        return results


if __name__ == "__main__":
    # Example usage
    processor = LeadProcessor()
    
    # Test with sample lead
    sample_lead = {
        'id': 'test_001',
        'name': 'Rajesh Kumar',
        'title': 'Owner',
        'company': 'Kumar Auto Parts',
        'source': 'LinkedIn',
        'date': '2026-02-10',
        'content': '''Managing orders from 50+ dealers is absolute chaos. Using WhatsApp for orders, 
        Excel for tracking, phone calls for urgent stuff. Lost 3 orders last week alone due to 
        miscommunication. There has to be a better way to handle this.''',
        'url': 'https://linkedin.com/example'
    }
    
    result = processor.process_lead(sample_lead)
    
    print("\n📋 RESULT:")
    print(json.dumps(result, indent=2, default=str))
