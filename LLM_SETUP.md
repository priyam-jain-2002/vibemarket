# LLM Setup Guide - Use Any AI You Have Access To!

Your lead generator now supports **multiple AI providers**. Use whichever API key you already have!

---

## 🎯 Quick Start with YOUR LLM

### Option 1: Anthropic Claude (Recommended)

**Why:** Best quality for lead analysis, nuanced understanding, vibe-matching
**Cost:** ~$0.008/lead ($5 free credits = 500-1000 leads)
**Setup:** 2 minutes

```bash
# 1. Get API key
# Go to: https://console.anthropic.com/
# Sign up (free $5 credits)
# Create API key

# 2. Install
pip install anthropic pyyaml python-dotenv

# 3. Configure
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> .env

# 4. Run
python3 my_leads.py
```

---

### Option 2: OpenAI GPT-4 (If you already have access)

**Why:** Familiar, widely supported, good quality
**Cost:** ~$0.01/lead
**Setup:** 2 minutes

```bash
# 1. Get API key
# Go to: https://platform.openai.com/api-keys
# Create new secret key

# 2. Install
pip install openai pyyaml python-dotenv

# 3. Configure
echo "OPENAI_API_KEY=sk-proj-your-key-here" >> .env

# 4. Run (auto-detects OpenAI)
python3 my_leads.py
```

**Or force OpenAI:**
```bash
echo "LLM_PROVIDER=openai" >> .env
python3 my_leads.py
```

---

### Option 3: Google Gemini (FREE!)

**Why:** Free tier available, Google ecosystem
**Cost:** FREE for first 60 requests/minute!
**Setup:** 2 minutes

```bash
# 1. Get API key
# Go to: https://makersuite.google.com/app/apikey
# Create API key

# 2. Install
pip install google-generativeai pyyaml python-dotenv

# 3. Configure
echo "GEMINI_API_KEY=your-key-here" >> .env

# 4. Run
python3 my_leads.py
```

**This is FREE for personal use!** Perfect if you don't want to pay for API calls.

---

### Option 4: Ollama (Local/Offline/FREE)

**Why:** 100% free, runs on your computer, private, no API calls
**Cost:** FREE (uses your CPU/GPU)
**Setup:** 5 minutes

```bash
# 1. Install Ollama
# Mac:
brew install ollama

# Linux:
curl https://ollama.ai/install.sh | sh

# Windows:
# Download from: https://ollama.ai/download

# 2. Start Ollama server
ollama serve

# 3. Download a model (in new terminal)
ollama pull llama2        # or: mistral, codellama, etc.

# 4. Configure (optional)
echo "OLLAMA_MODEL=llama2" >> .env

# 5. Run
python3 my_leads.py
```

**Note:** Local models have lower quality than cloud APIs, but they're FREE and private!

---

## 🔍 Check Which LLMs You Have Available

Run this to see what's configured:

```bash
python3 -c "from processors.llm_backends import list_available_backends; print('\n'.join(f'{k}: {\"✅\" if v else \"❌\"}' for k,v in list_available_backends().items()))"
```

Or run the full test:
```bash
python3 processors/llm_backends.py
```

Output:
```
🔍 Checking available LLM backends...

Claude          ✅ Available
OpenAI          ❌ Not configured
Gemini          ✅ Available
Ollama          ❌ Not configured

✅ Auto-selected backend: Claude
```

---

## 📊 LLM Comparison

| Provider | Cost/Lead | Quality | Speed | Free Tier | Best For |
|----------|-----------|---------|-------|-----------|----------|
| **Claude** | $0.008 | ⭐⭐⭐⭐⭐ | Fast | $5 credits | Best overall quality |
| **GPT-4** | $0.01 | ⭐⭐⭐⭐ | Fast | No | Familiar, reliable |
| **Gemini** | FREE! | ⭐⭐⭐⭐ | Fast | Yes (60/min) | Free tier users |
| **Ollama** | FREE | ⭐⭐⭐ | Medium | N/A | Privacy, offline |

