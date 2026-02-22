# Vibe-Leads: Complete Workflow Guide

## 🎯 Current Flows (Working TODAY)

### Flow 1: Manual Lead Processing (CLI)
**Status:** ✅ Fully Working

```
1. Collect Leads (Manual)
   ├─ Find leads on LinkedIn/IndiaMART
   ├─ Copy their post/requirement text
   └─ Save: name, title, company, content, URL

2. Add to Script
   ├─ Open my_leads.py
   ├─ Paste lead info in my_leads list
   └─ Save file

3. AI Analysis (Automated)
   ├─ Run: python3 my_leads.py
   ├─ Claude analyzes each lead
   │   ├─ Detects pain points
   │   ├─ Scores quality (A+/A/B/C)
   │   ├─ Assesses urgency
   │   ├─ Checks authority
   │   └─ Calculates specificity
   └─ Auto-rejects C leads

4. Message Generation (Automated)
   ├─ For A+/A leads only
   ├─ Analyzes their communication style
   ├─ Matches their vibe (casual/formal/urgent)
   ├─ Generates personalized outreach
   └─ References specific pain points

5. Export Results (Automated)
   ├─ CSV: data/qualified/qualified_*.csv
   ├─ JSON: data/qualified/qualified_*.json
   └─ Individual .txt files: data/messages/batch_*/
       ├─ A+_01_Name.txt (ready to send)
       ├─ A_02_Name.txt
       └─ SUMMARY.txt

6. Manual Outreach
   ├─ Review messages in data/messages/
   ├─ Customize if needed (optional)
   ├─ Copy-paste to LinkedIn/Email
   └─ Track responses manually
```

**Time:** 15 minutes for 20 leads
**Output:** 4-5 qualified leads with ready messages

---

### Flow 2: Web UI Lead Management (Phase 1)
**Status:** ✅ Built, Ready to Use

```
1. Add Lead via Web Form
   ├─ Go to: http://localhost:8000/leads/new/form
   ├─ Fill form: name, title, company, content, URL
   └─ Click "Add Lead"

2. View Dashboard
   ├─ See total leads, analyzed today, qualified count
   ├─ View recent leads with scores
   └─ See conversion funnel visualization

3. Analyze Lead (One-Click)
   ├─ Click "Analyze" button on any lead
   ├─ Claude processes in real-time (~5 sec)
   └─ Results appear: score, pain points, message

4. Review Lead Details
   ├─ Open lead detail page
   ├─ See full analysis:
   │   ├─ Original post
   │   ├─ Pain points detected
   │   ├─ Urgency/Authority scores
   │   └─ Generated outreach message
   └─ Activity timeline shows all changes

5. Manage Lifecycle
   ├─ Change status via dropdown:
   │   New → Analyzed → Contacted → Replied → Won/Lost
   ├─ Add tags for organization
   ├─ Add notes on interactions
   └─ All tracked in database

6. Filter & Search
   ├─ Search by: name, company, content keywords
   ├─ Filter by: score (A+/A/B/C)
   ├─ Filter by: status (new, contacted, etc.)
   └─ Filter by: source (manual, LinkedIn, etc.)

7. View Analytics
   ├─ Score distribution (how many A+/A/B/C)
   ├─ Source performance (which sources = quality)
   ├─ Reply rates
   └─ Conversion funnel
```

**Time:** Real-time, instant feedback
**Output:** Full lead database with lifecycle tracking

---

## 🔮 Future Flows (Planned)

### Flow 3: Automated LinkedIn Scraping (Phase 2)
**Status:** 🚧 Planned for Week 3

