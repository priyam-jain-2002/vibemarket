# Vibe-Leads Setup Guide

## Phase 1: Web UI with Database ✅ COMPLETE

Congratulations! Phase 1 of your personal lead generator is complete. Here's what we built:

### 🎯 What's New

#### 1. **SQLite Database** (`storage/models.py`, `storage/database.py`)
- Full lead lifecycle tracking (new → analyzed → contacted → replied → won/lost)
- Lead analysis storage (scores, pain points, urgency, authority)
- Email send tracking
- Scraper session tracking
- Activity history for each lead
- **No complex setup required** - single file database at `data/vibe-leads.db`

#### 2. **Web Dashboard** (`web/`)
- **Dashboard** (`/dashboard`) - Overview stats, recent leads, conversion funnel
- **Leads List** (`/leads`) - Filterable table with search, score/status/source filters
- **Lead Detail** (`/leads/{id}`) - Full lead info, AI analysis, outreach message
- **Add Lead Form** (`/leads/new/form`) - Manual lead entry
- Built with **htmx** (no npm, no build step!)
- **Tailwind CSS** via CDN (no build required)

#### 3. **Smart Features**
- One-click AI analysis (analyzes lead with existing Claude processor)
- Lead status tracking with history
- Conversion funnel visualization
- Score distribution charts
- Tags for organization
- Email history (ready for Phase 3)

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install fastapi uvicorn[standard] sqlalchemy jinja2 python-multipart anthropic pyyaml python-dotenv
```

**Or install from requirements.txt:**
```bash
pip install -r requirements.txt
```

### Step 2: Set Up Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your-key-here
```

### Step 3: Run the Web Server

```bash
python main.py
```

**Or with custom port:**
```bash
python main.py --port 3000
```

### Step 4: Open Your Browser

Navigate to:
- **Dashboard:** http://localhost:8000/dashboard
- **Leads:** http://localhost:8000/leads
- **API Docs:** http://localhost:8000/docs

---

## 📋 How to Use

### Adding Leads Manually

1. Click **"➕ Add Lead"** in the navigation
2. Fill in the form:
   - **Name** (required)
   - **Title** and **Company** (helps with authority scoring)
   - **Lead Content** (MOST IMPORTANT - this is what Claude analyzes)
   - **Source URL** (LinkedIn post, etc.)
3. Click **"Add Lead"**

### Analyzing Leads

**Option 1: From Dashboard**
- New leads show an "Analyze" button
- Click to trigger AI analysis

**Option 2: From Lead Detail Page**
- Open any lead
- Click **"🤖 Analyze with AI"**
- Results appear instantly:
  - Score (A+, A, B, C)
  - Pain points detected
  - Urgency level
  - Authority assessment
  - Personalized outreach message

### Filtering & Searching

On the Leads page:
- **Search:** Name, company, or content keywords
- **Filter by Score:** A+, A, B, C
- **Filter by Status:** New, Analyzed, Contacted, etc.
- **Filter by Source:** Manual, LinkedIn, etc.

### Managing Lead Lifecycle

1. **Status Dropdown** on lead detail page
2. Change status: New → Analyzed → Contacted → Replied → Won/Lost
3. All changes tracked in activity timeline

### Viewing Analytics

Dashboard shows:
- **Total leads** (all time)
- **Analyzed today** (AI processing count)
- **Qualified leads** (A+/A scores)
- **Contacted this week**
- **Reply rate**
- **Conversion funnel** (visual pipeline)
- **Score distribution** (quality breakdown)

---

## 📁 Project Structure

```
vibe-leads/
├── data/
│   └── vibe-leads.db          # SQLite database (auto-created)
│
├── storage/
│   ├── models.py              # Database schema (NEW ✨)
│   ├── database.py            # CRUD operations (NEW ✨)
│   └── storage.py             # File exports (existing)
│
├── web/                       # Web UI (NEW ✨)
│   ├── main.py                # FastAPI app
│   ├── routes/
│   │   ├── dashboard.py       # Dashboard endpoints
│   │   └── leads.py           # Lead management
│   ├── templates/             # HTML templates (htmx)
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── leads_list.html
│   │   ├── lead_detail.html
│   │   └── lead_form.html
│   └── static/                # CSS/JS (minimal)
│
├── processors/
│   └── claude_processor.py    # AI analysis (unchanged)
│
├── config/                     # YAML configs (unchanged)
│   ├── company.yaml
│   ├── audience.yaml
│   └── pain_points.yaml
│
├── main.py                     # Web server entry point (NEW ✨)
├── example_usage.py            # CLI example (existing)
└── requirements.txt            # Updated dependencies
```

