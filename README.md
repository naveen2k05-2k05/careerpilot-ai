# 🚀 CareerPilot AI

### AI-Powered Career Coaching & Interview Preparation Platform

CareerPilot AI is a full-stack career development platform that helps **students, freshers, and professionals** improve job readiness through resume analysis, career roadmaps, interview preparation, project recommendations, learning tracking, and job application management.

<p align="center">

**Resume Analysis** • **Career Planning** • **Interview Preparation** • **Job Tracking** • **Analytics**

</p>

---

## 🌐 Live Demo

**[Launch CareerPilot AI →](https://pilotyourcareer.netlify.app/login)**

> ⚠️ Development/testing deployment. Some features may use mock data, development authentication, or simulated AI responses.

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │        USER         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │   React + TypeScript      │
                    │      Frontend UI          │
                    └─────────────┬─────────────┘
                                  │
                             REST / JSON
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │       FastAPI Backend     │
                    │                           │
                    │ Resume • Jobs • Interview │
                    │ Analytics • Recommendations│
                    └───────┬───────────┬───────┘
                            │           │
                 ┌──────────┘           └──────────┐
                 ▼                                 ▼
        ┌────────────────┐                ┌─────────────────┐
        │ Firebase Auth  │                │   SQLAlchemy    │
        │                │                │      ORM        │
        │ Google OAuth   │                └────────┬────────┘
        └────────────────┘                         │
                                                   ▼
                                      ┌────────────────────────┐
                                      │ SQLite / PostgreSQL    │
                                      └───────────┬────────────┘
                                                  │
                                                  ▼
                                      ┌────────────────────────┐
                                      │ Career Analytics &     │
                                      │ Recommendation Engine  │
                                      └────────────────────────┘