```
1. Configure Scraper (Web UI)
   ├─ Set search query: "order management chaos India"
   ├─ Set filters:
   │   ├─ Date: Last 7 days
   │   ├─ Location: India
   │   ├─ Job titles: Owner, Director, Founder
   │   └─ Industries: Manufacturing, Distribution
   └─ Set limit: 50 leads/session

2. Run Scraper (Automated)
   ├─ Playwright launches browser
   ├─ Logs into LinkedIn (your credentials)
   ├─ Searches posts with keywords
   ├─ Extracts:
   │   ├─ Name, title, company
   │   ├─ Post content
   │   ├─ Post URL
   │   └─ Engagement metrics
   ├─ Rate limiting (3-8 sec delays)
   └─ Saves to database with status='new'

3. Auto-Analysis (Batch)
   ├─ After scraping completes
   ├─ Claude processes all new leads
   ├─ Updates with scores and messages
   └─ Sends notification: "12 new qualified leads"

4. Review & Approve (Manual)
   ├─ Check qualified leads in dashboard
   ├─ Review generated messages
   ├─ Edit if needed
   └─ Mark ready to send

5. Schedule Daily Runs (Cron)
   ├─ 9 AM: Scrape 50 new leads
   ├─ 9:05 AM: Auto-analyze all
   ├─ 9:10 AM: Notification with count
   └─ You review when convenient
```

**Time:** 5 minutes scraping, instant analysis, 5 min review
**Output:** 10-15 qualified leads daily on autopilot

---

### Flow 4: Email Outreach (Phase 3)
**Status:** 🚧 Planned for Week 4

```
1. Compose Email (Web UI)
   ├─ Lead detail page → "Send Email" button
   ├─ Email modal opens with:
   │   ├─ Pre-filled subject
   │   ├─ Generated message body
   │   ├─ Your signature
   └─ Edit/customize as needed

2. Preview & Send
   ├─ Preview email
   ├─ Check for typos
   ├─ Click "Send"
   └─ SMTP sends email

3. Automated Tracking
   ├─ Email logged in database
   ├─ Lead status → "contacted"
   ├─ Timestamp recorded
   └─ Appears in email history

4. Reply Detection (Manual for now)
   ├─ When lead replies
   ├─ Click "Mark as Replied"
   ├─ Add reply content (optional)
   └─ Lead status → "replied"

5. Bulk Sending
   ├─ Select multiple A+ leads
   ├─ Click "Bulk Send"
   ├─ Queue emails (1 per 30 sec)
   └─ Avoid spam flags

6. Follow-up Sequences (Future)
   ├─ If no reply after 3 days → Send follow-up
   ├─ If no reply after 7 days → Send final follow-up
   ├─ If replied → Move to "replied" status
   └─ Smart scheduling (not weekends)
```

**Time:** 1 minute per email, bulk = 5 min for 10 leads
**Output:** Tracked outreach, automatic follow-ups

---

### Flow 5: Full Automation (Phase 2+3+4)
**Status:** 🚧 Planned for Weeks 3-5

```
MORNING (9 AM) - Automated
├─ LinkedIn scraper runs (50 new leads)
├─ Claude analyzes all (10-15 qualified)
├─ Notification: "12 new A+ leads ready"
└─ You get morning coffee ☕

YOU (9:30 AM) - 10 minutes
├─ Open dashboard
├─ Review 12 qualified leads
├─ Edit 2-3 messages
├─ Click "Bulk Send" → Queue 12 emails
└─ Go about your day

SYSTEM (9:35 AM - 5 PM) - Automated
├─ Sends 12 emails (1 per 30 sec)
├─ Tracks delivery
├─ Updates lead statuses
└─ Waits for replies

YOU (Evening) - 5 minutes
├─ Check replies (3-4 expected)
├─ Respond to interested leads
├─ Schedule calls
└─ Mark won/lost

SYSTEM (Next 3 days) - Automated
├─ Sends follow-ups to non-responders
├─ Tracks engagement
├─ Alerts on new replies
└─ Updates analytics

WEEKLY REVIEW - 15 minutes
├─ View analytics dashboard
├─ Check: Which sources = best leads?
├─ Check: Which pain points = most replies?
├─ Adjust scraper queries
└─ Refine message templates
```

**Time:** 30 min/week active, rest automated
**Output:** 50-100 qualified leads/month, 10-20 meetings

---

## 📊 Flow Comparison

| Flow | Status | Time/Day | Leads/Day | Qualified | Setup Time |
|------|--------|----------|-----------|-----------|------------|
| **Manual CLI** | ✅ Today | 15 min | 20 | 4-5 | 5 min |
| **Web UI** | ✅ Ready | 20 min | 20 | 4-5 | 10 min |
| **Auto Scraper** | 🚧 Week 3 | 10 min | 50 | 10-15 | 30 min |
| **Email Auto** | 🚧 Week 4 | 15 min | 50 | 10-15 | 20 min |
| **Full Auto** | 🚧 Week 5 | 30 min/week | 250/week | 50-75/week | 1 hour |

