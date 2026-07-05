document.getElementById("careForm").addEventListener("submit", async function(e){
  e.preventDefault();
  const userInput = {
    age: parseInt(document.getElementById("age").value),
    income: parseInt(document.getElementById("income").value),
    conditions: [document.getElementById("conditions").value],
    preferred_provider: document.getElementById("provider").value
  };

  const response = await fetch("http://127.0.0.1:8000/recommend", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(userInput)
  });
  const data = await response.json();

  const plansDiv = document.getElementById("plans");
  plansDiv.innerHTML = `
    <div class="plan-card">
      <h3>${data.best_plan.provider} - ${data.best_plan.type}</h3>
      <p><strong>Premium:</strong> $${data.best_plan.premium}</p>
      <p><strong>Deductible:</strong> $${data.best_plan.deductible}</p>
      <p><strong>Coverage:</strong> ${data.best_plan.coverage}</p>
      <p><strong>Explanation:</strong> ${data.explanation}</p>
    </div>
  `;
  document.getElementById("result").style.display = "block";

  // Clear button handler
  document.getElementById("clearBtn").addEventListener("click", function() {
  // Reset form fields
  document.getElementById("careForm").reset();

  // Hide results section
  document.getElementById("result").style.display = "none";

  // Clear any plan cards
  document.getElementById("plans").innerHTML = "";
  })
});
