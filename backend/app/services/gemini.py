import json
import re
from typing import Any

from app.config import get_settings

ROLES = [
    "Software Engineer",
    "Data Analyst",
    "AI Engineer",
    "Data Scientist",
    "Full Stack Developer",
]


def _get_model():
    settings = get_settings()
    if not settings.gemini_api_key:
        return None

    try:
        import google.generativeai as genai
    except ImportError:
        return None

    genai.configure(api_key=settings.gemini_api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def _parse_json_response(text: str) -> dict | list:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"[\[{].*[\]}]", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Failed to parse AI response as JSON")


def _mock_resume_analysis(resume_text: str) -> dict:
    skills = ["Python", "JavaScript", "SQL", "Git", "React"]
    found = [s for s in skills if s.lower() in resume_text.lower()]
    return {
        "ats_score": 72.0,
        "strengths": ["Clear structure", "Relevant technical skills", "Project experience"],
        "weaknesses": ["Missing quantified achievements", "Limited keywords for ATS"],
        "improvements": [
            "Add metrics to project outcomes",
            "Include role-specific keywords",
            "Optimize section headings for ATS parsers",
        ],
        "extracted_skills": found or ["Python", "Communication", "Problem Solving"],
        "missing_skills": ["Docker", "AWS", "System Design"],
    }


def analyze_resume(resume_text: str, target_role: str | None = None) -> dict:
    model = _get_model()
    if not model:
        return _mock_resume_analysis(resume_text)

    prompt = f"""Analyze this resume and return ONLY valid JSON with keys:
ats_score (0-100 number), strengths (array), weaknesses (array), improvements (array),
extracted_skills (array), missing_skills (array).
Target role: {target_role or 'general tech role'}

Resume:
{resume_text[:8000]}
"""
    response = model.generate_content(prompt)
    return _parse_json_response(response.text)


def generate_career_roadmap(target_role: str) -> dict:
    model = _get_model()
    if not model:
        return _mock_career_roadmap(target_role)

    prompt = f"""Create a career roadmap for {target_role}. Return ONLY valid JSON with:
required_skills (array of strings),
learning_roadmap (array of objects with phase, duration, topics),
recommended_courses (array of objects with name, platform, url),
recommended_projects (array of objects with title, description),
estimated_timeline (string like "6-9 months")
"""
    response = model.generate_content(prompt)
    return _parse_json_response(response.text)


def _mock_career_roadmap(target_role: str) -> dict:
    return {
        "required_skills": ["Python", "SQL", "Git", "Data Structures", "APIs"],
        "learning_roadmap": [
            {"phase": "Foundation", "duration": "4-6 weeks", "topics": ["Programming basics", "Git", "SQL"]},
            {"phase": "Core Skills", "duration": "8-10 weeks", "topics": ["Frameworks", "Testing", "Databases"]},
            {"phase": "Portfolio", "duration": "6-8 weeks", "topics": ["Projects", "Resume", "Interview prep"]},
        ],
        "recommended_courses": [
            {"name": f"{target_role} Fundamentals", "platform": "Coursera", "url": "https://coursera.org"},
            {"name": "System Design Basics", "platform": "Udemy", "url": "https://udemy.com"},
        ],
        "recommended_projects": [
            {"title": "Portfolio API", "description": "Build a REST API with auth and documentation"},
            {"title": "Analytics Dashboard", "description": "Visualize data with charts and filters"},
        ],
        "estimated_timeline": "6-9 months",
    }


def analyze_job_match(resume_text: str, job_description: str) -> dict:
    if not resume_text or not resume_text.strip():
        return {
            "match_percentage": 0.0,
            "match_breakdown": {"technical_skills": 0, "soft_skills": 0, "experience_level": 0},
            "missing_skills": [],
            "skill_gap_analysis": [],
            "action_plan": ["Upload a resume to get started with job match analysis"],
            "recommendation": "No resume available",
        }
    
    if not job_description or not job_description.strip():
        return {
            "match_percentage": 0.0,
            "match_breakdown": {"technical_skills": 0, "soft_skills": 0, "experience_level": 0},
            "missing_skills": [],
            "skill_gap_analysis": [],
            "action_plan": ["Provide a job description to analyze match"],
            "recommendation": "Job description required",
        }
    
    model = _get_model()
    if not model:
        return _mock_job_match_analysis(resume_text, job_description)

    prompt = f"""Analyze the match between resume and job. Return ONLY valid JSON with:
match_percentage (0-100 number),
match_breakdown (object with technical_skills, soft_skills, experience_level - all 0-100),
missing_skills (array of skill names),
skill_gap_analysis (array of objects with: skill, importance, current_level, learning_path, estimated_weeks),
action_plan (array of detailed action steps),
recommendation (brief hiring prospect summary)

Resume (first 4000 chars):
{resume_text[:4000]}

Job Description (first 4000 chars):
{job_description[:4000]}
"""
    response = model.generate_content(prompt)
    return _parse_json_response(response.text)


def _mock_job_match_analysis(resume_text: str, job_description: str) -> dict:
    """Generate contextual mock analysis based on actual resume and JD content."""
    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()
    
    tech_skills = {
        "python": 90, "javascript": 85, "react": 85, "nodejs": 80, "sql": 75,
        "aws": 70, "docker": 65, "kubernetes": 60, "git": 90, "api": 80,
        "rest": 75, "graphql": 60, "typescript": 80, "java": 75, "golang": 60,
    }
    
    soft_skills = ["leadership", "communication", "teamwork", "problem-solving", "agile"]
    
    match_score = 0
    found_technical = 0
    total_required = 0
    missing = []
    gap_analysis = []
    
    for skill, importance in tech_skills.items():
        if skill in jd_lower:
            total_required += 1
            if skill in resume_lower:
                found_technical += 1
                match_score += (importance / 100) * 0.6
            else:
                missing.append(skill.capitalize())
                gap_analysis.append({
                    "skill": skill.capitalize(),
                    "importance": "high" if importance >= 70 else "medium",
                    "current_level": "none",
                    "learning_path": f"Online course + small project",
                    "estimated_weeks": 4 if importance >= 70 else 2,
                })
    
    soft_match = sum(1 for s in soft_skills if s in resume_lower and s in jd_lower) / max(1, len([s for s in soft_skills if s in jd_lower]))
    match_score += soft_match * 0.2
    
    exp_years = 5 if "senior" in resume_lower else 2 if "junior" in resume_lower else 3
    exp_required = 5 if "senior" in jd_lower else 2 if "junior" in jd_lower else 3
    exp_match = min(1.0, exp_years / max(1, exp_required)) * 0.2
    match_score += exp_match
    
    final_match = min(100, max(0, (match_score / 1.0) * 100))
    
    return {
        "match_percentage": round(final_match, 1),
        "match_breakdown": {
            "technical_skills": round((found_technical / max(1, total_required)) * 100),
            "soft_skills": round(soft_match * 100),
            "experience_level": round(exp_match * 100),
        },
        "missing_skills": missing[:5],
        "skill_gap_analysis": gap_analysis[:5],
        "action_plan": [
            f"Priority 1: Learn {missing[0] if missing else 'required skills'} within {gap_analysis[0]['estimated_weeks'] if gap_analysis else 2} weeks" if missing else "You have strong technical alignment with this role",
            "Priority 2: Update resume with keywords from the job description",
            "Priority 3: Build a project showcasing top 3 required skills",
            "Priority 4: Prepare targeted answers for gaps during interviews",
            "Priority 5: Connect with current professionals in this role on LinkedIn",
        ],
        "recommendation": f"Strong match ({round(final_match)}%)! Consider applying." if final_match >= 70 else f"Good match ({round(final_match)}%). Address top {len(missing[:3])} skill gaps first." if final_match >= 50 else f"Moderate fit ({round(final_match)}%). Significant upskilling needed.",
    }


def generate_interview_questions(
    target_role: str,
    difficulty: str,
    question_types: list[str] | None = None,
) -> dict:
    types = question_types or ["hr", "technical", "project", "scenario"]
    model = _get_model()
    if not model:
        return _mock_interview_questions(target_role, difficulty, types)

    prompt = f"""Generate interview questions for {target_role} at {difficulty} level.
Types needed: {', '.join(types)}.
Return ONLY valid JSON with keys matching types (hr, technical, project, scenario), each an array of question strings.
Generate 3-5 questions per type.
"""
    response = model.generate_content(prompt)
    return _parse_json_response(response.text)


def _mock_interview_questions(target_role: str, difficulty: str, types: list[str]) -> dict:
    """Generate role and difficulty-specific interview questions."""
    questions: dict[str, list[str]] = {}
    
    # Role-specific question banks
    role_questions = {
        "Software Engineer": {
            "beginner": {
                "hr": [
                    "Tell me about yourself and your programming journey.",
                    "Why are you interested in software engineering?",
                    "What motivates you to write code?",
                    "Describe a time you learned a new technology quickly.",
                ],
                "technical": [
                    "What is the difference between a variable and a constant?",
                    "Explain what an API is in simple terms.",
                    "What are the basic data structures you know?",
                    "How would you explain object-oriented programming?",
                    "What is version control and why is it important?",
                ],
                "project": [
                    "Describe a simple project you've built.",
                    "What was the most challenging bug you fixed?",
                    "Walk me through your first coding project.",
                ],
                "scenario": [
                    "How would you approach learning a new programming language?",
                    "What would you do if your code isn't working and you don't know why?",
                    "How do you stay updated with new technologies?",
                ],
            },
            "intermediate": {
                "hr": [
                    "Tell me about a technical challenge you overcame.",
                    "How do you handle code reviews and feedback?",
                    "Describe your experience working in a team.",
                    "What's your approach to work-life balance in tech?",
                ],
                "technical": [
                    "Explain the difference between SQL and NoSQL databases.",
                    "What are RESTful APIs and how do they work?",
                    "Describe the concept of time complexity.",
                    "How would you optimize a slow database query?",
                    "Explain the MVC pattern and its benefits.",
                ],
                "project": [
                    "Walk me through your most complex project.",
                    "How did you handle scalability in your last project?",
                    "Describe a time you had to refactor legacy code.",
                ],
                "scenario": [
                    "How would you debug a production issue affecting users?",
                    "A feature request conflicts with system architecture. What do you do?",
                    "How do you prioritize technical debt vs new features?",
                ],
            },
            "advanced": {
                "hr": [
                    "Describe your leadership experience in technical projects.",
                    "How do you mentor junior developers?",
                    "Tell me about a time you influenced technical direction.",
                    "How do you handle disagreements about architecture decisions?",
                ],
                "technical": [
                    "Design a distributed system handling millions of users.",
                    "Explain the CAP theorem and its practical implications.",
                    "How would you implement a caching strategy at scale?",
                    "Describe microservices communication patterns and trade-offs.",
                    "What strategies would you use for zero-downtime deployments?",
                ],
                "project": [
                    "Describe the most complex system you've architected.",
                    "How did you ensure reliability in a high-traffic system?",
                    "Walk me through a major technical decision you made.",
                ],
                "scenario": [
                    "The system is down and affecting revenue. How do you respond?",
                    "How would you migrate a monolith to microservices?",
                    "Design a system for handling billions of events per second.",
                ],
            },
        },
        "Data Analyst": {
            "beginner": {
                "hr": [
                    "Tell me about your interest in data analysis.",
                    "Why do you want to work with data?",
                    "Describe your analytical thinking process.",
                ],
                "technical": [
                    "What is a LEFT JOIN in SQL?",
                    "Explain what a pivot table is and when to use it.",
                    "What's the difference between mean, median, and mode?",
                    "How would you identify outliers in a dataset?",
                    "What is data visualization and why is it important?",
                ],
                "project": [
                    "Describe a data analysis project you've completed.",
                    "Walk me through how you created a dashboard.",
                    "What tools have you used for data visualization?",
                ],
                "scenario": [
                    "How would you analyze sales trends for a retail company?",
                    "What would you do if your data has missing values?",
                    "How do you ensure data quality in your analysis?",
                ],
            },
            "intermediate": {
                "hr": [
                    "Describe a time your analysis influenced business decisions.",
                    "How do you communicate complex findings to non-technical stakeholders?",
                    "Tell me about a challenging data problem you solved.",
                ],
                "technical": [
                    "How would you identify customer churn using SQL?",
                    "Explain the difference between correlation and causation.",
                    "What is A/B testing and how do you analyze results?",
                    "How would you build a customer segmentation model?",
                    "Describe your experience with statistical hypothesis testing.",
                ],
                "project": [
                    "Walk me through a complex analysis that drove business value.",
                    "How did you handle conflicting data from multiple sources?",
                    "Describe a predictive model you built.",
                ],
                "scenario": [
                    "The CEO wants insights on customer behavior by tomorrow. How do you proceed?",
                    "How would you analyze the impact of a marketing campaign?",
                    "Two datasets show different results. How do you reconcile them?",
                ],
            },
            "advanced": {
                "hr": [
                    "How have you influenced data strategy at your organization?",
                    "Describe your experience building analytics teams.",
                    "Tell me about a time you identified a major business opportunity through data.",
                ],
                "technical": [
                    "Design a KPI framework for an e-commerce company.",
                    "How would you build a real-time analytics dashboard?",
                    "Explain your approach to predictive revenue forecasting.",
                    "Describe how you'd implement a data warehouse from scratch.",
                    "What's your strategy for handling petabyte-scale data?",
                ],
                "project": [
                    "Describe the most impactful analytics project you've led.",
                    "How did you design an end-to-end analytics solution?",
                    "Walk me through building a company-wide BI platform.",
                ],
                "scenario": [
                    "The company wants to become data-driven. Where do you start?",
                    "How would you measure the ROI of a new product feature?",
                    "Design an analytics system for real-time fraud detection.",
                ],
            },
        },
        "Data Scientist": {
            "beginner": {
                "hr": [
                    "What attracted you to data science?",
                    "Describe your background in statistics and programming.",
                    "How do you approach learning new ML algorithms?",
                ],
                "technical": [
                    "What is overfitting and how do you prevent it?",
                    "Explain the difference between supervised and unsupervised learning.",
                    "What is a confusion matrix?",
                    "How do you split data for training and testing?",
                    "What is feature engineering?",
                ],
                "project": [
                    "Describe a machine learning project you've built.",
                    "Walk me through your model building process.",
                    "What was the most challenging part of your ML project?",
                ],
                "scenario": [
                    "How would you approach a classification problem?",
                    "What would you do if your model has low accuracy?",
                    "How do you choose which algorithm to use?",
                ],
            },
            "intermediate": {
                "hr": [
                    "Describe a time your model created business value.",
                    "How do you explain ML models to non-technical stakeholders?",
                    "Tell me about a failed ML experiment and what you learned.",
                ],
                "technical": [
                    "Explain the bias-variance tradeoff.",
                    "How would you handle imbalanced datasets?",
                    "What is cross-validation and why is it important?",
                    "Describe different ensemble methods and when to use them.",
                    "How do you evaluate a regression model?",
                ],
                "project": [
                    "Walk me through a complex ML pipeline you built.",
                    "How did you deploy a model to production?",
                    "Describe your experience with feature selection.",
                ],
                "scenario": [
                    "Your model performs well in training but poorly in production. Why?",
                    "How would you build a recommendation system?",
                    "The business wants to understand why your model made a prediction. How do you explain it?",
                ],
            },
            "advanced": {
                "hr": [
                    "How have you led ML initiatives in your organization?",
                    "Describe your experience with MLOps and model governance.",
                    "Tell me about a time you innovated with ML.",
                ],
                "technical": [
                    "Design an end-to-end recommendation system at scale.",
                    "How would you implement real-time fraud detection?",
                    "Explain your approach to model monitoring and retraining.",
                    "Describe advanced techniques for handling data drift.",
                    "How would you build a multi-model ensemble system?",
                ],
                "project": [
                    "Describe the most complex ML system you've architected.",
                    "How did you scale ML models to handle millions of predictions?",
                    "Walk me through building an ML platform from scratch.",
                ],
                "scenario": [
                    "Design a complete ML infrastructure for a startup.",
                    "How would you implement A/B testing for ML models?",
                    "The model is biased against certain groups. How do you fix it?",
                ],
            },
        },
        "Full Stack Developer": {
            "beginner": {
                "hr": [
                    "Tell me about your web development journey.",
                    "Why are you interested in full-stack development?",
                    "What aspects of web development do you enjoy most?",
                ],
                "technical": [
                    "What's the difference between frontend and backend?",
                    "Explain what HTML, CSS, and JavaScript do.",
                    "What is a REST API?",
                    "How do browsers render a webpage?",
                    "What are cookies and sessions?",
                ],
                "project": [
                    "Describe a website you've built.",
                    "Walk me through your development process.",
                    "What technologies did you use in your last project?",
                ],
                "scenario": [
                    "How would you make a website responsive?",
                    "What would you do if a feature works locally but not in production?",
                    "How do you debug frontend issues?",
                ],
            },
            "intermediate": {
                "hr": [
                    "Describe a challenging full-stack project you completed.",
                    "How do you balance frontend and backend work?",
                    "Tell me about your experience with agile development.",
                ],
                "technical": [
                    "Explain client-side vs server-side rendering.",
                    "How would you handle authentication in a web app?",
                    "What is CORS and why is it important?",
                    "Describe state management in frontend applications.",
                    "How do you optimize web application performance?",
                ],
                "project": [
                    "Walk me through building a full-stack application.",
                    "How did you handle database design in your project?",
                    "Describe your deployment process.",
                ],
                "scenario": [
                    "The application is slow. How do you identify and fix it?",
                    "How would you implement real-time features?",
                    "A security vulnerability is discovered. What's your response?",
                ],
            },
            "advanced": {
                "hr": [
                    "Describe your experience leading full-stack projects.",
                    "How do you make architectural decisions?",
                    "Tell me about a time you improved system performance significantly.",
                ],
                "technical": [
                    "Design a real-time collaborative editing application.",
                    "How would you scale a full-stack app to millions of users?",
                    "Explain your approach to microservices in full-stack development.",
                    "Describe strategies for implementing effective caching.",
                    "How would you implement a CI/CD pipeline?",
                ],
                "project": [
                    "Describe the most complex full-stack system you've built.",
                    "How did you ensure reliability and uptime?",
                    "Walk me through your monitoring and logging strategy.",
                ],
                "scenario": [
                    "Design a multi-tenant SaaS platform architecture.",
                    "How would you migrate a legacy system to modern stack?",
                    "The system needs to handle 10x traffic tomorrow. What do you do?",
                ],
            },
        },
        "AI Engineer": {
            "beginner": {
                "hr": [
                    "What interests you about AI engineering?",
                    "Describe your background in AI and ML.",
                    "How do you stay current with AI developments?",
                ],
                "technical": [
                    "What is the difference between AI, ML, and Deep Learning?",
                    "Explain what a neural network is.",
                    "What is natural language processing?",
                    "How do you evaluate an AI model?",
                    "What is transfer learning?",
                ],
                "project": [
                    "Describe an AI project you've worked on.",
                    "Walk me through building a simple ML model.",
                    "What AI tools and frameworks have you used?",
                ],
                "scenario": [
                    "How would you approach building a chatbot?",
                    "What would you do if your AI model gives unexpected results?",
                    "How do you choose between different AI approaches?",
                ],
            },
            "intermediate": {
                "hr": [
                    "Describe a time your AI solution solved a real problem.",
                    "How do you explain AI systems to non-technical people?",
                    "Tell me about challenges you've faced in AI projects.",
                ],
                "technical": [
                    "Explain how transformers work in NLP.",
                    "What is retrieval-augmented generation (RAG)?",
                    "How would you implement semantic search?",
                    "Describe your experience with vector databases.",
                    "What is prompt engineering and why is it important?",
                ],
                "project": [
                    "Walk me through building an AI-powered application.",
                    "How did you integrate LLMs into your project?",
                    "Describe your experience with AI model deployment.",
                ],
                "scenario": [
                    "How would you build a document Q&A system?",
                    "The AI model is too slow for production. How do you optimize it?",
                    "How would you handle hallucinations in LLM outputs?",
                ],
            },
            "advanced": {
                "hr": [
                    "Describe your experience leading AI initiatives.",
                    "How do you approach AI ethics and responsible AI?",
                    "Tell me about innovating with cutting-edge AI.",
                ],
                "technical": [
                    "Design an intelligent career coaching platform.",
                    "How would you build a multi-agent AI system?",
                    "Explain your approach to AI model monitoring and governance.",
                    "Describe advanced techniques for improving LLM performance.",
                    "How would you implement AI at enterprise scale?",
                ],
                "project": [
                    "Describe the most complex AI system you've architected.",
                    "How did you ensure AI safety and reliability?",
                    "Walk me through building an AI platform from scratch.",
                ],
                "scenario": [
                    "Design an AI-powered interview simulator with adaptive questioning.",
                    "How would you build a production-ready RAG system?",
                    "The AI system needs to handle multiple languages. How do you approach this?",
                ],
            },
        },
    }
    
    # Get role-specific questions or default to Software Engineer
    role_bank = role_questions.get(target_role, role_questions["Software Engineer"])
    difficulty_bank = role_bank.get(difficulty, role_bank.get("intermediate", {}))
    
    # Build response for requested types
    for t in types:
        questions[t] = difficulty_bank.get(t, [f"Tell me about your experience with {target_role}."])
    
    return questions


def get_mock_interview_question(
    target_role: str,
    difficulty: str,
    conversation: list[dict],
    question_index: int,
) -> str:
    model = _get_model()
    if not model:
        return _get_mock_question_from_bank(target_role, difficulty, question_index)

    history = "\n".join(f"{m['role']}: {m['content']}" for m in conversation[-10:])
    prompt = f"""You are an interviewer for {target_role} ({difficulty} level).
Ask ONE new interview question. Consider conversation history.
If the candidate's last answer was shallow, ask a follow-up instead.
Return ONLY the question text, no JSON.

History:
{history}
"""
    response = model.generate_content(prompt)
    return response.text.strip()


def _get_mock_question_from_bank(target_role: str, difficulty: str, question_index: int) -> str:
    """Get role-specific programming and coding interview questions."""
    questions = {
        "Software Engineer": {
            "beginner": [
                "Tell me about yourself and your background in programming.",
                "What programming languages are you most comfortable with?",
                "Describe a simple coding project you've built.",
                "What does the term 'DRY' (Don't Repeat Yourself) mean to you?",
                "Explain what a function is and why we use them.",
                "What is the difference between a variable and a constant?",
                "How would you debug a program that's not working correctly?",
                "What version control systems have you used? Why are they important?",
                "Describe the difference between compiled and interpreted languages.",
                "What's your approach to writing clean, readable code?",
            ],
            "intermediate": [
                "Walk me through how you would design a system to handle user authentication.",
                "Explain the concept of time complexity and why it matters.",
                "How would you optimize a slow database query?",
                "Describe a microservices architecture and its benefits.",
                "What are RESTful APIs and how do they work?",
                "Explain the difference between SQL and NoSQL databases.",
                "What is a race condition and how would you prevent it?",
                "Describe your experience with automated testing.",
                "How would you approach refactoring legacy code?",
                "Explain the MVC (Model-View-Controller) pattern.",
                "What's your experience with Git workflows and branching strategies?",
                "How do you handle security vulnerabilities in your code?",
            ],
            "advanced": [
                "Design a distributed system that handles millions of users. What challenges would you face?",
                "Explain how you would implement caching strategies for optimal performance.",
                "Describe the trade-offs between consistency, availability, and partition tolerance (CAP theorem).",
                "How would you architect a scalable real-time analytics system?",
                "Explain microservices communication patterns and their trade-offs.",
                "What strategies would you use for zero-downtime deployments?",
                "How do you approach performance profiling and optimization?",
                "Describe your experience with containerization and orchestration (Docker, Kubernetes).",
                "How would you design a system for handling billions of events per second?",
                "Explain the principles of event-driven architecture and when to use it.",
            ],
        },
        "Full Stack Developer": {
            "beginner": [
                "Tell me about your background in web development.",
                "What's the difference between frontend and backend development?",
                "Describe a website you've built and the technologies you used.",
                "What is HTML and what's its role in web development?",
                "Explain what CSS is and how it works with HTML.",
                "What is JavaScript and why is it important for web development?",
                "How do browsers render a webpage?",
                "What's the purpose of a framework like React or Vue?",
                "Describe what a REST API is in simple terms.",
                "What are cookies and sessions, and why do they matter?",
            ],
            "intermediate": [
                "How would you build a responsive web application for multiple devices?",
                "Explain the difference between client-side and server-side rendering.",
                "What's the difference between SQL and NoSQL, and when would you use each?",
                "Describe how you would handle authentication and authorization in a web app.",
                "What are middleware in web frameworks and why are they useful?",
                "Explain the concept of HTTP status codes and give examples.",
                "How would you optimize a slow web application?",
                "Describe your experience with state management in frontend applications.",
                "What is CORS and why is it important?",
                "How do you test your full-stack applications?",
                "Explain the deployment process for a full-stack application.",
                "What are some security best practices for web applications?",
            ],
            "advanced": [
                "Design a real-time collaborative editing application. How would you architect it?",
                "Explain how you would scale a full-stack application to handle millions of users.",
                "Describe strategies for implementing effective caching at multiple layers.",
                "How would you handle data consistency between frontend and backend in real-time?",
                "Explain the principles of headless CMS and when to use them.",
                "How would you implement a CI/CD pipeline for a full-stack application?",
                "Describe your approach to monitoring and logging in production.",
                "How would you architect a system for handling complex business logic?",
                "Explain microservices architecture and how it impacts full-stack development.",
                "How do you approach performance optimization at scale?",
            ],
        },
        "Data Engineer": {
            "beginner": [
                "Tell me about your background in data engineering.",
                "What is ETL and why is it important?",
                "Describe a data pipeline you've built.",
                "What's the difference between a data warehouse and a data lake?",
                "Explain what SQL is and its importance in data engineering.",
                "What is data quality and how do you ensure it?",
                "Describe the basics of distributed computing.",
                "What are the key responsibilities of a data engineer?",
                "Explain what a data schema is and why it matters.",
                "What's the difference between batch and real-time processing?",
            ],
            "intermediate": [
                "How would you design a data pipeline for handling terabytes of data?",
                "Explain the architecture of Apache Spark and when to use it.",
                "Describe your experience with cloud platforms (AWS, GCP, Azure).",
                "How do you optimize SQL queries for performance?",
                "Explain the difference between structured and unstructured data.",
                "What strategies would you use for data partitioning and indexing?",
                "Describe your experience with data orchestration tools like Airflow.",
                "How would you handle data validation and quality checks?",
                "Explain the concept of data lineage and why it's important.",
                "How do you ensure data security and privacy?",
                "Describe your experience with big data technologies (Hadoop, Spark).",
                "How would you handle schema evolution in data pipelines?",
            ],
            "advanced": [
                "Design a real-time data platform handling petabyte-scale datasets.",
                "Explain how you would implement data governance and cataloging.",
                "Describe strategies for optimizing data warehousing performance.",
                "How would you architect a system for streaming data at scale?",
                "Explain the trade-offs between different data storage technologies.",
                "How do you approach data lineage and impact analysis?",
                "Describe your experience with machine learning data pipelines.",
                "How would you implement data quality monitoring and alerting?",
                "Explain the principles of data mesh architecture.",
                "How do you handle disaster recovery and data resilience?",
            ],
        },
    }
    
    # Default to Software Engineer if role not found
    role_questions = questions.get(target_role, questions["Software Engineer"])
    difficulty_level = role_questions.get(difficulty, role_questions.get("intermediate"))
    
    # Cycle through questions
    if question_index >= len(difficulty_level):
        return difficulty_level[-1]
    
    return difficulty_level[question_index]


def evaluate_interview_answer(
    question: str,
    answer: str,
    target_role: str,
    difficulty: str,
) -> dict:
    answer_clean = answer.strip()
    
    # Check if answer is substantive
    is_understandable = _is_answer_substantive(answer_clean, question)
    
    if not is_understandable:
        return {
            "score": None,
            "feedback": "Your answer seems unclear or off-topic. Please provide a more focused and detailed response.",
            "needs_clarification": True,
            "clarification_prompt": f"I didn't quite understand your answer. Could you please elaborate on: {question}",
            "needs_follow_up": False,
            "follow_up": None,
        }
    
    model = _get_model()
    if not model:
        return _mock_evaluate_answer(question, answer_clean, target_role, difficulty)

    prompt = f"""Evaluate this interview answer for {target_role} ({difficulty}).
Return ONLY valid JSON: 
score (0-10 number), 
feedback (2-3 sentences),
strengths (array of 2-3 strings),
areas_to_improve (array of 2-3 strings)

Question: {question}
Answer: {answer}
"""
    response = model.generate_content(prompt)
    return _parse_json_response(response.text)


def _is_answer_substantive(answer: str, question: str) -> bool:
    """Check if answer is meaningful and related to the question."""
    words = answer.split()
    
    # Too short answers (less than 10 words) are likely low quality
    if len(words) < 10:
        return False
    
    # Very generic or one-word answers
    if len(words) < 5 and answer.lower() in ["yes", "no", "maybe", "i don't know", "not sure"]:
        return False
    
    # Check for common non-answers
    non_answers = ["i don't know", "no idea", "not sure", "dunno", "unclear", "whatever", "something like that"]
    if any(phrase in answer.lower() for phrase in non_answers):
        if len(words) < 15:
            return False
    
    return True


def _mock_evaluate_answer(question: str, answer: str, target_role: str, difficulty: str) -> dict:
    """Generate contextual evaluation based on answer quality."""
    score = 6 if len(answer.split()) < 30 else 7 if len(answer.split()) < 50 else 8
    
    return {
        "score": score,
        "feedback": f"Reasonable answer. Consider adding specific examples and measurable outcomes.",
        "strengths": ["Relevant answer", "Shows understanding"],
        "areas_to_improve": ["Add concrete examples", "Quantify results when possible"],
        "needs_follow_up": False,
        "follow_up": None,
    }


def generate_interview_feedback(
    conversation: list[dict],
    target_role: str,
) -> dict:
    model = _get_model()
    if not model:
        return {
            "technical_score": 75.0,
            "communication_score": 80.0,
            "confidence_score": 70.0,
            "overall_rating": 75.0,
            "improvement_suggestions": [
                "Use the STAR method for behavioral questions",
                "Provide more technical depth in answers",
                "Practice concise opening summaries",
            ],
            "detailed_feedback": "Solid performance with room to improve specificity and confidence.",
        }

    history = "\n".join(f"{m['role']}: {m['content']}" for m in conversation)
    prompt = f"""Analyze this mock interview for {target_role}.
Return ONLY valid JSON:
technical_score, communication_score, confidence_score, overall_rating (all 0-100),
improvement_suggestions (array), detailed_feedback (string)

Transcript:
{history[:10000]}
"""
    response = model.generate_content(prompt)
    return _parse_json_response(response.text)


def recommend_projects(target_role: str) -> dict:
    model = _get_model()
    if not model:
        return _mock_projects(target_role)

    prompt = f"""Recommend portfolio projects for {target_role}.
Return ONLY valid JSON with beginner, intermediate, advanced arrays.
Each project: title, description, technologies (array), difficulty, resume_impact (string).
3 projects per level.
"""
    response = model.generate_content(prompt)
    return _parse_json_response(response.text)


def _mock_projects(target_role: str) -> dict:
    """Generate role-specific project recommendations with unique titles and descriptions."""
    
    project_templates = {
        "Software Engineer": {
            "beginner": [
                {"title": "Personal Portfolio Website", "description": "Build a responsive portfolio showcasing your projects with React and Tailwind CSS", "technologies": ["React", "Tailwind CSS", "JavaScript"], "resume_impact": "Demonstrates frontend skills and modern UI development"},
                {"title": "Todo List Application", "description": "Create a full-stack todo app with user authentication and CRUD operations", "technologies": ["Node.js", "Express", "MongoDB"], "resume_impact": "Shows understanding of backend development and databases"},
                {"title": "Weather Dashboard", "description": "Build a weather app integrating external APIs with real-time data", "technologies": ["JavaScript", "REST API", "HTML/CSS"], "resume_impact": "Proves API integration and data handling skills"},
            ],
            "intermediate": [
                {"title": "E-commerce Platform", "description": "Develop a full-featured online store with cart, payments, and admin panel", "technologies": ["React", "Node.js", "PostgreSQL", "Stripe"], "resume_impact": "Demonstrates complex state management and payment integration"},
                {"title": "Real-time Chat Application", "description": "Build a messaging app with WebSocket support and user presence", "technologies": ["Socket.io", "React", "Redis"], "resume_impact": "Shows real-time communication and scalability knowledge"},
                {"title": "Task Management System", "description": "Create a Trello-like board with drag-and-drop and team collaboration", "technologies": ["React", "FastAPI", "PostgreSQL"], "resume_impact": "Highlights advanced UI interactions and team features"},
            ],
            "advanced": [
                {"title": "Microservices Architecture Platform", "description": "Design a distributed system with multiple services, API gateway, and service mesh", "technologies": ["Docker", "Kubernetes", "gRPC", "Redis"], "resume_impact": "Demonstrates enterprise-level architecture skills"},
                {"title": "CI/CD Pipeline Automation", "description": "Build an automated deployment system with testing, monitoring, and rollback", "technologies": ["Jenkins", "Docker", "AWS", "Terraform"], "resume_impact": "Shows DevOps expertise and infrastructure as code"},
                {"title": "Scalable Video Streaming Service", "description": "Create a Netflix-like platform with CDN, adaptive streaming, and recommendations", "technologies": ["Node.js", "AWS S3", "CloudFront", "ML"], "resume_impact": "Proves ability to handle high-scale distributed systems"},
            ],
        },
        "Full Stack Developer": {
            "beginner": [
                {"title": "Blog Platform", "description": "Create a blogging site with markdown support and user comments", "technologies": ["React", "Express", "MongoDB"], "resume_impact": "Shows full-stack development fundamentals"},
                {"title": "Recipe Sharing App", "description": "Build a platform for sharing and discovering recipes with search", "technologies": ["Vue.js", "Node.js", "MySQL"], "resume_impact": "Demonstrates CRUD operations and search functionality"},
                {"title": "Expense Tracker", "description": "Develop a personal finance app with charts and budget tracking", "technologies": ["React", "FastAPI", "SQLite"], "resume_impact": "Highlights data visualization and financial logic"},
            ],
            "intermediate": [
                {"title": "Social Media Dashboard", "description": "Create a multi-platform social media management tool with analytics", "technologies": ["React", "Node.js", "PostgreSQL", "Chart.js"], "resume_impact": "Shows API integration and data analytics skills"},
                {"title": "Job Board Platform", "description": "Build a job posting site with applicant tracking and resume parsing", "technologies": ["Next.js", "Django", "PostgreSQL"], "resume_impact": "Demonstrates complex business logic and file handling"},
                {"title": "Learning Management System", "description": "Develop an online course platform with video streaming and quizzes", "technologies": ["React", "Node.js", "AWS S3", "MongoDB"], "resume_impact": "Highlights multimedia handling and user progress tracking"},
            ],
            "advanced": [
                {"title": "Multi-Tenant SaaS Platform", "description": "Build a subscription-based software with tenant isolation and billing", "technologies": ["React", "Node.js", "PostgreSQL", "Stripe"], "resume_impact": "Proves enterprise SaaS architecture expertise"},
                {"title": "Real-Time Collaboration Tool", "description": "Create a Google Docs-like editor with concurrent editing and conflict resolution", "technologies": ["React", "WebSocket", "CRDT", "Redis"], "resume_impact": "Shows advanced real-time synchronization skills"},
                {"title": "Serverless E-commerce Backend", "description": "Design a scalable commerce API using serverless architecture", "technologies": ["AWS Lambda", "DynamoDB", "API Gateway", "S3"], "resume_impact": "Demonstrates cloud-native and serverless expertise"},
            ],
        },
        "Data Analyst": {
            "beginner": [
                {"title": "Sales Dashboard with Power BI", "description": "Create an interactive dashboard analyzing sales trends and KPIs", "technologies": ["Power BI", "Excel", "SQL"], "resume_impact": "Shows data visualization and business intelligence skills"},
                {"title": "Customer Segmentation Analysis", "description": "Analyze customer data to identify segments using clustering", "technologies": ["Python", "Pandas", "Matplotlib"], "resume_impact": "Demonstrates statistical analysis and segmentation"},
                {"title": "Excel KPI Tracker", "description": "Build an automated Excel dashboard with pivot tables and charts", "technologies": ["Excel", "VBA", "Power Query"], "resume_impact": "Highlights Excel proficiency and automation"},
            ],
            "intermediate": [
                {"title": "Customer Churn Prediction", "description": "Analyze customer behavior to predict and prevent churn", "technologies": ["Python", "SQL", "Tableau", "scikit-learn"], "resume_impact": "Shows predictive analytics and business impact"},
                {"title": "Financial Performance Dashboard", "description": "Create a comprehensive financial reporting system with drill-downs", "technologies": ["SQL", "Power BI", "DAX"], "resume_impact": "Demonstrates financial analysis and advanced BI"},
                {"title": "A/B Testing Analysis Framework", "description": "Build a system to analyze experiment results and statistical significance", "technologies": ["Python", "SQL", "Statistics"], "resume_impact": "Highlights experimental design and hypothesis testing"},
            ],
            "advanced": [
                {"title": "Real-Time Business Intelligence Platform", "description": "Design a streaming analytics system for live business metrics", "technologies": ["Python", "Kafka", "Tableau", "SQL"], "resume_impact": "Proves real-time analytics and big data skills"},
                {"title": "Predictive Revenue Analytics System", "description": "Build ML-powered forecasting for revenue and growth projections", "technologies": ["Python", "Time Series", "Prophet", "SQL"], "resume_impact": "Shows advanced forecasting and ML integration"},
                {"title": "Multi-Source Data Warehouse", "description": "Create an ETL pipeline integrating multiple data sources for analysis", "technologies": ["SQL", "Airflow", "dbt", "Snowflake"], "resume_impact": "Demonstrates data engineering and warehouse design"},
            ],
        },
        "Data Scientist": {
            "beginner": [
                {"title": "House Price Prediction", "description": "Build a regression model to predict housing prices from features", "technologies": ["Python", "scikit-learn", "Pandas"], "resume_impact": "Shows ML fundamentals and regression analysis"},
                {"title": "Sentiment Analysis Tool", "description": "Analyze text sentiment using NLP techniques", "technologies": ["Python", "NLTK", "TextBlob"], "resume_impact": "Demonstrates NLP and text processing skills"},
                {"title": "Iris Flower Classification", "description": "Create a multi-class classifier for the classic Iris dataset", "technologies": ["Python", "scikit-learn", "Matplotlib"], "resume_impact": "Highlights classification and model evaluation"},
            ],
            "intermediate": [
                {"title": "Customer Lifetime Value Predictor", "description": "Build ML models to predict customer value and retention", "technologies": ["Python", "XGBoost", "SQL", "Pandas"], "resume_impact": "Shows business-focused ML and feature engineering"},
                {"title": "Image Classification System", "description": "Develop a CNN-based image classifier with transfer learning", "technologies": ["Python", "TensorFlow", "Keras"], "resume_impact": "Demonstrates deep learning and computer vision"},
                {"title": "Recommendation Engine", "description": "Create a collaborative filtering system for product recommendations", "technologies": ["Python", "Surprise", "Pandas"], "resume_impact": "Highlights recommender systems and personalization"},
            ],
            "advanced": [
                {"title": "End-to-End ML Pipeline", "description": "Design a production ML system with training, serving, and monitoring", "technologies": ["Python", "MLflow", "Docker", "FastAPI"], "resume_impact": "Proves MLOps and production ML expertise"},
                {"title": "NLP Chatbot with RAG", "description": "Build an intelligent chatbot using retrieval-augmented generation", "technologies": ["Python", "LangChain", "Vector DB", "OpenAI"], "resume_impact": "Shows cutting-edge NLP and LLM integration"},
                {"title": "Fraud Detection System", "description": "Create a real-time anomaly detection system for fraud prevention", "technologies": ["Python", "Kafka", "TensorFlow", "Redis"], "resume_impact": "Demonstrates real-time ML and anomaly detection"},
            ],
        },
        "AI Engineer": {
            "beginner": [
                {"title": "Resume Classifier", "description": "Build a model to categorize resumes by job role", "technologies": ["Python", "scikit-learn", "NLP"], "resume_impact": "Shows text classification and ML basics"},
                {"title": "Simple Chatbot", "description": "Create a rule-based chatbot with intent recognition", "technologies": ["Python", "NLTK", "Flask"], "resume_impact": "Demonstrates conversational AI fundamentals"},
                {"title": "Image Caption Generator", "description": "Build a model that generates captions for images", "technologies": ["Python", "TensorFlow", "CNN"], "resume_impact": "Highlights vision-language models"},
            ],
            "intermediate": [
                {"title": "Job Recommendation Engine", "description": "Develop an AI system matching candidates to jobs", "technologies": ["Python", "Transformers", "Vector DB"], "resume_impact": "Shows semantic search and embeddings"},
                {"title": "Document Q&A System", "description": "Create a system that answers questions from documents", "technologies": ["Python", "LangChain", "FAISS"], "resume_impact": "Demonstrates RAG and information retrieval"},
                {"title": "Voice Assistant", "description": "Build a voice-controlled AI assistant with speech recognition", "technologies": ["Python", "Whisper", "TTS", "LLM"], "resume_impact": "Highlights multimodal AI integration"},
            ],
            "advanced": [
                {"title": "AI Career Coach Platform", "description": "Design an intelligent career guidance system with personalization", "technologies": ["Python", "LLM", "Vector DB", "FastAPI"], "resume_impact": "Proves end-to-end AI product development"},
                {"title": "Intelligent Interview Simulator", "description": "Create an AI interviewer with adaptive questioning and feedback", "technologies": ["Python", "GPT-4", "Speech API", "WebSocket"], "resume_impact": "Shows advanced conversational AI and evaluation"},
                {"title": "Multi-Agent AI System", "description": "Build a system with multiple AI agents collaborating on tasks", "technologies": ["Python", "LangGraph", "Redis", "Docker"], "resume_impact": "Demonstrates cutting-edge AI orchestration"},
            ],
        },
    }
    
    # Default to Software Engineer if role not found
    role_projects = project_templates.get(target_role, project_templates["Software Engineer"])
    
    return {
        "beginner": [{"difficulty": "beginner", **p} for p in role_projects["beginner"]],
        "intermediate": [{"difficulty": "intermediate", **p} for p in role_projects["intermediate"]],
        "advanced": [{"difficulty": "advanced", **p} for p in role_projects["advanced"]],
    }


def get_dashboard_recommendations(user_context: dict) -> list[str]:
    model = _get_model()
    if not model:
        return [
            "Upload your latest resume for an ATS score",
            "Complete a mock interview this week",
            "Add 2 missing skills to your learning tracker",
            "Apply to 3 roles matching your target position",
        ]

    prompt = f"""Based on user career data, return ONLY a JSON array of 4 personalized recommendation strings.
Context: {json.dumps(user_context)}
"""
    response = model.generate_content(prompt)
    result = _parse_json_response(response.text)
    return result if isinstance(result, list) else result.get("recommendations", [])
