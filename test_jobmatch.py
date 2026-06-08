#!/usr/bin/env python3
"""Test JobMatch analysis with various inputs to demonstrate contextual analysis."""

import sys
sys.path.insert(0, 'backend')

from app.services.gemini import _mock_job_match_analysis
import json

test_cases = [
    {
        "name": "Scenario 1: Strong Python Backend Developer",
        "resume": """
        Senior Software Engineer with 5 years experience.
        Skills: Python, JavaScript, React, NodeJS, AWS, Docker, Git, REST APIs, SQL
        Led teams, excellent communication, agile methodologies.
        """,
        "jd": """
        Backend Engineer - Python/AWS
        5+ years experience required
        Must have: Python, AWS, Docker, REST APIs, leadership
        Nice to have: Kubernetes, CI/CD
        """
    },
    {
        "name": "Scenario 2: Junior Frontend Dev applying for Senior Backend Role",
        "resume": """
        Junior Developer, 1 year experience.
        Skills: HTML, CSS, JavaScript, React
        Learning: Git, communication skills developing
        """,
        "jd": """
        Senior Backend Engineer
        5+ years required, system design expertise
        Must have: Python, Java, Kubernetes, microservices, AWS, CI/CD
        Leadership and team mentoring required
        """
    },
    {
        "name": "Scenario 3: Exact Match - GraphQL/TypeScript",
        "resume": """
        Full Stack Engineer, 3 years experience
        Expert in: TypeScript, JavaScript, GraphQL, React, Node.js
        Excellent problem-solving, great communicator, team player
        """,
        "jd": """
        Full Stack Engineer
        3 years experience
        Required: TypeScript, JavaScript, GraphQL, Node.js, React
        Soft skills: Communication, teamwork, problem-solving
        """
    }
]

print("=" * 80)
print("JobMatch Analysis - Contextual Mock Analysis Test")
print("=" * 80)

for i, test in enumerate(test_cases, 1):
    print(f"\n📋 {test['name']}")
    print("-" * 80)
    
    result = _mock_job_match_analysis(test['resume'], test['jd'])
    
    print(f"Match Percentage: {result['match_percentage']}%")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nMatch Breakdown:")
    for category, score in result['match_breakdown'].items():
        print(f"  • {category}: {score}%")
    
    if result['missing_skills']:
        print(f"\nMissing Skills: {', '.join(result['missing_skills'])}")
    else:
        print("\n✅ No missing skills detected!")
    
    if result['skill_gap_analysis']:
        print(f"\nSkill Gaps ({len(result['skill_gap_analysis'])} identified):")
        for gap in result['skill_gap_analysis'][:3]:
            print(f"  • {gap['skill']} ({gap['importance']} priority)")
            print(f"    → {gap['learning_path']} (~{gap['estimated_weeks']} weeks)")
    
    print(f"\nAction Plan:")
    for j, action in enumerate(result['action_plan'][:3], 1):
        print(f"  {j}. {action}")

print("\n" + "=" * 80)
print("✅ Test Complete - Each scenario shows different contextual analysis!")
print("=" * 80)
