# 🚀 CareerPilot AI

> Full-stack career development platform for resume analysis, career planning, interview preparation, job tracking, learning progress, and personalized career recommendations.

<p align="center">
  <img src="https://img.shields.io/badge/React-TypeScript-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/Tailwind-CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Firebase-Authentication-FFCA28?style=for-the-badge&logo=firebase&logoColor=black" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
</p>

---

## Overview

**CareerPilot AI** is a full-stack career development platform designed to help students, freshers, and professionals improve their job readiness through a centralized career preparation workflow.

Instead of managing resumes, interview preparation, career planning, projects, and job applications separately, CareerPilot AI brings these capabilities together into one platform.

### What it solves

| Career Challenge | CareerPilot AI |
|---|---|
| Improving resume quality | ATS scoring & resume analysis |
| Identifying skill gaps | Skill extraction & missing-skill detection |
| Planning a career path | Personalized career roadmaps |
| Preparing for interviews | HR, technical & scenario-based practice |
| Practicing interviews | Interactive mock interviews |
| Finding suitable projects | Role-based project recommendations |
| Tracking learning progress | Skills, courses & projects tracker |
| Managing applications | Job application pipeline |
| Measuring progress | Career analytics dashboard |

---

## How It Works

```text
                    ┌─────────────────────┐
                    │    User Profile     │
                    │   Career Objective  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Resume Analyzer   │
                    │  ATS + Skill Gaps   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Career Coach     │
                    │ Skills + Roadmaps   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Project Recommend.  │
                    │ Portfolio Projects  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Interview Prep      │
                    │ HR + Technical      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Mock Interview    │
                    │ Questions + Feedback │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Job Match &       │
                    │ Application Tracker │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Career Analytics    │
                    │ Progress + Insights │
                    └─────────────────────┘



careerpilot-ai/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── start.ps1
├── .gitignore
├── LICENSE
└── README.md

📄 License
MIT License
