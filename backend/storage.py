import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEVICES_FILE = DATA_DIR / "devices.json"
ALERTS_FILE = DATA_DIR / "alerts.json"


def ensure_data_dir():
    DATA_DIR.mkdir(exist_ok=True)


def load_json(path, default):
    ensure_data_dir()

    if not path.exists():
        return default

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    ensure_data_dir()

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_devices():
    return load_json(DEVICES_FILE, [])


def save_devices(devices):
    save_json(DEVICES_FILE, devices)


def load_alerts():
    return load_json(ALERTS_FILE, [])


def save_alerts(alerts):
    save_json(ALERTS_FILE, alerts)


def compare_devices(old_devices, new_devices):
    old_ips = {device["ip"] for device in old_devices}
    new_ips = {device["ip"] for device in new_devices}

    added = [device for device in new_devices if device["ip"] not in old_ips]
    removed = [device for device in old_devices if device["ip"] not in new_ips]

    return added, removed
