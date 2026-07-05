# CareChoice AI: Smart Healthcare Plan Agent

## Overview
CareChoice AI is a ReAct-based agent that helps Californians compare Medicaid, Medicare, and commercial health insurance plans. It uses reasoning + acting loops to fetch plan data, check eligibility, and deliver personalized recommendations.

## Features
- Eligibility engine (Medicare, Medicaid, Commercial)
- Plan comparison module
- Explainer agent for plain-language outputs
- Simple HTML frontend
- FastAPI backend
- Colab notebook demo

## 🔄 CareChoice AI Workflow Diagram

User Input
──────────
[ Demographics ] ──► [ Preferences ] ──► [ Constraints ]
   (Age, Income,       (Provider,        (Eligibility rules:
    Health needs)       Priorities)       Medicaid, Medicare, Commercial)

───────────────────────────────────────────────────────────────
                 ▼
        ┌───────────────────────┐
        │   ReAct Agent Loop    │
        └───────────────────────┘
                 │
   ┌─────────────┼─────────────────────────────┐
   │ Thought: Analyze input, decide next step  │
   │ Action: Call APIs / fetch plan data       │
   │ Observation: Receive structured results   │
   │ Reasoning: Compare, filter, rank plans    │
   │ Action: Summarize & explain trade-offs    │
   │ Final Answer: Deliver recommendation      │
   └───────────────────────────────────────────┘
                 ▼
───────────────────────────────────────────────────────────────

Core Components
───────────────
[ Eligibility Engine ] ──► Determines Medicaid / Medicare / Commercial path
[ Plan Database & APIs ] ──► Pulls CMS.gov, Covered CA, Provider data
[ Comparison Module ] ──► Scores & ranks plans by cost, coverage, network
[ Preference Layer ] ──► Injects user priorities into ranking logic
[ Explainer Agent ] ──► Converts jargon into plain language
[ Security & Guardrails ] ──► Structured JSON, safe API handling

───────────────────────────────────────────────────────────────
                 ▼
Output Delivery
───────────────
[ Ranked Plan List ] ──► Top 3–5 options with scores
[ Explanation Layer ] ──► Trade-offs explained clearly
[ Final Recommendation ] ──► Best-fit plan highlighted with reasoning trace

## Run Locally
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
