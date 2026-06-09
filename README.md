# 🚀 CareerPilot AI

### AI-Powered Career Coaching & Interview Preparation Platform

CareerPilot AI is a full-stack career development platform designed to help students, freshers, and professionals improve their job readiness through resume analysis, interview preparation, career roadmaps, learning progress tracking, and job application management.

The platform provides an end-to-end career growth experience by combining career analytics, resume evaluation, interview practice, and personalized recommendations within a modern web application.

---

🌐 Live Demo

Development Deployment (Netlify)

🔗 Live Application: https://pilotyourcareer.netlify.app/login

⚠️ This is currently a development/testing deployment. Some features may use mock data, development authentication, or simulated AI responses while production integrations are being finalized.

Demo Mode Available:

Continue as Demo User
Test Dashboard Features
Resume Analysis Workflow
Interview Preparation Modules
Analytics Dashboard

## 🌟 Key Features

### 🔐 Authentication

* Firebase Authentication
* Google Sign-In
* Secure Session Management
* Demo Login for Local Development

### 📊 Career Dashboard

* Resume Score Analysis
* Interview Readiness Score
* Skills Progress Tracking
* Application Statistics
* Personalized Recommendations

### 📄 Resume Analyzer

* PDF & DOCX Resume Upload
* Skill Extraction
* ATS Score Calculation
* Missing Skills Detection
* Resume Improvement Suggestions

### 🎯 Career Coach

Generate personalized career roadmaps for:

* Software Engineer
* Data Analyst
* Data Scientist
* AI Engineer
* Full Stack Developer

Provides:

* Required Skills
* Learning Roadmaps
* Recommended Projects
* Preparation Timeline

### 💼 Job Match Analyzer

Compare Resume vs Job Description

Outputs:

* Match Percentage
* Missing Skills
* Skill Gap Analysis
* Action Plan

### 🎤 Interview Preparation

* HR Interview Questions
* Technical Questions
* Project-Based Questions
* Scenario-Based Questions

Difficulty Levels:

* Beginner
* Intermediate
* Advanced

### 🧠 Mock Interview Module

* Interactive Interview Simulation
* Follow-up Questions
* Realistic Interview Flow
* Performance Evaluation

### 📈 Interview Feedback Engine

Provides:

* Technical Score
* Communication Score
* Confidence Score
* Overall Rating
* Improvement Suggestions

### 🚀 Project Recommendation Engine

Project recommendations based on target career role.

Includes:

* Beginner Projects
* Intermediate Projects
* Advanced Projects

Each project includes:

* Description
* Technologies Used
* Difficulty Level
* Resume Impact

### 📚 Learning Tracker

Track:

* Skills Learned
* Courses Completed
* Projects Completed
* Interview Practice Sessions

### 📋 Job Application Tracker

Manage:

* Applied
* Under Review
* Interview Scheduled
* Rejected
* Offer Received

Store:

* Company Name
* Role
* Application Date
* Notes

### 📊 Analytics Dashboard

Visualize:

* Skill Growth
* ATS Improvement
* Interview Performance
* Job Application Success Rate

---

# 🏗️ System Architecture

Frontend (React + TypeScript)
↓
FastAPI REST APIs
↓
Firebase Authentication
↓
Database Layer (SQLite/PostgreSQL)
↓
Career Analytics & Recommendation Engine

---

# 🛠️ Tech Stack

## Frontend

| Technology   | Purpose               |
| ------------ | --------------------- |
| React.js     | User Interface        |
| TypeScript   | Type Safety           |
| Tailwind CSS | Responsive UI Styling |
| React Router | Client-Side Routing   |
| Chart.js     | Data Visualization    |
| Axios        | API Communication     |

---

## Backend

| Technology | Purpose              |
| ---------- | -------------------- |
| Python     | Core Language        |
| FastAPI    | REST API Development |
| SQLAlchemy | ORM                  |
| Pydantic   | Data Validation      |
| Uvicorn    | ASGI Server          |

---

## Database

| Environment | Database   |
| ----------- | ---------- |
| Development | SQLite     |
| Production  | PostgreSQL |

---

## Authentication

| Technology              | Purpose             |
| ----------------------- | ------------------- |
| Firebase Authentication | User Authentication |
| Google OAuth            | Social Login        |

---

## AI Layer

Current Version:

* Rule-Based Recommendation Engine
* Resume Analysis Logic
* Interview Evaluation Engine

Planned Enhancements:

* Google Gemini Integration
* LLM-Powered Career Coaching
* AI Resume Analysis
* AI Interview Feedback
* RAG-Based Knowledge Retrieval

---

# 🚀 Quick Start

## Backend Setup

```bash
cd backend

py -m venv venv

.\venv\Scripts\activate

pip install -r requirements.txt
```

## Frontend Setup

```bash
cd frontend

npm install
```

## Run Application

```bash
cd ..

.\start.ps1
```

---

# 🌐 Application URLs

| Service           | URL                          |
| ----------------- | ---------------------------- |
| Frontend          | http://127.0.0.1:5173        |
| API Documentation | http://127.0.0.1:8000/docs   |
| Health Check      | http://127.0.0.1:8000/health |

---

# ⚙️ Environment Variables

## Backend (.env)

```env
DATABASE_URL=sqlite:///./careerpilot.db

DEV_MODE=true

DEV_AUTH_TOKEN=careerpilot-dev-local-token

GEMINI_API_KEY=

FIREBASE_PROJECT_ID=

FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Frontend (.env)

```env
VITE_API_URL=http://127.0.0.1:8000/api

VITE_DEV_MODE=true

VITE_DEV_AUTH_TOKEN=careerpilot-dev-local-token

VITE_FIREBASE_API_KEY=

VITE_FIREBASE_AUTH_DOMAIN=

VITE_FIREBASE_PROJECT_ID=
```

---

# 🚀 Production Deployment

## Frontend

* Netlify

## Backend

* Render

## Database

* PostgreSQL

Production Checklist:

* Configure Firebase Authentication
* Add Gemini API Key
* Configure PostgreSQL Database
* Disable Development Mode
* Configure Environment Variables

---

# 🔮 Future Enhancements

* Gemini AI Integration
* AI Career Coach
* Resume Semantic Analysis
* AI Mock Interviews
* Personalized Learning Recommendations
* RAG-Based Knowledge Retrieval
* Voice-Based Interview Practice

---

## 📄 License

MIT License