---

## 🔄 Backward Compatibility

✅ **Everything still works the old way!**

Your existing `example_usage.py` script still works:
```bash
python example_usage.py
```

File exports still happen (CSV, JSON, text files in `data/` folders).

The web UI is an **addition**, not a replacement.

---

## 🎨 Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **Backend** | FastAPI | Modern, fast, auto-docs |
| **Database** | SQLite | Zero-config, portable |
| **ORM** | SQLAlchemy | Easy migrations, flexible |
| **Frontend** | htmx | No build step, simple |
| **Styling** | Tailwind CSS (CDN) | No build required |
| **Templates** | Jinja2 | Python standard |

**Total build complexity:** ZERO (no npm, no webpack, no build step!)

---

## 🧪 Testing

### Test Database
```bash
python storage/models.py
# Creates database and shows tables
```

### Test CRUD Operations
```bash
python storage/database.py
# Creates test lead and shows stats
```

### Test Web App
```bash
python main.py
# Starts web server
```

---

## 🚧 What's Coming Next

### Phase 2: LinkedIn Scraper (Automation)
- Automated lead collection from LinkedIn
- Search by keywords ("order management chaos", etc.)
- Filter by location, industry, date
- Rate limiting and stealth mode
- Web UI to configure and run scraper

### Phase 3: Email Integration
- Send emails directly from the web UI
- SMTP configuration (Gmail, Outlook)
- Email tracking (sent, replied)
- Template system

### Phase 4: Analytics & Lifecycle
- Advanced analytics dashboard
- Time-series charts
- Source performance tracking
- A/B testing for messages

### Phase 5: Polish & Deployment
- Docker setup (one-command deployment)
- CLI tool for automation
- Tests (pytest)
- Deployment guides (Railway, Render, etc.)

---

## 💡 Tips

### Best Practices

1. **Add quality leads** - The AI is only as good as the input
2. **Use the "Lead Content" field** - This is what Claude analyzes
3. **Review generated messages** - Always customize before sending
4. **Track everything** - Use status changes and notes
5. **Start small** - Test with 5-10 leads before scaling

### Workflow Recommendation

1. **Morning:** Run scraper (Phase 2) to collect new leads
2. **Analyze in bulk:** Click through and analyze all new leads
3. **Review qualified leads:** Focus on A+ and A scores
4. **Customize messages:** Edit generated outreach
5. **Send emails:** (Phase 3) Send to qualified leads
6. **Track responses:** Update status when they reply
7. **Review analytics:** Check what's working

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'anthropic'"
```bash
pip install anthropic
```

### "Database file not found"
```bash
mkdir -p data
python main.py  # Auto-creates database
```

### "Port 8000 already in use"
```bash
python main.py --port 3000  # Use different port
```

### Web UI not loading
1. Check console for errors
2. Ensure all dependencies installed
3. Try: `python -m web.main`

---

## 📞 Support

- **Issues:** Open an issue on GitHub
- **Docs:** See README.md and INDUSTRY_LEVEL_PLAN.md
- **Config:** Edit YAML files in `config/` directory

---

## ✨ What You Can Do Right Now

1. ✅ **Run the web UI** - `python main.py`
2. ✅ **Add leads manually** - Test the form
3. ✅ **Analyze with AI** - See Claude score and generate messages
4. ✅ **Track lifecycle** - Move leads through pipeline
5. ✅ **View analytics** - See your conversion funnel

**Phase 1 is production-ready for manual lead management!**

Ready for Phase 2 (LinkedIn scraper)? Let's build it! 🚀