---

## 🔄 Detailed Flow Examples

### Example 1: Solo Founder (Today - Manual CLI)

**Monday Morning (15 min):**
```
9:00 AM - Find 10 leads on LinkedIn
          Search: "inventory tracking chaos" + India
          Copy 10 posts with clear pain points

9:10 AM - Add to my_leads.py, run: python3 my_leads.py
          System analyzes → 2 A+ leads, 1 A lead

9:12 AM - Open data/messages/batch_*/
          Read 3 generated messages
          Customize slightly

9:15 AM - Send 3 messages on LinkedIn
          Track in spreadsheet

Result: 3 quality messages sent, expect 1 reply
```

### Example 2: Sales Team (Web UI)

**Team Lead:**
```
1. Configure scraper queries (one-time)
2. Review qualified leads dashboard daily
3. Assign leads to team members
4. Track conversion rates
```

**Sales Rep:**
```
1. Login to dashboard
2. See assigned leads (filtered by rep)
3. Review AI analysis
4. Customize messages
5. Send emails from system
6. Update status when replied
7. Track in pipeline
```

**Manager:**
```
1. View analytics dashboard
2. Check: Reply rates, conversion rates
3. See: Which sources = best ROI
4. Adjust: Scraper queries, message templates
5. Export: Weekly reports
```

### Example 3: Agency (Full Automation)

**Setup (1 hour, one-time):**
```
1. Configure 5 scraper queries (different industries)
2. Set up email templates
3. Configure follow-up sequences
4. Connect to CRM (HubSpot/Salesforce)
5. Set daily limits (avoid spam)
```

**Daily (30 min):**
```
Morning:
  - Review 50 new qualified leads
  - Approve/edit 10 messages
  - Send bulk email queue

Afternoon:
  - Check replies (15-20 expected)
  - Respond to interested leads
  - Schedule demos

Evening:
  - Review analytics
  - Adjust strategies
```

**Output:**
- 250 leads/week analyzed
- 50-75 qualified/week
- 10-15 meetings/week
- 2-4 deals/week

---

## 🎯 Flow Selection Guide

**Use Manual CLI if:**
- ✅ Starting today
- ✅ Less than 50 leads/week
- ✅ Want full control
- ✅ Don't need web UI

**Use Web UI if:**
- ✅ Want visual dashboard
- ✅ Track lead lifecycle
- ✅ Need analytics
- ✅ Team collaboration

**Use Auto Scraper if:**
- ✅ Process 100+ leads/week
- ✅ Want automated collection
- ✅ Have LinkedIn account
- ✅ Save time on finding leads

**Use Email Auto if:**
- ✅ Send 50+ emails/week
- ✅ Want tracking
- ✅ Need follow-up sequences
- ✅ Measure reply rates

**Use Full Auto if:**
- ✅ Running at scale (500+ leads/month)
- ✅ Sales team with quotas
- ✅ Need complete pipeline
- ✅ ROI-focused optimization

---

## 🚀 Getting Started with Each Flow

### Start with Manual CLI (Today):
```bash
python3 my_leads.py
```

### Add Web UI (10 min setup):
```bash
python3 main.py
# Open: http://localhost:8000
```

### Add Scraper (Week 3):
```bash
# I'll build this for you next
# Adds automated LinkedIn lead collection
```

### Add Email (Week 4):
```bash
# Configure SMTP settings
# Send directly from web UI
```

---

## 💡 Pro Tips for Each Flow

**Manual CLI:**
- Process leads daily (don't batch 100s)
- Quality > Quantity
- Review messages before sending

**Web UI:**
- Use filters to focus on A+ leads
- Track status changes religiously
- Review analytics weekly

**Auto Scraper:**
- Start with strict filters (quality over quantity)
- Test with small batches first
- Respect LinkedIn rate limits

**Email Auto:**
- Warm up email sending (start with 10/day)
- Always customize first message
- Track reply rates to optimize

---

**Which flow do you want to use first?**

Today: Manual CLI → Tomorrow: Web UI → Next Week: Auto Scraper?
