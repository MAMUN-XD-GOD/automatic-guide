// ----------------------
// DOM Elements
// ----------------------
const chartUpload = document.getElementById("chartUpload");
const analyzeBtn = document.getElementById("analyzeBtn");

const directionEl = document.getElementById("direction");
const entryEl = document.getElementById("entry");
const tpEl = document.getElementById("tp");
const slEl = document.getElementById("sl");
const probabilityEl = document.getElementById("probability");
const trendEl = document.getElementById("trend");

const winBtn = document.getElementById("winBtn");
const lossBtn = document.getElementById("lossBtn");

const newsList = document.getElementById("newsList");
const overallAccEl = document.getElementById("overallAcc");
const marketStatsEl = document.getElementById("marketStats");

// ----------------------
// Dummy Fetch Functions (Connect to backend)
// ----------------------
async function analyzeChart(file) {
    // Simulate backend POST /analysis
    let formData = new FormData();
    formData.append("chart", file);

    // Dummy fetch for testing
    const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    return data;
}

async function fetchNews() {
    const response = await fetch("/api/news");
    const data = await response.json();
    return data;
}

async function fetchAccuracy() {
    const response = await fetch("/api/accuracy");
    const data = await response.json();
    return data;
}

async function sendFeedback(signal_id, result) {
    await fetch("/api/feedback", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({signal_id, result})
    });
}

// ----------------------
// Update UI
// ----------------------
function updateSignalUI(signal) {
    directionEl.innerText = signal.direction;
    entryEl.innerText = signal.entry;
    tpEl.innerText = signal.TP;
    slEl.innerText = signal.SL;
    probabilityEl.innerText = signal.probability;
    trendEl.innerText = signal.trend;
}

function updateNewsUI(newsData) {
    newsList.innerHTML = "";
    newsData.forEach(item=>{
        const li = document.createElement("li");
        li.textContent = `[${item.source}] ${item.headline} (Impact: ${item.impact_score})`;
        newsList.appendChild(li);
    });
}

function updateAccuracyUI(accData) {
    overallAccEl.innerText = accData.overall;
    marketStatsEl.innerText = JSON.stringify(accData.stats, null, 2);
}

// ----------------------
// Event Listeners
// ----------------------
analyzeBtn.addEventListener("click", async ()=>{
    if(chartUpload.files.length===0) return alert("Please upload chart image!");
    const file = chartUpload.files[0];
    const result = await analyzeChart(file);

    updateSignalUI({
        direction: result.context.signal.direction,
        entry: result.context.signal.entry,
        TP: result.context.signal.TP,
        SL: result.context.signal.SL,
        probability: result.probability,
        trend: result.context.vision.trend_bias
    });

    // Update News & Accuracy
    const news = await fetchNews();
    updateNewsUI(news);

    const acc = await fetchAccuracy();
    updateAccuracyUI(acc);

    // Store current signal_id for feedback
    window.currentSignalId = result.signal_id;
});

winBtn.addEventListener("click", async ()=>{
    if(!window.currentSignalId) return;
    await sendFeedback(window.currentSignalId, "win");
    alert("Feedback Recorded ✅");
});

lossBtn.addEventListener("click", async ()=>{
    if(!window.currentSignalId) return;
    await sendFeedback(window.currentSignalId, "loss");
    alert("Feedback Recorded ❌");
});

// ----------------------
// Auto News Refresh Every 60s
// ----------------------
setInterval(async ()=>{
    const news = await fetchNews();
    updateNewsUI(news);
}, 60000);
