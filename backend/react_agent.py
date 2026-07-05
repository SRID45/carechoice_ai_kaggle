from eligibility import check_eligibility
from plans import get_mock_plans
import os
import requests
import json

def gemini_reasoning(prompt: str, filtered_plans: list, api_key: str):
    model = "gemini-2.5-flash" 
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Instruct the agent on its role and rules
    system_instruction = (
        "You are an expert health insurance advisor agent. Analyze the user profiles "
        "and compare the filtered available plans. Pick the absolute best plan based on the user's needs, "
        "and generate a patient-friendly explanation detailing the exact trade-offs."
    )
    
    # Enforce structured JSON output from Gemini
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "thought_trace": {"type": "STRING", "description": "Internal reasoning step evaluating options and priorities."},
            "selected_provider_name": {"type": "STRING", "description": "The exact 'provider' name string of the chosen plan."},
            "user_explanation": {"type": "STRING", "description": "A clear, detailed explanation written directly to the user detailing why this plan was chosen over alternatives."}
        },
        "required": ["thought_trace", "selected_provider_name", "user_explanation"]
    }
    
    data = {
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"parts": [{"text": f"User Prompt:\n{prompt}\n\nAvailable Filtered Options:\n{json.dumps(filtered_plans)}"}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    # Parse Gemini's response safely
    res_json = response.json()
    raw_text = res_json['candidates'][0]['content']['parts'][0]['text']
    return json.loads(raw_text)

def react_loop(user_input: dict, api_key: str):
    # Step 1: Act - Determine Eligibility
    eligibility = check_eligibility(user_input)
    thought = f"User age {user_input['age']} & income {user_input['income']} → check {eligibility} eligibility"

    # Step 2: Act - Fetch and filter plans based on calculated category
    plans = get_mock_plans()
    filtered = [p for p in plans if eligibility.lower() in p["type"].lower()]

    if not filtered:
        return {
            "thought": thought,
            "all_filtered_plans": [],
            "best_plan": None,
            "explanation": "No available plans found matching eligibility path requirements."
        }

    # Step 3: Call Gemini to perform Agentic evaluation
    prompt = (
        f"Find the best fit plan for a user who is {user_input['age']} years old, "
        f"has an income of ${user_input['income']}, health conditions: {user_input.get('conditions', [])}, "
        f"and preferred provider: '{user_input.get('preferred_provider', 'None')}'."
    )

    try:
        agent_verdict = gemini_reasoning(prompt, filtered, api_key)
        
        # Cross-reference Gemini's chosen name with database objects
        chosen_provider = agent_verdict.get("selected_provider_name", "").lower()
        best_plan = next((p for p in filtered if p["provider"].lower() == chosen_provider), filtered[0])
        explanation = agent_verdict.get("user_explanation")
        thought = agent_verdict.get("thought_trace", thought)

    except Exception as e:
        # Secure fallback parsing mechanics in case of unexpected network hitches
        best_plan = sorted(filtered, key=lambda x: x["premium"])[0]
        explanation = f"Recommended {best_plan['provider']} because it offers the lowest baseline premium. (Agent processing fallback triggered: {str(e)})"

    return {
        "thought": thought,
        "all_filtered_plans": filtered,
        "best_plan": best_plan,
        "explanation": explanation
    }