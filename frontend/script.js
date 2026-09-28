async function sendCommand(command) {
    const response = await fetch("/api/action", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({command})
    });

    if (!response.ok) {
        console.error("Command failed");
        return;
    }

    const data = await response.json();
    render(data);
}

async function setVolume(value) {
    document.getElementById("volumeValue").textContent = `${value}%`;

    const response = await fetch("/api/volume", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({volume: value})
    });

    if (response.ok) {
        render(await response.json());
    }
}

async function loadState() {
    const response = await fetch("/api/state");
    if (response.ok) {
        render(await response.json());
    }
}

function render(data) {
    document.getElementById("mediaState").textContent =
        data.playing ? "PLAYING" : "STOPPED";

    document.getElementById("track").textContent = data.track;
    document.getElementById("halState").textContent = data.audio_hal;
    document.getElementById("driverState").textContent = data.driver;
    document.getElementById("volumeValue").textContent = `${data.volume}%`;
    document.getElementById("volume").value = data.volume;

    const logs = document.getElementById("logs");
    logs.innerHTML = data.logs.map(log => `
        <div class="log">
            <span class="log-time">${log.time}</span>
            <span class="log-component">${log.component}</span>
            <span>${log.message}</span>
        </div>
    `).join("");

    syncLogHeight();
}

function syncLogHeight() {
    const statusGrid = document.querySelector(".status-grid");
    const volume = document.querySelector(".volume");
    const logs = document.getElementById("logs");
    if (!statusGrid || !volume || !logs) return;

    if (window.innerWidth > 1050) {
        const top = statusGrid.getBoundingClientRect().top;
        const bottom = volume.getBoundingClientRect().bottom;
        const targetHeight = Math.round(bottom - top);
        if (targetHeight > 100) {
            logs.style.height = `${targetHeight}px`;
            logs.style.maxHeight = `${targetHeight}px`;
        }
    } else {
        logs.style.height = "";
        logs.style.maxHeight = "";
    }
}

window.addEventListener("resize", syncLogHeight);
window.addEventListener("DOMContentLoaded", syncLogHeight);

loadState();
