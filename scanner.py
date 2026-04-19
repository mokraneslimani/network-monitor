import time
from datetime import datetime

from backend.risk import enrich_device
from backend.scanner import get_all_devices
from backend.storage import compare_devices, load_devices, save_devices


def log(message, level="INFO"):
    print(f"[{level}] {datetime.now()} - {message}")


def main():
    log("Lancement du scan")

    old_devices = load_devices()
    raw_devices = get_all_devices()
    devices = [enrich_device(device) for device in raw_devices]
    added, removed = compare_devices(old_devices, devices)

    print("\n--- NOUVEAUX APPAREILS ---")
    for device in added:
        print("Nouveau :", device)

    print("\n--- APPAREILS DISPARUS ---")
    for device in removed:
        print("Disparu :", device)

    print("\n--- ALERTES ---")
    for device in devices:
        for alert in device["alerts"]:
            print(f"{alert['severity']} - {device['ip']} - {alert['message']}")

    save_devices(devices)

    print("\n--- LISTE ACTUELLE ---")
    for device in devices:
        print(device)

    log("Fin du scan")


def auto_scan():
    while True:
        main()
        time.sleep(60)


if __name__ == "__main__":
    auto_scan()
