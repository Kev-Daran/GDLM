# JobWeaver 

AI-powered Chrome extension that analyzes your resume against job postings and finds relevant professionals to connect with - all in one click.

##  What It Does

1. **Paste a job description** → Get instant resume match score + improvement tips
2. **Auto-finds professionals** at that company in that role
3. **Get LinkedIn profiles** to network and land referrals

##  Quick Start

### Prerequisites
- Chrome, Edge, or any Chromium-based browser
- That's it!

### Installation

1. **Download the extension**
   ```bash
   git clone https://github.com/yourusername/jobweaver.git
   cd jobweaver
   ```

2. **Load in Chrome**
   - Open Chrome and go to `chrome://extensions/`
   - Enable **Developer mode** (toggle in top-right)
   - Click **Load unpacked**
   - Select the `chrome_extension` folder
   - Done! 

3. **Pin the extension**
   - Click the puzzle piece icon in Chrome toolbar
   - Pin JobWeaver for easy access

## 📖 How to Use

### First Time Setup
1. Click the extension icon
2. Upload your resume (PDF) using the 📄 button

### Analyze a Job
1. Copy any job description
2. Paste it into JobWeaver
3. Get instant:
   -  Resume match score (0-100%)
   -  Specific improvement recommendations
   -  LinkedIn profiles of professionals at that company

### Find Professionals
Just type: `Find [role] at [company], [country]`

Example: `Find Data Scientists at Google`

##  Features

- **Smart Resume Analysis** - Cosine similarity matching with actionable feedback
- **Automated Networking** - Finds relevant LinkedIn profiles instantly
- **Multi-Agent System** - Powered by Google ADK agents working together
- **Chat Persistence** - Your conversations stay until browser restart

##  Architecture

```
Chrome Extension (Frontend)
    ↓
Google Cloud Run (Backend API)
    ↓
Multi-Agent System (Google ADK)
    ├── Root Agent (Orchestrator)
    ├── Resume Support Agent
    └── Searcher Agent (LinkedIn)
```

##  Tech Stack

**Frontend:**
- Vanilla JavaScript
- Chrome Extensions API
- Chrome Storage API

**Backend:**
- FastAPI (Python)
- Google ADK (Agent Development Kit)
- scikit-learn (Resume matching)
- pdfplumber (Resume parsing)

**Infrastructure:**
- Docker
- Google Cloud Run (Serverless)
- Google Custom Search API

## 📝 Example Use Case

**Scenario:** You find a Machine Learning Engineer role at Netflix

**You do:** Paste the job description into JobWeaver

**JobWeaver does:**
1. Analyzes your resume → "78% match"
2. Suggests adding "MLOps experience" and "Recommendation systems"
3. Finds 5 ML Engineers at Netflix with LinkedIn URLs
4. Provides networking message templates

**Result:** You know exactly how to improve your resume AND who to reach out to for referrals.


## 🔮 Future Improvements

- [ ] Persistent resume storage (Google Cloud Storage)
- [ ] User based storage
- [ ] Auto job description extraction from websites


