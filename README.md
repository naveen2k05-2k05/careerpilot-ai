<<<<<<< HEAD
# CareerPilot AI

AI-powered Career Coach and Interview Preparation Platform.

## Quick Start (Windows)

```powershell
# 1. Backend setup (first time only)
cd backend
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# 2. Frontend setup (first time only)
cd ..\frontend
npm install

# 3. Start both servers
cd ..
.\start.ps1
```

Open **http://127.0.0.1:5173** and click **Continue as Demo User** — no Firebase required for local dev.

| URL | Description |
|-----|-------------|
| http://127.0.0.1:5173 | React app |
| http://127.0.0.1:8000/docs | API documentation |
| http://127.0.0.1:8000/health | Health check |

## Features

- Authentication (Firebase + **Demo Mode** for local dev)
- Dashboard with resume score, interview readiness, recommendations
- Resume Analyzer (PDF/DOCX upload, ATS scoring, skill extraction)
- Career Coach (role-based roadmaps)
- Job Match Analyzer (with optional save to applications)
- AI Interview Coach & Mock Interview with feedback
- Project Recommendations with portfolio tracking
- Learning Tracker & Job Application Tracker
- Analytics Dashboard with Chart.js visualizations

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Tailwind CSS, React Router, Chart.js |
| Backend | Python FastAPI |
| Database | SQLite (local) / PostgreSQL (production) |
| Auth | Firebase Authentication + Dev bypass |
| AI | Google Gemini API (mock fallback when no key) |

## Environment Variables

### Backend (`backend/.env`)

```env
DATABASE_URL=sqlite:///./careerpilot.db
DEV_MODE=true
DEV_AUTH_TOKEN=careerpilot-dev-local-token
GEMINI_API_KEY=           # optional — uses mock AI without it
FIREBASE_PROJECT_ID=      # required for production auth
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Frontend (`frontend/.env`)

```env
VITE_API_URL=http://127.0.0.1:8000/api
VITE_DEV_MODE=true
VITE_DEV_AUTH_TOKEN=careerpilot-dev-local-token
VITE_FIREBASE_*=          # required for production auth
```

## Production Setup

1. Set `DEV_MODE=false` on backend
2. Configure real Firebase credentials (frontend + backend)
3. Set `GEMINI_API_KEY` for live AI responses
4. Use PostgreSQL: `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/careerpilot`
5. Deploy frontend to **Netlify**, backend to **Render**

## Manual Start

**Backend:**
```powershell
cd backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Frontend:**
```powershell
cd frontend
npm run dev
```

## License

MIT
=======
# careerpilot-ai
>>>>>>> a9c378a49608ce6c388b7667d0ce4c2af51e0c72
