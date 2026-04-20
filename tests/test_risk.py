from backend.risk import calculate_risk, build_alerts, enrich_device


def test_calculate_risk_for_unknown_device():
    device = {
        "status": "online",
        "vendor": "Inconnu",
        "hostname": "Inconnu",
        "latency": 10,
        "ports": [],
    }

    risk = calculate_risk(device)

    assert risk == 25


def test_calculate_risk_for_sensitive_port():
    device = {
        "status": "online",
        "vendor": "Cisco",
        "hostname": "router",
        "latency": 10,
        "ports": [3306],
    }

    risk = calculate_risk(device)

    assert risk == 30


def test_build_alerts_for_unknown_vendor_and_hostname():
    device = {
        "vendor": "Inconnu",
        "hostname": "Inconnu",
        "latency": 10,
        "ports": [],
    }

    alerts = build_alerts(device)

    assert {"severity": "MEDIUM", "message": "Fabricant inconnu"} in alerts
    assert {"severity": "LOW", "message": "Hostname inconnu"} in alerts


def test_enrich_device_adds_risk_and_alerts():
    device = {
        "ip": "192.168.1.10",
        "mac": "AA:BB:CC:DD:EE:FF",
        "hostname": "Inconnu",
        "vendor": "Inconnu",
        "status": "online",
        "latency": 10,
        "ports": [],
    }

    enriched = enrich_device(device)

    assert enriched["ip"] == "192.168.1.10"
    assert enriched["risk"] == 25
    assert len(enriched["alerts"]) == 2
