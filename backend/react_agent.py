from eligibility import check_eligibility
from plans import get_mock_plans
import os
import requests

 # Debugging line to check if the key is loaded correctly

def gemini_reasoning(prompt: str, api_key: str):
    # Recommended model update
    model = "gemini-2.5-flash" 
    # Notice the '?key=' query parameter added to the URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def react_loop(user_input: str, api_key: str):

    eligibility = check_eligibility(user_input)
    thought = f"User age {user_input['age']} → check {eligibility} eligibility"

    plans = get_mock_plans()
    filtered = [p for p in plans if eligibility in p["type"]]

    # Call Gemini for reasoning/explanation
    reasoning = gemini_reasoning(f"Compare plans for {user_input}", api_key=api_key)

    print(f"Gemini reasoning response: {reasoning}")  # Debugging line to check the response from Gemini
    best_plan = sorted(filtered, key=lambda x: x["premium"])[0]
    explanation = reasoning.get("text", f"Recommended {best_plan['provider']} {best_plan['type']} because it balances cost and {best_plan['coverage']}.")
    print(f"Best plan: {best_plan}, Explanation: {explanation}")  # Debugging line to check the best plan and explanation
    return {
        "thought": thought,
        "observation": filtered,
        "best_plan": best_plan,
        "explanation": explanation
    }
