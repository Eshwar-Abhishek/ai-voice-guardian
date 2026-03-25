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
        body: JSON.stringify({ text })
    })
    .then(res => res.json())
    .then(data => {

        let color = "";
        if (data.risk === "HIGH RISK") color = "red";
        else if (data.risk === "MEDIUM RISK") color = "orange";
        else color = "green";

        const resultDiv = document.getElementById("result");

        // ✨ Fade animation
        resultDiv.style.opacity = 0;

        setTimeout(() => {
            resultDiv.innerHTML = `
                <div style="color:${color}; font-size:22px;">
                    ${data.risk}
                </div>
                <div>${data.message}</div>
                <small>Keywords: ${data.keywords.join(", ")}</small>
            `;
            resultDiv.style.opacity = 1;
        }, 200);

        if (data.audio) {
            const audio = document.getElementById("audio");
            audio.src = data.audio;
            audio.play();
        }
    });
}

// 🎤 Voice Input
function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    recognition.lang = "en-US";

    recognition.onresult = function(event) {
        document.getElementById("text").value = event.results[0][0].transcript;
    };

    recognition.start();
}
