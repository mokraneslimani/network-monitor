const tableBody = document.getElementById("devicesTable");
const connectionDot = document.getElementById("connectionDot");
const connectionText = document.getElementById("connectionText");
const lastUpdate = document.getElementById("lastUpdate");
const totalDevices = document.getElementById("totalDevices");
const onlineDevices = document.getElementById("onlineDevices");
const highRiskDevices = document.getElementById("highRiskDevices");
const totalAlerts = document.getElementById("totalAlerts");
const addedDevices = document.getElementById("addedDevices");
const removedDevices = document.getElementById("removedDevices");
const alertsList = document.getElementById("alertsList");

const chartContext = document.getElementById("latencyChart");

const latencyChart = new Chart(chartContext, {
    type: "bar",
    data: {
        labels: [],
        datasets: [
            {
                label: "Latency (ms)",
                data: [],
                backgroundColor: "rgba(13, 202, 240, 0.65)",
                borderColor: "rgba(13, 202, 240, 1)",
                borderWidth: 1,
                borderRadius: 8,
            },
        ],
    },
    options: {
        responsive: true,
        scales: {
            x: {
                ticks: { color: "#cbd5e1" },
                grid: { color: "rgba(148, 163, 184, 0.15)" },
            },
            y: {
                beginAtZero: true,
                ticks: { color: "#cbd5e1" },
                grid: { color: "rgba(148, 163, 184, 0.15)" },
            },
        },
        plugins: {
            legend: {
                labels: { color: "#e2e8f0" },
            },
        },
    },
});

function statusBadge(status) {
    const className = status === "online" ? "text-bg-success" : "text-bg-danger";
    return `<span class="badge ${className}">${status}</span>`;
}

function riskBadge(risk) {
    if (risk >= 70) {
        return `<span class="badge text-bg-danger">High (${risk})</span>`;
    }

    if (risk >= 35) {
        return `<span class="badge text-bg-warning">Medium (${risk})</span>`;
    }

    return `<span class="badge text-bg-success">Low (${risk})</span>`;
}

function severityBadge(severity) {
    if (severity === "HIGH") {
        return "text-bg-danger";
    }

    if (severity === "MEDIUM") {
        return "text-bg-warning";
    }

    return "text-bg-info";
}

function portsText(ports) {
    if (!ports || ports.length === 0) {
        return `<span class="text-secondary">None</span>`;
    }

    return ports.map((port) => `<span class="port-pill">${port}</span>`).join(" ");
}

function eventItem(device, type) {
    const badgeClass = type === "added" ? "text-bg-success" : "text-bg-secondary";
    const label = type === "added" ? "New" : "Removed";

    return `
        <div class="event-item">
            <div class="d-flex justify-content-between gap-2">
                <strong>${device.ip}</strong>
                <span class="badge ${badgeClass}">${label}</span>
            </div>
            <div class="event-muted">${device.hostname || "Inconnu"} - ${device.vendor || "Inconnu"}</div>
        </div>
    `;
}

function alertItem(alert) {
    return `
        <div class="event-item event-alert">
            <div class="d-flex justify-content-between gap-2">
                <strong>${alert.ip}</strong>
                <span class="badge ${severityBadge(alert.severity)}">${alert.severity}</span>
            </div>
            <div>${alert.message}</div>
            <div class="event-muted">${alert.hostname} - risk ${alert.risk}</div>
        </div>
    `;
}

function updateStats(stats) {
    totalDevices.textContent = stats.total;
    onlineDevices.textContent = stats.online;
    highRiskDevices.textContent = stats.high_risk;
    totalAlerts.textContent = stats.alerts;
}

function updateEvents(data) {
    addedDevices.innerHTML = data.added.length
        ? data.added.map((device) => eventItem(device, "added")).join("")
        : `<div class="event-muted">No new devices</div>`;

    removedDevices.innerHTML = data.removed.length
        ? data.removed.map((device) => eventItem(device, "removed")).join("")
        : `<div class="event-muted">No removed devices</div>`;

    alertsList.innerHTML = data.alerts.length
        ? data.alerts.map((alert) => alertItem(alert)).join("")
        : `<div class="event-muted">No alerts</div>`;
}

function updateTable(devices) {
    tableBody.innerHTML = "";

    devices.forEach((device) => {
        const row = document.createElement("tr");

        if (device.risk >= 70) {
            row.classList.add("alert-row");
        }

        row.innerHTML = `
            <td class="fw-semibold">${device.ip}</td>
            <td>${device.hostname}</td>
            <td>${device.vendor}</td>
            <td>${statusBadge(device.status)}</td>
            <td>${device.latency} ms</td>
            <td>${portsText(device.ports)}</td>
            <td>${riskBadge(device.risk)}</td>
        `;

        tableBody.appendChild(row);
    });
}

function updateChart(devices) {
    latencyChart.data.labels = devices.map((device) => device.hostname || device.ip);
    latencyChart.data.datasets[0].data = devices.map((device) => device.latency);
    latencyChart.update();
}

function updateDashboard(data) {
    updateStats(data.stats);
    updateEvents(data);
    updateTable(data.devices);
    updateChart(data.devices);
    lastUpdate.textContent = `Last update: ${new Date().toLocaleTimeString()}`;
}

function setConnectionStatus(isConnected) {
    connectionDot.className = `connection-dot ${isConnected ? "bg-success" : "bg-danger"}`;
    connectionText.textContent = isConnected ? "Connected" : "Disconnected";
}

function connectWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${protocol}://${window.location.host}/ws`);

    socket.onopen = () => {
        setConnectionStatus(true);
    };

    socket.onmessage = (event) => {
        updateDashboard(JSON.parse(event.data));
    };

    socket.onclose = () => {
        setConnectionStatus(false);
        setTimeout(connectWebSocket, 3000);
    };

    socket.onerror = () => {
        socket.close();
    };
}

connectWebSocket();
