SENSITIVE_PORTS = {
    21: "FTP ouvert",
    23: "Telnet ouvert",
    3306: "MySQL ouvert",
    3389: "RDP ouvert",
}


def build_alerts(device):
    alerts = []

    if device.get("vendor") == "Inconnu":
        alerts.append(
            {
                "severity": "MEDIUM",
                "message": "Fabricant inconnu",
            }
        )

    if device.get("hostname") == "Inconnu":
        alerts.append(
            {
                "severity": "LOW",
                "message": "Hostname inconnu",
            }
        )

    if device.get("latency") and device["latency"] > 100:
        alerts.append(
            {
                "severity": "LOW",
                "message": "Latence elevee",
            }
        )

    for port in device.get("ports", []):
        if port in SENSITIVE_PORTS:
            alerts.append(
                {
                    "severity": "HIGH",
                    "message": f"Port sensible ouvert : {port} ({SENSITIVE_PORTS[port]})",
                }
            )

    return alerts


def calculate_risk(device):
    risk = 0

    if device.get("status") == "offline":
        risk += 20

    if device.get("vendor") == "Inconnu":
        risk += 15

    if device.get("hostname") == "Inconnu":
        risk += 10

    if device.get("latency") and device["latency"] > 100:
        risk += 10

    for port in device.get("ports", []):
        if port in SENSITIVE_PORTS:
            risk += 30

    return min(risk, 100)


def enrich_device(device):
    enriched = {
        "ip": device.get("ip", "Inconnu"),
        "mac": device.get("mac", "Inconnu"),
        "hostname": device.get("hostname", "Inconnu"),
        "vendor": device.get("vendor", "Inconnu"),
        "status": device.get("status", "offline"),
        "latency": device.get("latency") or 0,
        "ports": device.get("ports", []),
    }

    enriched["risk"] = calculate_risk(enriched)
    enriched["alerts"] = build_alerts(enriched)

    return enriched
