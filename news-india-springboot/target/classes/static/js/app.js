const grid = document.getElementById("newsGrid");
const statusEl = document.getElementById("status");
const lastUpdatedEl = document.getElementById("lastUpdated");
const refreshBtn = document.getElementById("refreshBtn");

let currentAbort = null;
const REFRESH_MS = 60_000;
const REQUEST_LIMIT = 18;

function escapeHtml(text) {
  if (text === null || text === undefined) return "";
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatDate(pubDate) {
  if (!pubDate) return "";
  const d = new Date(pubDate);
  if (Number.isNaN(d.getTime())) return pubDate;
  return d.toLocaleString(undefined, { year: "numeric", month: "short", day: "2-digit" });
}

function renderSkeleton(count) {
  grid.innerHTML = "";
  for (let i = 0; i < count; i++) {
    const sk = document.createElement("div");
    sk.className = "skeleton";
    grid.appendChild(sk);
  }
}

function renderItems(items) {
  grid.innerHTML = "";

  if (!items || items.length === 0) {
    statusEl.textContent = "No headlines available right now.";
    return;
  }

  for (const item of items) {
    const a = document.createElement("a");
    a.className = "card";
    a.target = "_blank";
    a.rel = "noopener";
    a.href = item.link || "#";

    const title = escapeHtml(item.title || "");
    const date = escapeHtml(formatDate(item.publishedAt || ""));

    a.innerHTML = `
      <div class="card-inner">
        <h3 class="card-title">${title}</h3>
        <div class="card-date">
          <span class="pill"><span class="dot"></span>${date || "Latest"}</span>
        </div>
      </div>
    `;

    grid.appendChild(a);
  }
}

async function loadNews() {
  if (currentAbort) currentAbort.abort();
  currentAbort = new AbortController();

  statusEl.textContent = "Loading latest headlines...";
  renderSkeleton(REQUEST_LIMIT);

  try {
    const res = await fetch(`/api/news?limit=${REQUEST_LIMIT}`, {
      method: "GET",
      signal: currentAbort.signal,
      cache: "no-store",
    });

    const data = await res.json().catch(() => null);

    if (!res.ok) {
      const msg = data && data.message ? data.message : `Request failed (${res.status}).`;
      throw new Error(msg);
    }

    renderItems(data && data.items ? data.items : []);
    statusEl.textContent = "Showing current headlines in India.";
    lastUpdatedEl.textContent = new Date().toLocaleString();
  } catch (err) {
    if (err && err.name === "AbortError") return;
    statusEl.textContent = "Could not refresh news right now. Please try again shortly.";
  }
}

refreshBtn.addEventListener("click", loadNews);

loadNews();
setInterval(loadNews, REFRESH_MS);

