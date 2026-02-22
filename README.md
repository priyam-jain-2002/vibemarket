# Vibe-Leads: Quality-First Lead Generation

> AI-powered lead generation that prioritizes **quality over quantity** through vibe-matching and deep analysis.

## 🎯 Philosophy

Most lead gen tools blast 1000 templated messages and get 2% reply rates.

Vibe-Leads analyzes 100 leads deeply, qualifies 20 as high-quality, generates 20 personalized messages, and gets 25-30% reply rates.

**20 perfect leads > 200 garbage leads**

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/vibe-leads
cd vibe-leads

# Install dependencies
pip install -r requirements.txt

# Set up your Claude API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 2. Configure for Your Business

Edit the config files in `config/`:

**`config/company.yaml`** - Your product/company details
**`config/audience.yaml`** - Who you're targeting  
**`config/pain_points.yaml`** - Problems you solve

### 3. Collect Leads Manually

Find 20-30 leads from:
- LinkedIn posts about operational challenges
- IndiaMART forum discussions
- Twitter/Reddit posts about pain points

Save in this format:
```python
lead = {
    'name': 'Rajesh Kumar',
    'title': 'Owner',
    'company': 'Kumar Auto Parts',
    'source': 'LinkedIn',
    'date': '2026-02-10',
    'content': 'What they posted about their problem',
    'url': 'https://linkedin.com/...'
}
```

### 4. Process Leads

```python
from processors.claude_processor import LeadProcessor
from storage.storage import LeadStorage

# Initialize
processor = LeadProcessor()
storage = LeadStorage()

# Process your leads
results = processor.process_batch(your_leads)

# Save results
storage.save_qualified_leads(results)
storage.export_messages_for_outreach(results)
```

### 5. Review & Send

Check `data/messages/` for outreach-ready messages.

Each A+ and A lead gets:
- Personalized message that matches their vibe
- Context about their specific pain point
- Low-pressure next step

---

## 📊 How It Works

### Lead Scoring (Strict Quality Filter)

**A+ Lead** (Top 5-10%)
- Explicit pain point mentioned
- Decision maker (Owner/Founder/Director)
- High urgency ("losing money", "crisis")
- Specific details/numbers

**A Lead** (Next 10-15%)
- Clear pain point
- Authority or influence
- Medium urgency
- Good fit

**B Lead** (20-30%)
- Pain mentioned but vague
- Lower urgency or unclear authority

**C Lead** (Rejected - 50-60%)
- No clear pain point
- Wrong audience
- Student/researcher
- Spam/promotional

### Vibe-Matching Magic

The system analyzes:
1. **Communication style**: Formal vs casual
2. **Urgency level**: Crisis vs exploring
3. **Pain specificity**: "Lost 3 orders" vs "having issues"
4. **Decision authority**: Owner vs junior manager

Then generates messages that:
- Reference their specific words
- Match their energy/tone
- Show you actually read their post
- Offer help, not a sales pitch

---

## 🎛️ Configuration Guide

### Company Config (`config/company.yaml`)

```yaml
company:
  name: "YourProduct"
  product: "What you do"
  website: "https://yoursite.com"

value_propositions:
  primary:
    - "Main problem you solve"
    - "Key benefit 2"
    - "Key benefit 3"

communication_style:
  tone: "conversational"  # formal, conversational, casual
  language: "Indian English"  # Adapt to your market
  
  avoid:
    - "corporate buzzwords"
    - "salesy language"
```

### Audience Config (`config/audience.yaml`)

```yaml
audience:
  titles:
    primary:
      - "Owner"
      - "Founder"
      - "Director"
  
  industries:
    high_priority:
      - "Your Industry 1"
      - "Your Industry 2"
  
  locations:
    primary:
      - "Your Target Geography"
```

### Pain Points Config (`config/pain_points.yaml`)

**This is the most important file.**

Define exactly what problems you solve and how to detect them:

