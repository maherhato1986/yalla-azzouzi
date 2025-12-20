const API_KEY = "71a7d17fa5addaa485d7d720bdae8f5f";
const API_URL = "https://v3.football.api-sports.io";

async function fetchMatches(endpoint) {
  const res = await fetch(`${API_URL}${endpoint}`, {
    headers: {
      "x-apisports-key": API_KEY
    }
  });
  const data = await res.json();
  return data.response || [];
}

function createMatchHTML(match) {
  const home = match.teams.home;
  const away = match.teams.away;
  const goalsHome = match.goals.home ?? "-";
  const goalsAway = match.goals.away ?? "-";

  let status = "لم تبدأ";
  if (match.fixture.status.short === "LIVE") status = "🔴 جارية الآن";
  if (match.fixture.status.short === "FT") status = "✅ انتهت";

  return `
    <div class="match-card">
      <div class="teams">
        <div>${home.name}</div>
        <strong>${goalsHome} - ${goalsAway}</strong>
        <div>${away.name}</div>
      </div>
      <div class="status">${status}</div>
    </div>
  `;
}

async function loadTodayMatches() {
  const today = new Date().toISOString().split("T")[0];
  const matches = await fetchMatches(`/fixtures?date=${today}`);

  let html = "";
  matches.forEach(m => {
    html += createMatchHTML(m);
  });

  // 🔴 نضيف بدون حذف أي شيء
  const container = document.createElement("div");
  container.innerHTML = `
    <h3 style="margin:15px 0">⚽ مباريات اليوم (تحديث تلقائي)</h3>
    ${html}
  `;

  document.body.prepend(container);
}

// تحديث تلقائي كل دقيقة
loadTodayMatches();
setInterval(loadTodayMatches, 60000);
