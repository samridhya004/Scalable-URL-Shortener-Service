async function shortenUrl() {
    const longUrl = document.getElementById("longUrl").value;
    const expiry = document.getElementById("expiry").value;
    const alias = document.getElementById("alias").value;

    if (!longUrl) {
        alert("❌ Please enter a URL");
        return;
    }

    const payload = { long_url: longUrl };
    if (expiry) payload.expiry_minutes = parseInt(expiry);
    if (alias) payload.custom_alias = alias;

    try {
        const response = await fetch("http://127.0.0.1:8000/shorten", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            alert(`❌ ${data.detail}`);
            return;
        }

        const resultCard = document.getElementById("result-card");
        const shortUrlLink = document.getElementById("shortUrlLink");
        const openBtn = document.getElementById("openBtn");

        shortUrlLink.textContent = data.short_url;
        shortUrlLink.href = data.short_url;
        openBtn.href = data.short_url;

        resultCard.classList.remove("hidden");

        window.generatedShortUrl = data.short_url;

        const shortCode = data.short_url.split("/").pop();
        fetchStats(shortCode);

    } catch {
        alert("❌ Failed to connect to backend");
    }
}

function copyToClipboard() {
    if (!window.generatedShortUrl) return;

    navigator.clipboard.writeText(window.generatedShortUrl)
        .then(() => alert("✅ Short URL copied!"))
        .catch(() => alert("❌ Copy failed"));
}

async function fetchStats(shortCode) {
    const analyticsDiv = document.getElementById("analytics-card");
    analyticsDiv.innerHTML = "📊 Loading analytics...";

    try {
        const response = await fetch(`http://127.0.0.1:8000/stats/${shortCode}`);
        const data = await response.json();

        if (!response.ok) {
            analyticsDiv.innerHTML = "❌ Unable to fetch analytics";
            return;
        }

        analyticsDiv.innerHTML = `
            <strong>📊 Analytics</strong>
            <div class="analytics-item">
                <span>👁 Clicks</span>
                <b>${data.clicks}</b>
            </div>
            <div class="analytics-item">
                <span>🕒 Created</span>
                <span>${new Date(data.created_at).toLocaleString()}</span>
            </div>
        `;

        analyticsDiv.classList.remove("hidden");

    } catch {
        analyticsDiv.innerHTML = "❌ Analytics service unavailable";
    }
}
