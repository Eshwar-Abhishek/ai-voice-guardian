// 🎤 Mic Input
function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";

    recognition.onresult = function (event) {
        const text = event.results[0][0].transcript;
        document.getElementById("userInput").value = text;
        sendText();
    };

    recognition.start();
}


// 🚀 Send text to backend
async function sendText() {
    const input = document.getElementById("userInput").value;

    if (!input) return;

    try {
        const response = await fetch("http://127.0.0.1:8000/process", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: input })
        });

        const data = await response.json();

        console.log(data);

        // ✅ Show response
        document.getElementById("result").innerText = data.response;

        // ✅ Risk bar (REAL VALUE)
        updateRiskBar(data.risk);

        // ✅ Alert
        showAlert(data.risk);

        // ✅ Play audio
        playAudio(data.audio);

    } catch (error) {
        console.error(error);
        document.getElementById("result").innerText = "❌ Backend not running!";
    }
}


// 📊 Risk Bar
function updateRiskBar(risk) {
    const bar = document.getElementById("riskBar");

    bar.style.width = risk + "%";

    if (risk > 70) bar.style.background = "red";
    else if (risk > 40) bar.style.background = "orange";
    else bar.style.background = "green";
}


// 🚨 Alert system
function showAlert(risk) {
    if (risk > 75) {
        alert("🚨 HIGH RISK DETECTED!");

        let sound = new Audio("https://www.soundjay.com/button/beep-07.wav");
        sound.play();
    }
}


// 🔊 Play audio
function playAudio(audioData) {
    if (!audioData) return;

    if (audioData.audio_url) {
        const audio = new Audio(audioData.audio_url);
        audio.play();
    }
}