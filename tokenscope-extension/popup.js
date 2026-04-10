document.addEventListener("DOMContentLoaded", () => {

  const btn = document.getElementById("analyzeBtn");

  btn.addEventListener("click", async () => {

    const text = document.getElementById("prompt").value;

    if (!text) {
      alert("Enter prompt first");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          prompt: text,
          model: "gpt-4o-mini"
        })
      });

      const data = await res.json();

      let html = "";

      // Tokens + Cost
      html += `<div class="card">
        <b>Tokens:</b> ${data.tokens} <br/>
        <b>Cost:</b> $${data.cost}
      </div>`;

      // Heatmap
      html += `<div class="card"><b>Heatmap:</b><br/>`;

      const words = text.match(/\b\w+\b/g) || [];

      words.forEach(word => {
        if (data.token_importance[word]) {

          let level = data.token_importance[word].level;
          let cls = "highlight-low";

          if (level === "HIGH") cls = "highlight-high";
          else if (level === "MEDIUM") cls = "highlight-medium";

          html += `<span class="${cls}">${word} </span>`;
        } else {
          html += word + " ";
        }
      });

      html += `</div>`;

      // Optimization
      if (data.optimization) {
        html += `<div class="card">
          <b>✨ Optimized Prompt</b><br/>
          <div id="optimizedText">${data.optimization.best_prompt}</div>

          <button id="copyBtn" class="copy-btn">📋 Copy</button>

          <div style="margin-top:5px; color:#10b981;">
            Saved: ${data.optimization.tokens_saved} tokens
          </div>
        </div>`;
      }

      document.getElementById("result").innerHTML = html;

      // Copy button logic
      const copyBtn = document.getElementById("copyBtn");
      if (copyBtn) {
        copyBtn.onclick = () => {
          const text = document.getElementById("optimizedText").innerText;
          navigator.clipboard.writeText(text);
          alert("Copied 🚀");
        };
      }

    } catch (err) {
      console.error(err);
      alert("Backend not running");
    }

  });

});