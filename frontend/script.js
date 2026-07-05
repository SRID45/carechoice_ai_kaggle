document.getElementById("careForm").addEventListener("submit", async function(e){
  e.preventDefault();
  
  const userInput = {
    age: parseInt(document.getElementById("age").value),
    income: parseInt(document.getElementById("income").value),
    conditions: document.getElementById("conditions").value ? [document.getElementById("conditions").value] : [],
    preferred_provider: document.getElementById("provider").value
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/recommend", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(userInput)
    });
    
    if (!response.ok) throw new Error("Network exception calling agent reasoning route.");
    const data = await response.json();

    // 1. Render the Agent Thought Trace Metadata
    document.getElementById("thoughtText").innerText = data.thought || "Processing profiles criteria context rules...";

    // 2. Render the Top Selection highlighted by Gemini
    const topPlanDiv = document.getElementById("topPlan");
    if (data.best_plan) {
      topPlanDiv.innerHTML = `
        <div class="plan-card" style="border: 2px solid #2bc473; background: #fafdfb; position: relative;">
          <span style="position: absolute; top: 10px; right: 10px; background: #2bc473; color: white; padding: 3px 8px; font-size: 11px; font-weight: bold; border-radius: 4px;">GEMINI SELECTION</span>
          <h3>${data.best_plan.provider} - ${data.best_plan.type}</h3>
          <p><strong>Premium:</strong> $${data.best_plan.premium}/month</p>
          <p><strong>Deductible:</strong> $${data.best_plan.deductible}</p>
          <p><strong>Coverage Scope:</strong> ${data.best_plan.coverage}</p>
          <div style="background: #f4f6f8; padding: 12px; border-left: 3px solid #2bc473; margin-top: 10px; font-size: 14px; line-height: 1.4;">
            <strong>Gemini Reasoning:</strong> ${data.explanation}
          </div>
        </div>
      `;
    } else {
      topPlanDiv.innerHTML = "<p>No matching criteria plans discovered.</p>";
    }

    // 3. Render All Evaluated Alternatives Loop List
    const allPlansDiv = document.getElementById("allPlansList");
    if (data.all_filtered_plans && data.all_filtered_plans.length > 0) {
      allPlansDiv.innerHTML = data.all_filtered_plans.map(plan => `
        <div class="plan-card" style="background: #fcfcfc; border: 1px solid #e2e8f0; padding: 12px; margin-bottom: 10px;">
          <h4 style="margin: 0 0 5px 0; color: #334155;">${plan.provider} (${plan.type})</h4>
          <p style="margin: 3px 0; font-size: 13px; color: #64748b;">Premium: $${plan.premium} | Deductible: $${plan.deductible}</p>
          <small style="color: #94a3b8;">Coverage Focus: ${plan.coverage}</small>
        </div>
      `).join("");
    } else {
      allPlansDiv.innerHTML = "<p>No alternative plans passed category validation.</p>";
    }

    // Show the results panel container blocks
    document.getElementById("result").style.display = "block";

  } catch (error) {
    console.error(error);
    alert("Error fetching recommendation: " + error.message);
  }
});

// Clear button handler function
document.getElementById("clearBtn").addEventListener("click", function() {
  document.getElementById("careForm").reset();
  document.getElementById("result").style.display = "none";
  document.getElementById("thoughtText").innerText = "";
  document.getElementById("topPlan").innerHTML = "";
  document.getElementById("allPlansList").innerHTML = "";
});