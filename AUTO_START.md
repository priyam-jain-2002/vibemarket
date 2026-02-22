# Start Automated Lead Generation (5 Minutes)

## The Complete Loop

```
LinkedIn → AI Analysis → Personalized Messages
(Automated)     (Automated)      (Ready to send)
```

## Quick Start

### 1. Install Playwright (one-time)

```bash
pip install playwright beautifulsoup4
playwright install chromium
```

### 2. Add LinkedIn Credentials

Edit `.env`:
```bash
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password
LEAD_SEARCH_QUERY=order management chaos India
LEAD_LIMIT=20
```

### 3. Run Pipeline

```bash
python3 auto_pipeline.py
```

### 4. Get Messages

Check `data/messages/batch_*/` for ready-to-send outreach.

## What Happens

1. **Logs into LinkedIn** with your credentials
2. **Searches posts** for your keywords
3. **Extracts leads** (name, title, company, content)
4. **AI analyzes** each lead (score A+ to C)
5. **Generates messages** for qualified leads (A+/A only)
6. **Saves to files** - ready to copy-paste

## Example Output

```
🤖 AUTOMATED LEAD GENERATION PIPELINE

📍 STEP 1: FINDING LEADS
   ✅ Found 18 leads

📍 STEP 3: AI ANALYSIS
   ✅ Qualified: 7 leads (2 A+, 5 A)

🎯 PIPELINE COMPLETE
   Check 'data/messages/' for outreach!
```

## Safety Notes

- Max 20-50 leads per day (avoid detection)
- Run once daily (not continuously)
- You assume responsibility for LinkedIn ToS compliance
- See [SCRAPER_SETUP.md](SCRAPER_SETUP.md) for full details

---

**That's it!** One command finds leads and generates personalized messages automatically.