```yaml
pain_points:
  primary_pains:
    - name: "Problem Name"
      description: "What this problem is"
      
      explicit_signals:
        - "exact phrases people use"
        - "keywords to look for"
      
      urgency_indicators:
        high:
          - "losing money"
          - "crisis"
        medium:
          - "struggling"
          - "difficult"
      
      ideal_lead_examples:
        - "Example of what a perfect lead would say"
```

The better you define pain points, the better the lead quality.

---

## 💰 Cost

**Claude API Pricing:**
- ~$0.003 per lead analyzed
- ~$0.005 per message generated

**Example:**
- Process 100 leads: $0.30
- Generate 20 messages: $0.10
- **Total: $0.40 for 20 quality leads**

Compare to:
- Traditional tools: $50-200/month
- Apollo/Lemlist: $49-99/month
- Clay: $149-349/month

---

## 📁 Project Structure

```
vibe-leads/
├── config/              # Your business configuration
│   ├── company.yaml
│   ├── audience.yaml
│   └── pain_points.yaml
├── processors/          # Core processing logic
│   └── claude_processor.py
├── storage/            # Data storage
│   └── storage.py
├── scrapers/           # Lead collection (future)
├── data/               # Generated data
│   ├── raw_leads/
│   ├── processed/
│   ├── qualified/
│   └── messages/       # Outreach-ready messages
├── example_usage.py    # Example script
└── requirements.txt
```

---

## 🔧 Advanced Usage

### Batch Processing

```python
# Process multiple batches
for batch in lead_batches:
    results = processor.process_batch(batch)
    storage.save_qualified_leads(results)
```

### Custom Scoring

Edit `config/pain_points.yaml` to adjust:
- Signal weights
- Scoring criteria
- Quality thresholds

### Export Formats

```python
# CSV for spreadsheets
storage.save_qualified_leads(results)

# Individual text files for copy-paste
storage.export_messages_for_outreach(results)

# JSON for further processing
storage.save_processed_results(results)
```

---

## 🎯 Best Practices

### 1. Start Small
- Test with 20-30 manually collected leads
- See what gets qualified
- Refine your pain point definitions

### 2. Review Every Message
- AI is good but not perfect
- Always review before sending
- Tweak messages for your voice

### 3. Track Results
- Note which messages get replies
- Update configs based on what works
- Iterate on quality signals

### 4. Don't Automate Too Early
- Validate the approach manually first
- Build automation only after proven
- Quality > speed always

---

## 🚧 Roadmap

### Phase 1: Manual Processing ✅
- Config-based setup
- Claude-powered analysis
- Vibe-matched message generation

### Phase 2: Semi-Automation (Next)
- LinkedIn scraper
- IndiaMART scraper
- Scheduled processing

### Phase 3: Full Pipeline
- Auto-scraping with scheduling
- CRM integration
- Follow-up sequences

---

## 🤝 Contributing

This is open source! Contributions welcome:

1. **Add Scrapers**: Build scrapers for new platforms
2. **Improve Prompts**: Better analysis = better leads
3. **Add Features**: Export to CRM, auto-sending, etc.
4. **Share Configs**: Industry-specific pain point definitions

---

## 📄 License

MIT License - use it for anything, commercial or personal.

---

## 🙏 Credits

Built with:
- [Anthropic Claude](https://anthropic.com) - AI analysis and generation
- Python - Core processing
- YAML - Configuration

---

## 💡 Philosophy

> "The best cold outreach feels warm."

Vibe-Leads is built on the principle that AI should make outreach **more human**, not less.

By deeply analyzing what people actually say and matching their energy, we can have real conversations at scale.

Not spam. Not templates. Just thoughtful, personalized messages to people who actually need what you're offering.

---

## 📞 Support

Questions? Ideas? Found a bug?

Open an issue or start a discussion on GitHub.

---

**Built by [Your Name] for Opbase, open-sourced for everyone.**
