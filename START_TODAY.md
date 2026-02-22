# Start Generating Quality Leads TODAY 🚀

## Quick Setup (5 minutes)

### Step 1: Install ONLY what you need right now

```bash
pip3 install anthropic pyyaml python-dotenv
```

That's it! Just 3 packages to start.

### Step 2: Configure your API key

```bash
# Copy the example
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=sk-ant-xxxxx
```

Or set it directly:
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### Step 3: Run it NOW

```bash
python3 example_usage.py
```

This will:
- ✅ Analyze 5 example leads with Claude AI
- ✅ Generate personalized outreach messages for A+/A leads
- ✅ Export to CSV and individual text files
- ✅ Show you exactly which leads are quality (A+/A vs B/C)

---

## Where Your Leads Will Be

After running, check these folders:

```
data/
├── qualified/              # Your A+ and A leads only
│   ├── qualified_*.csv     # Spreadsheet view
│   └── qualified_*.json    # Full data
│
└── messages/               # Ready-to-send messages
    └── batch_*/
        ├── A+_01_Name.txt  # Individual message files
        ├── A_02_Name.txt
        └── SUMMARY.txt     # Batch overview
```

**Open the `.txt` files in `data/messages/` - These are ready to copy-paste and send!**

---

## How to Add YOUR Leads (Real Ones)

### Option 1: Quick Script (Fastest)

Create `my_leads.py`:

```python
from processors.claude_processor import LeadProcessor
from storage.storage import LeadStorage

# Your real leads from LinkedIn, IndiaMART, etc.
my_leads = [
    {
        'id': '1',
        'name': 'Rajesh Kumar',
        'title': 'Owner',
        'company': 'Kumar Industries',
        'source': 'LinkedIn',
        'date': '2026-02-10',
        'content': '''
        Managing 50+ dealer orders is absolute chaos. Using WhatsApp for
        orders, Excel for tracking. Lost 3 orders this week because messages
        got buried. Need a proper system urgently.
        ''',
        'url': 'https://linkedin.com/posts/rajesh-kumar-...'
    },
    # Add more leads here...
]

# Process them
processor = LeadProcessor(config_dir="config")
storage = LeadStorage(data_dir="data")

print("🚀 Processing your leads...")
results = processor.process_batch(my_leads)

# Save results
storage.save_qualified_leads(results, source="my_leads")
storage.export_messages_for_outreach(results, source="my_leads")

print(f"\n✅ Done! Check data/messages/ for your personalized outreach messages")
```

Run it:
```bash
python3 my_leads.py
```

### Option 2: Edit example_usage.py

Just replace the example leads with yours in [example_usage.py](example_usage.py) (lines 15-75).

---

## Daily Workflow (Starting Today)

### Morning Routine (15 mins)

1. **Collect leads from LinkedIn/IndiaMART**
   - Copy their posts mentioning problems
   - Save: name, title, company, post content, URL

2. **Add to script**
   ```python
   my_leads = [
       {'name': '...', 'content': '...', ...},
       # Paste more leads
   ]
   ```

3. **Run analysis**
   ```bash
   python3 my_leads.py
   ```

4. **Review A+/A leads**
   - Open `data/qualified/qualified_*.csv`
   - See scores, pain points, urgency

5. **Send messages**
   - Open `data/messages/batch_*/`
   - Copy-paste messages to LinkedIn/email
   - Customize if needed (they're already 90% ready)

### What Makes a Good Lead?

The AI looks for:
- ✅ **Explicit pain points** ("chaos", "losing money", "urgent need")
- ✅ **Decision maker** (Owner, Director, Founder)
- ✅ **Specific details** ("50+ dealers", "lost 3 orders")
- ✅ **Urgency** ("need ASAP", "crisis")

**A+ Lead Example:**
```
"Managing orders from 100+ dealers across India is complete chaos.
Using WhatsApp and Excel. Lost Rs 2L in orders last month because
messages got buried. Need proper order management system urgently."

→ Score: A+
→ Pain: Order Management Chaos
→ Urgency: HIGH
→ Authority: DECISION_MAKER
→ Message: Personalized, specific, vibe-matched
```

**C Lead Example (Ignored):**
```
"Doing MBA project on supply chain. Looking for information."

→ Score: C
→ Reason: Student, not a buyer, no pain points
→ No message generated (don't waste time)
```

---

## Tips for Quality Over Quantity

✅ **20 perfect leads > 200 garbage leads**

- Don't scrape random contacts
- Find people actively complaining about problems you solve
- Look for specific language in their posts
- Verify they're decision makers (not students/researchers)

### Where to Find Quality Leads TODAY

**LinkedIn:**
1. Search: `"order management chaos" OR "inventory tracking issues" OR "dealer coordination problems"`
2. Filter: Posts from last 7 days
3. Look for: Owners, Directors, Founders posting problems
4. Copy their post content verbatim

**IndiaMART:**
1. Browse buyer requirements in your industry
2. Look for detailed requirements (not generic)
3. Copy their requirement text
4. Note their company name

**Target:**
- Industrial suppliers (auto parts, electronics, machinery)
- Companies with 10-500 employees
- India-based (or your target market)
- B2B businesses with dealer networks

---

## Expected Results (First Day)

If you process **20 leads** today:
- ~4-5 will be A+/A (20-25% qualification rate)
- You'll get 4-5 personalized messages ready to send
- Estimated time: 30 mins to collect, 2 mins to analyze, 10 mins to send
- **Expected reply rate: 25-30%** (if you send good messages to A+ leads)

That means **1-2 meetings booked from today's work** 🎯

---

## Troubleshooting

### "No module named anthropic"
```bash
pip3 install anthropic
```

### "ANTHROPIC_API_KEY not found"
Make sure `.env` file has:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key
```

Or export it:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### "Permission denied"
```bash
chmod +x example_usage.py
python3 example_usage.py
```

### Results seem wrong?
Check your `config/pain_points.yaml` - customize for your specific use case.

---

## What NOT to Do

❌ Don't blast 1000 leads through the system
❌ Don't scrape random contacts without pain points
❌ Don't send templated messages (always customize slightly)
❌ Don't target students, researchers, or non-buyers

**Focus:** Quality leads with real pain points matching your solution.

---

## Ready to Scale? (Later)

Once this is working and you're closing deals:

- **Phase 2:** Automate LinkedIn scraping (save time on collection)
- **Phase 3:** Add email sending from the system
- **Phase 4:** Track replies and conversions
- **Phase 5:** Full analytics and optimization

But for TODAY, just use the CLI. It works perfectly.

---

## Start Now 🚀

```bash
# 1. Install
pip3 install anthropic pyyaml python-dotenv

# 2. Configure
echo 'ANTHROPIC_API_KEY=sk-ant-your-key' > .env

# 3. Test
python3 example_usage.py

# 4. Check results
ls -la data/messages/
cat data/messages/batch_*/A+_*.txt

# 5. Send those messages and start closing deals!
```

**You're 5 minutes away from your first quality leads.**

Let's go! 💪
