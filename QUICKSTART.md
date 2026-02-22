# QUICK START GUIDE

## 🚀 Get Running in 5 Minutes

### Step 1: Setup (2 minutes)

```bash
# Extract the zip
unzip vibe-leads.zip
cd vibe-leads

# Install dependencies
pip install -r requirements.txt

# Set up your API key
cp .env.example .env
# Edit .env and add your Anthropic API key
nano .env  # or use any editor
```

### Step 2: Configure for Opbase (2 minutes)

The configs are already set up for Opbase! But you can customize:

```bash
# Edit company details
nano config/company.yaml

# Adjust target audience
nano config/audience.yaml

# Fine-tune pain point detection (MOST IMPORTANT)
nano config/pain_points.yaml
```

### Step 3: Test with Examples (1 minute)

```bash
# Run the example with sample leads
python example_usage.py
```

This will:
- Process 5 sample leads
- Score them (A+, A, B, C)
- Generate messages for qualified leads
- Save everything to `data/` folder

Check `data/messages/` for the results!

---

## 📝 Add Your Own Leads

Edit `example_usage.py` and replace `sample_leads` with your own:

```python
your_leads = [
    {
        'name': 'Person Name',
        'title': 'Their Title',
        'company': 'Company Name',
        'source': 'LinkedIn',
        'date': '2026-02-10',
        'content': '''What they posted about their problem...''',
        'url': 'https://linkedin.com/...'
    },
    # Add more leads...
]
```

Then run:
```bash
python example_usage.py
```

---

## 🎯 Where to Find Leads

### LinkedIn
Search for posts with:
- "managing orders difficult"
- "inventory tracking issue"  
- "B2B operations chaos"

Filter by:
- Location: India
- Title: Owner, Founder, Director

### IndiaMART
Browse supplier forums for:
- Operational complaints
- System/process questions
- Coordination issues

### Google Search
```
site:linkedin.com "industrial supplier" India "struggling with orders"
site:indiamart.com "manufacturer" "operations"
```

---

## 📊 Understanding Results

### Lead Scores

**A+** (Send immediately)
- Perfect fit
- Clear urgent pain
- Decision maker
- Specific details

**A** (High priority)
- Good fit
- Clear pain
- Authority present
- Worth pursuing

**B** (Maybe)
- Weak signals
- Low urgency
- Review manually

**C** (Skip)
- Not qualified
- Wrong fit
- No pain point

### Output Files

```
data/
├── raw_leads/           # Your input leads
├── processed/           # Full analysis results
├── qualified/           # Only A+/A leads (CSV + JSON)
└── messages/            # Ready-to-send messages
    └── batch_20260210/
        ├── A+_01_Rajesh_Kumar.txt
        ├── A_02_Priya_Sharma.txt
        └── SUMMARY.txt
```

---

## 💡 Pro Tips

1. **Start small**: Test with 20 leads first
2. **Review everything**: Don't auto-send without reading
3. **Track results**: Note which messages get replies
4. **Iterate configs**: Adjust pain_points.yaml based on what works
5. **Quality > Quantity**: 20 perfect leads > 200 garbage leads

---

## 🆘 Troubleshooting

**"No module named anthropic"**
→ Run `pip install -r requirements.txt`

**"ANTHROPIC_API_KEY environment variable not set"**
→ Create .env file and add your API key

**"No qualified leads"**
→ Your sample leads might not match criteria. Try different leads or adjust `pain_points.yaml`

**API costs too high**
→ You're using the wrong model. Ensure CLAUDE_MODEL=claude-sonnet-4-20250514 in .env

---

## 📈 Next Steps

1. ✅ Run example
2. ✅ Add your own 20 leads
3. ✅ Process and review results
4. ✅ Send the A+ messages
5. ✅ Track reply rate
6. ✅ Iterate on configs
7. 🚀 Scale up!

---

**Questions? Check README.md or open an issue on GitHub.**
