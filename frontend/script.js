const behaviorData = {
  keyIntervals: [],
  mouseEvents: 0,
  clicks: 0,
  scrolls: 0,
  tabSwitches: 0,
  answerChanges: 0,
  startTime: performance.now()
};

let lastKeyTime = null;
let lastMouseSample = 0;

const answerBox = document.getElementById("answer");

answerBox.addEventListener("keydown", () => {
  const now = performance.now();
  if (lastKeyTime !== null) {
    behaviorData.keyIntervals.push(now - lastKeyTime);
  }
  lastKeyTime = now;
});

answerBox.addEventListener("input", () => {
  behaviorData.answerChanges++;
});

document.addEventListener("mousemove", () => {
  const now = performance.now();
  if (now - lastMouseSample > 100) {
    behaviorData.mouseEvents++;
    lastMouseSample = now;
  }
});

document.addEventListener("click", () => behaviorData.clicks++);
document.addEventListener("scroll", () => behaviorData.scrolls++);

document.addEventListener("visibilitychange", () => {
  if (document.hidden) behaviorData.tabSwitches++;
});

document.getElementById("submitBtn").addEventListener("click", () => {
  const totalTime = (performance.now() - behaviorData.startTime) / 1000;

  const payload = {
    keyIntervalMean: mean(behaviorData.keyIntervals),
    keyIntervalStd: std(behaviorData.keyIntervals),
    mouseRate: behaviorData.mouseEvents / totalTime,
    clickRate: behaviorData.clicks / totalTime,
    scrollRate: behaviorData.scrolls / totalTime,
    tabSwitches: behaviorData.tabSwitches,
    answerChanges: behaviorData.answerChanges,
    timeSpent: totalTime
  };

  fetch("http://127.0.0.1:5000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
  .then(res => res.json())
  .then(data => {
    alert(`Risk Score: ${data.risk_score} (${data.status})`);
  });
});

function mean(arr) {
  if (!arr.length) return 0;
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function std(arr) {
  if (!arr.length) return 0;
  const m = mean(arr);
  return Math.sqrt(arr.reduce((s, x) => s + (x - m) ** 2, 0) / arr.length);
}
