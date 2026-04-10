console.log("🔥 TokenScope content script loaded.");

function getPromptBox() {
  return document.querySelector('[contenteditable="true"]');
}

// 🔥 Create floating popup
function createPopup(text, saved) {
  let existing = document.getElementById("tokenscope-popup");
  if (existing) existing.remove();

  let div = document.createElement("div");
  div.id = "tokenscope-popup";

  div.style.position = "fixed";
  div.style.bottom = "20px";
  div.style.right = "20px";
  div.style.background = "#111";
  div.style.color = "#fff";
  div.style.padding = "12px";
  div.style.borderRadius = "10px";
  div.style.zIndex = 9999;
  div.style.width = "300px";
  div.style.boxShadow = "0 0 10px rgba(0,0,0,0.5)";

  div.innerHTML = `
    <div style="font-weight:bold;">⚡ Optimized Prompt</div>
    <div style="margin-top:6px; font-size:13px;">${text}</div>
    <div style="margin-top:6px; font-size:12px; color:#aaa;">
      Saved: ${saved} tokens
    </div>
    <button id="applyBtn" style="margin-top:10px; padding:5px 10px; cursor:pointer;">
      Apply
    </button>
  `;

  document.body.appendChild(div);

  document.getElementById("applyBtn").onclick = () => {
    let input = getPromptBox();
    if (input) {
      input.textContent = text;
    }
  };
}

// 🔥 MAIN LOOP (important fix)
setInterval(() => {
  const input = getPromptBox();

  if (!input) {
    console.log("❌ Input not found yet...");
    return;
  }

  const text = input.innerText;

  if (!text || text.length < 10) return;

  console.log("📩 Detected input:", text);

  fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      prompt: text,
      model: "gpt-4o-mini"
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.optimization) {
      createPopup(
        data.optimization.best_prompt,
        data.optimization.tokens_saved
      );
    }
  })
  .catch(err => console.error(err));

}, 3000); // every 3 sec