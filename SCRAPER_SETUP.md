# LinkedIn Scraper Setup Guide

## 🎯 What This Does

**Complete Automation Loop:**
1. **Find leads** → Auto-scrape LinkedIn for posts mentioning your keywords
2. **Get backgrounds** → Extract profile data (name, title, company)
3. **AI Analysis** → Score quality (A+/A/B/C), detect pain points
4. **Generate messages** → Personalized outreach ready to send

## ⚙️ Setup (5 minutes)

### Step 1: Install Playwright

```bash
pip install playwright beautifulsoup4
playwright install chromium
```

This downloads the Chromium browser used for scraping.

### Step 2: Add LinkedIn Credentials to `.env`

```bash
# Add to .env file
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password

# Search configuration
LEAD_SEARCH_QUERY=order management chaos India
LEAD_LIMIT=20
```

**Security Note:** These credentials stay on your machine. Never commit `.env` to git.

### Step 3: Run Automated Pipeline

```bash
python3 auto_pipeline.py
```

That's it! The system will:
- Login to LinkedIn
- Search for posts matching your keywords
- Extract leads (name, title, company, post content)
- Analyze with AI
- Generate personalized messages
- Save to `data/messages/`

## 🔍 How It Works

### Search Strategy

The scraper searches LinkedIn posts (not profiles) for keywords like:
- "order management chaos"
- "inventory tracking nightmare"
- "dealer network problems"
- "lost orders miscommunication"

### What Gets Extracted

From each post:
- **Name** - Person's full name
- **Title** - Current job title
- **Company** - Where they work
- **Content** - Full post text (their pain points)
- **URL** - Link to their profile

### AI Analysis

Each lead gets scored:
- **A+** - Explicit pain + Decision maker + High urgency → Must contact
- **A** - Clear pain + Authority + Medium urgency → High priority
- **B** - Pain mentioned but weak signals → Low priority
- **C** - No real pain or wrong fit → Skip

### Message Generation

For A+/A leads only:
- Analyzes their vibe (urgent/frustrated/exploring)
- References their specific problem
- Matches their communication style
- Creates personalized outreach (not generic template)

## 📊 Example Output

```
🤖 AUTOMATED LEAD GENERATION PIPELINE
============================================================

📍 STEP 1: FINDING LEADS
   Query: order management chaos India
   Limit: 20

🔐 Logging into LinkedIn...
✅ Login successful!

🔍 Searching LinkedIn for: 'order management chaos India'
   📜 Scrolling... (1/3)
   📜 Scrolling... (2/3)
   Found 18 posts on page
   ✅ Lead 1: Rajesh Kumar - Kumar Auto Parts
   ✅ Lead 2: Priya Sharma - Sharma Electronics
   ✅ Lead 3: Amit Patel - Patel Industrial Supplies

📍 STEP 3: AI ANALYSIS & QUALIFICATION

📊 Analyzing: Rajesh Kumar
   Score: A
   Pain: Managing 50+ dealers, Lost 3 orders due to miscommunication
   Urgency: MEDIUM
   ✅ Qualified - Generating message...

📈 BATCH RESULTS:
   Total processed: 18
   A+ leads: 2 (11.1%)
   A leads: 5 (27.8%)
   Messages generated: 7

🎯 PIPELINE COMPLETE
Leads found: 18
Qualified (A+/A): 7

✅ Check 'data/messages/' for outreach-ready messages!
```

## ⚠️ Important Disclaimers

### LinkedIn ToS Compliance

- **You assume all responsibility** for LinkedIn's Terms of Service compliance
- LinkedIn actively detects and may restrict automated access
- This tool is for **personal research and education**
- Use at your own risk

### Detection Avoidance

The scraper uses stealth tactics:
- Human-like delays (3-8 seconds between actions)
- Realistic user agent
- No "webdriver" flag
- Browser fingerprinting resistance

But LinkedIn is sophisticated. To avoid detection:
- ✅ Run **max once per day**
- ✅ Limit to **20-50 leads per session**
- ✅ Don't run 24/7
- ✅ Use `headless=False` (visible browser)
- ❌ Don't scrape hundreds of leads at once
- ❌ Don't run automated scripts constantly

### Account Safety

If LinkedIn detects automation:
- Warning notification
- Temporary restriction
- Account suspension (rare, for repeat offenders)

**Recommendation:** Use a secondary LinkedIn account for testing.

## 🛠️ Customization

### Change Search Query

Edit `.env`:
```bash
LEAD_SEARCH_QUERY=inventory management nightmare manufacturing
```

### Change Lead Limit

Edit `.env`:
```bash
LEAD_LIMIT=50  # Max recommended: 50 per day
```

### Headless Mode

Edit `auto_pipeline.py`:
```python
scraper = LinkedInScraper(headless=True)  # Hides browser window
```

**Note:** Headless mode is faster but slightly more detectable.

## 📅 Recommended Workflow

### Daily Routine (15 minutes)

**Morning:**
```bash
python3 auto_pipeline.py
```
- Scrapes 20 new leads
- AI analyzes automatically
- Messages generated

**Review (10 min):**
- Check `data/messages/batch_*/SUMMARY.txt`
- Review A+ leads
- Edit messages if needed

**Outreach (5 min):**
- Copy-paste messages to LinkedIn DMs
- Or use email addresses if available

### Weekly

- Adjust search keywords based on what works
- Review analytics (which industries/titles = best response)
- Refine pain point configs in `config/pain_points.yaml`

## 🐛 Troubleshooting

### "Login failed"
- Check credentials in `.env`
- Try logging in manually first (LinkedIn might require verification)
- LinkedIn may be blocking automation (try again later)

### "No leads found"
- Try different keywords
- Search too specific (broaden it)
- Rate limited by LinkedIn (try tomorrow)

### "Playwright not installed"
```bash
pip install playwright
playwright install chromium
```

### Browser keeps crashing
- Close other applications (free up RAM)
- Reduce `LEAD_LIMIT` to 10-20
- Update Playwright: `pip install --upgrade playwright`

## 🔐 Security Best Practices

1. **Never commit `.env` to git**
   - Already in `.gitignore`
   - Contains sensitive credentials

2. **Use app-specific password** (if available)
   - LinkedIn doesn't offer this yet
   - Consider 2FA on main account

3. **Rotate credentials periodically**
   - Change password every few months
   - Use password manager

## 📈 Next Steps

Once you have qualified leads:

1. **Manual outreach** (current)
   - Copy messages from `data/messages/`
   - Send via LinkedIn DMs

2. **Email integration** (Phase 3 - coming soon)
   - Auto-send emails via SMTP
   - Track opens/replies
   - Follow-up sequences

3. **CRM integration** (Future)
   - Sync to HubSpot/Salesforce
   - Full pipeline tracking

## ❓ FAQ

**Q: Is this legal?**
A: Scraping publicly visible data is generally legal in many jurisdictions, but violates LinkedIn's ToS. Use for personal research/education only.

**Q: Will my account get banned?**
A: Unlikely if you follow the guidelines (max 50/day, human-like delays). Use at your own risk.

**Q: Can I scrape profiles instead of posts?**
A: Not implemented yet. Posts are safer (less detectable) and show active pain points.

**Q: Does it work with Sales Navigator?**
A: Not tested. Regular LinkedIn search should work fine.

**Q: Can I scrape other platforms?**
A: Twitter/X scraper coming next. IndiaMART scraper also planned.

---

**Ready to find leads automatically?**

```bash
python3 auto_pipeline.py
```
