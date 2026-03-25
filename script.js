function analyze() {
    const btn = event.target;

    // 🔥 Add click animation
    btn.classList.add("glow");

    setTimeout(() => {
        btn.classList.remove("glow");
    }, 800);

    const text = document.getElementById("text").value;

    fetch("https://ai-voice-guardian-1.onrender.com/analyze", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: text })
})
.then(res => {
    if (!res.ok) {
        throw new Error("API Error: " + res.status);
    }
    return res.json();
})
.then(data => {

    let keywords = data.keywords || [];  // ✅ FIX CRASH

    let color = "";
    if (data.risk === "HIGH RISK") color = "red";
    else if (data.risk === "MEDIUM RISK") color = "orange";
    else color = "green";

    document.getElementById("result").innerHTML = `
        <div style="color:${color}; font-size:22px;">
            ${data.risk}
        </div>
        <div>${data.message}</div>
        <small>Keywords: ${keywords.join(", ")}</small>
    `;
})
.catch(err => {
    console.error(err);
    document.getElementById("result").innerHTML =
        "❌ Error connecting to backend. Check API.";
});
// 🎤 Voice Input
function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    recognition.lang = "en-US";

    recognition.onresult = function(event) {
        document.getElementById("text").value = event.results[0][0].transcript;
    };

    recognition.start();
}
