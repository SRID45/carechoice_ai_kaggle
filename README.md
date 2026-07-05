Step 1: Copy the Markdown Content
Click the "Copy" button on the top-right corner of the code block below.

Markdown
# CareChoice AI: Smart Healthcare Plan Agent

## Overview
CareChoice AI is an advanced ReAct-based agent designed to help Californians navigate the complex landscape of Medicaid, Medicare, and commercial health insurance plans. By combining local programmatic rules (the Eligibility Engine) with sophisticated Large Language Model reasoning via Google's Gemini 2.5 Flash API, the system executes real-time evaluation loops to fetch plan data, verify eligibility constraints, and provide highly transparent, personalized health coverage recommendations.

---

## Features
- **Dynamic Eligibility Engine:** Automatically categorizes user data against legal age and income thresholds to route users into Medicare, Medicaid, or Commercial plan streams.
- **Structured JSON ReAct Loop:** Employs Gemini's native `responseSchema` to guarantee strict JSON formatting, preventing text-parsing bugs and ensuring clean data delivery.
- **Explainer Agent Module:** Automatically translates technical insurance jargon (premiums, deductibles, co-pays) into friendly, actionable human summaries.
- **Comprehensive Frontend Dashboard:** A clean HTML5 interface that displays the final highlighted plan selection right alongside an expandable list of all evaluated alternatives.
- **Production-Ready FastAPI Server:** Features modular asynchronous endpoints, explicit route handling, type safety via Pydantic, and absolute path environment loading hooks.

---

## 🔄 CareChoice AI Workflow Diagram

```text
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
   │ Thought: Analyze demographics & filter pathways │
   │ Action: Query Programmatic Engine & Mock DB  │
   │ Observation: Receive filtered safe options  │
   │ Reasoning: Gemini matches custom preferences│
   │ Action: Yield Structured Response Contract  │
   │ Final Answer: Deliver matched dashboard state│
   └───────────────────────────────────────────┘
                 ▼
───────────────────────────────────────────────────────────────
Core Components
[ Eligibility Engine ] Programmatically calculates whether the applicant qualifies for Medicaid (Medi-Cal), Medicare, or private market Commercial plans based on local thresholds.

[ Plan Database & APIs ] Serves a curated collection of local health options containing critical cost matrices (Premiums, Deductibles) and specialty focus points.

[ Gemini Structured Reasoner ] Acts as the logical brain of the ReAct sequence. It consumes the filtered option objects, matches them against health conditions or preferred networks, and emits a structured data contract mapping thoughts and selections directly.

[ Safety & Guardrail Framework ] Implements Gemini's functional responseMimeType: "application/json" boundaries. This eliminates raw markdown string extraction hazards (reasoning.get("text")) and establishes clean application stability.

Output Delivery
When a query evaluates successfully, the runtime updates the UI layout state seamlessly:

Agent Thought Trace: Visualizes the agent's hidden evaluation thought process, building explicit trust about how a specific conclusion was reached.

Top Highlighted Selection: Creates a prominent custom UI card showcasing the perfect plan fit matched with a tailored, text-based breakdown explaining its strategic advantages.

All Eligible Plans Evaluated: Displays a comprehensive list containing every valid plan option discovered within that tier, providing users with absolute comparative oversight.

📁 Repository Structure
Plaintext
carechoice-ai/
├── backend/
│   ├── main.py              # FastAPI app server entrypoint
│   ├── react_agent.py       # ReAct Loop engine & structured Gemini integration
│   ├── eligibility.py       # Rule-based eligibility matrix
│   ├── plans.py             # Curated insurance plan data store
│   └── requirements.txt     # Backend framework dependency manifest
├── frontend/
│   ├── index.html           # Unified web interaction interface template
│   ├── style.css            # Component aesthetics & grid presentation layout
│   └── script.js            # Async AJAX handler & dynamic UI renderer logic
├── .env                     # Secure API credential targets (git-ignored)
└── README.md                # Comprehensive system documentation
🚀 Run Locally
1. Configure the Environment Key
Create a .env file directly inside the root directory of the repository (/carechoice-ai/.env) and declare your Google API credentials securely:

Code snippet
GEMINI_API_KEY=AIzaSyYourActualGeminiAPIKeyHere
2. Install Project Dependencies
Open your terminal inside the backend package folder and install all required frameworks:

Bash
cd backend
pip install -r requirements.txt
3. Initialize the Web Server
Launch the application via the Uvicorn runtime server engine:

Bash
uvicorn main:app --reload
Once initialized, navigate to http://127.0.0.1:8000/ inside your favorite internet browser to explore the running agent interface!


