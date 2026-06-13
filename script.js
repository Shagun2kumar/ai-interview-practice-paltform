let questions = [];
let currentIndex = 0;
let skills = [];
let timeLeft = 60;
let timer;

function openFullScreen() {
    let elem = document.documentElement;

    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) {
        elem.webkitRequestFullscreen();
    }
}
document.addEventListener("fullscreenchange", () => {

    if (!document.fullscreenElement) {

        alert("⚠️ Please stay in full screen mode!");

        openFullScreen();   // 👈 force back to fullscreen
    }
});

// ================= UPLOAD =================
async function upload(){
    let file = document.getElementById("file").files[0];

    if(!file){
        alert("Select resume first");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    let res = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    let data = await res.json();

    skills = data.skills;

    document.getElementById("res").innerText =
        "✅ Resume Uploaded | Skills: " + skills.join(", ");
}

// ================= QUESTIONS =================
async function getQ(){
     openFullScreen();
    let role = document.getElementById("role").value;

    let res = await fetch("/questions", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            role: role,
            skills: skills
        })
    });

    let data = await res.json();

    questions = data.questions;
    currentIndex = 0;

    showQuestion();
}

function showQuestion(){

    if(currentIndex < questions.length){

        document.getElementById("q").innerText =
            "Q" + (currentIndex+1) + ": " + questions[currentIndex];

        startTimer();   // 👈 start timer here

    } else {

        document.getElementById("q").innerText =
            "Interview Completed";

        clearInterval(timer);
    }
}



// ================= NEXT =================
function nextQ(){

    clearInterval(timer);  // stop old timer

    currentIndex++;
    document.getElementById("a").value = "";

    showQuestion();
}



// ================= SUBMIT =================
async function submitAns(){
    let q = questions[currentIndex];
    let a = document.getElementById("a").value;

    if(!a){
        alert("Write answer first");
        return;
    }

    let res = await fetch("/answer", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            q: q,
            a: a,
            username: "user"
        })
    });

    let data = await res.json();

    document.getElementById("result").innerText =
        "Score: " + data.score + " | " + data.fb;
}

// ================= VOICE =================
function voice(){
    if(!('webkitSpeechRecognition' in window)){
        alert("Use Chrome for voice");
        return;
    }

    let rec = new webkitSpeechRecognition();
    rec.start();

    rec.onresult = function(e){
        document.getElementById("a").value =
            e.results[0][0].transcript;
    };
}

// ================= CONFIDENCE =================
async function conf(){

    document.getElementById("result").innerText =
        "Analyzing camera... Look at screen";

    let res = await fetch("/confidence");
    let data = await res.json();

    document.getElementById("result").innerText =
        "Camera Confidence: " + data.confidence + "%\n" +
        data.camera_feedback;
}
function voiceConfidence(){

    if(!('webkitSpeechRecognition' in window)){
        alert("Use Google Chrome for voice feature");
        return;
    }

    let recognition = new webkitSpeechRecognition();

    recognition.lang = "en-US";
    recognition.start();

    document.getElementById("result").innerText =
        "🎤 Listening... Speak your introduction";

    recognition.onresult = function(event){

        let text = event.results[0][0].transcript;

        let words = text.split(" ").length;

        let score = 50;
        let msg = "";

        if(words > 30){
            score = 80;
            msg = " Excellent Fluent and confident speaking";
        }
        else if(words > 15){
            score = 65;
            msg = "Good, but improve fluency";
        }
        else{
            score = 40;
            msg = "Speak more clearly and confidently";
        }

        document.getElementById("result").innerText =
            "Voice Confidence: " + score + "%\n" +
            msg + "\n\nYou said: " + text;
    };

    recognition.onerror = function(){
        alert("Voice recognition error. Allow microphone permission.");
    };
}
async function loadDashboard(){

    let res = await fetch("/dashboard");
    let data = await res.json();

    document.getElementById("avg").innerText =
        data.avg.toFixed(2);

    document.getElementById("latest").innerText =
        data.latest;

    document.getElementById("highest").innerText =
        data.highest;

    document.getElementById("total").innerText =
        data.total;

    document.getElementById("level").innerText =
        data.level;

    document.getElementById("feedback").innerText =
        data.feedback;

    let list = document.getElementById("scores");
    list.innerHTML = "";

    data.scores.forEach((s, i) => {
        let li = document.createElement("li");
        li.innerText = "Attempt " + (i+1) + " : " + s;
        list.appendChild(li);
    });

    // GRAPH (SMALL)
    let ctx = document.getElementById('scoreChart').getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.scores.map((_, i) => "A" + (i+1)),
            datasets: [{
                label: 'Score Trend',
                data: data.scores,
                borderWidth: 2,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

loadDashboard();
function startTimer(){

    clearInterval(timer);  // reset timer

    timeLeft = 60;

    document.getElementById("timer").innerText =
        "Time Left: " + timeLeft + "s";

    timer = setInterval(() => {

        timeLeft--;

        document.getElementById("timer").innerText =
            "Time Left: " + timeLeft + "s";

        if (timeLeft <= 0){

            clearInterval(timer);

            alert("⏱ Time up! Moving to next question.");

            nextQ();   // auto next question
        }

    }, 1000);
}