---

## 🎯 Recommended Setup

**For Testing (Today):**
```bash
# Use Gemini (it's free!)
pip install google-generativeai pyyaml python-dotenv
# Add GEMINI_API_KEY to .env
python3 my_leads.py
```

**For Production (Best Quality):**
```bash
# Use Claude
pip install anthropic pyyaml python-dotenv
# Add ANTHROPIC_API_KEY to .env
python3 my_leads.py
```

**For High Volume (Cost-Conscious):**
```bash
# Use Gemini Pro (free) or Ollama (local)
pip install google-generativeai pyyaml python-dotenv
# Add GEMINI_API_KEY to .env
python3 my_leads.py
```

---

## ⚙️ Advanced: Force Specific Provider

Edit your `.env`:

```bash
# Force specific provider (overrides auto-detection)
LLM_PROVIDER=claude       # or: openai, gemini, ollama

# Provider-specific settings
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-sonnet-4-20250514

OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4-turbo-preview

GEMINI_API_KEY=...
GEMINI_MODEL=gemini-pro

OLLAMA_MODEL=llama2
```

---

## 🔄 Switch Between LLMs

You can easily switch:

```bash
# Try Claude
echo "LLM_PROVIDER=claude" >> .env
python3 my_leads.py

# Try OpenAI
echo "LLM_PROVIDER=openai" >> .env
python3 my_leads.py

# Try Gemini
echo "LLM_PROVIDER=gemini" >> .env
python3 my_leads.py

# Auto-detect (removes provider preference)
sed -i '' '/LLM_PROVIDER/d' .env
python3 my_leads.py
```

---

## 💡 Which Should You Use?

**Start with what you have:**

- ✅ **Have OpenAI API key?** → Use it!
- ✅ **Have Google account?** → Get free Gemini!
- ✅ **Want best quality?** → Get Claude ($5 free)
- ✅ **Want 100% free?** → Install Ollama locally

**The system works with ALL of them.** Choose based on what you have access to.

---

## 🧪 Test Your Setup

After configuring, test it works:

```bash
# Test LLM backend
python3 processors/llm_backends.py

# Test with sample leads
python3 example_usage.py

# Check results
ls -la data/messages/
cat data/messages/batch_*/A+_*.txt
```

If you see personalized messages, it's working! 🎉

---

## 🆘 Troubleshooting

### "No LLM backend available"
→ Install at least one: `pip install anthropic` (or openai, or google-generativeai)
→ Add API key to `.env`

### "API key not found"
→ Check `.env` file has the right key for your provider
→ Make sure it's not commented out (#)

### "Rate limit exceeded"
→ You hit API limits
→ Wait a minute or switch to another provider

### "Poor quality results"
→ Local models (Ollama) have lower quality
→ Switch to Claude or GPT-4 for best results

---

## 💰 Cost Comparison (100 leads)

| Provider | Cost | Quality | Notes |
|----------|------|---------|-------|
| Gemini | **$0** | ⭐⭐⭐⭐ | FREE (60 requests/min limit) |
| Ollama | **$0** | ⭐⭐⭐ | FREE (uses your CPU/GPU) |
| Claude | **$0.80** | ⭐⭐⭐⭐⭐ | Best quality, $5 free credits |
| GPT-4 | **$1.00** | ⭐⭐⭐⭐ | Good quality, familiar |

---

## 🚀 Start Now

**If you already have an API key:**
```bash
# 1. Add to .env
echo "YOUR_PROVIDER_API_KEY=your-key" >> .env

# 2. Install package
pip install anthropic  # or: openai, google-generativeai

# 3. Run
python3 my_leads.py
```

**If you don't have any:**
```bash
# Get FREE Gemini API key (2 minutes)
# https://makersuite.google.com/app/apikey

pip install google-generativeai pyyaml python-dotenv
echo "GEMINI_API_KEY=your-key" >> .env
python3 my_leads.py
```

**You're 2 minutes from generating leads with ANY LLM you have!** 🎯
