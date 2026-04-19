import asyncio
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.risk import enrich_device
from backend.scanner import get_all_devices
from backend.storage import compare_devices, load_devices, save_alerts, save_devices


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="Network Monitoring Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


def build_dashboard_data():
    old_devices = load_devices()
    raw_devices = get_all_devices()
    devices = [enrich_device(device) for device in raw_devices]
    added, removed = compare_devices(old_devices, devices)

    alerts = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for device in devices:
        for alert in device["alerts"]:
            alerts.append(
                {
                    "date": now,
                    "ip": device["ip"],
                    "hostname": device["hostname"],
                    "severity": alert["severity"],
                    "message": alert["message"],
                    "risk": device["risk"],
                }
            )

    for device in added:
        alerts.append(
            {
                "date": now,
                "ip": device["ip"],
                "hostname": device["hostname"],
                "severity": "HIGH",
                "message": "Nouvel appareil detecte",
                "risk": device["risk"],
            }
        )

    stats = {
        "total": len(devices),
        "online": len([device for device in devices if device["status"] == "online"]),
        "offline": len([device for device in devices if device["status"] == "offline"]),
        "high_risk": len([device for device in devices if device["risk"] >= 70]),
        "alerts": len(alerts),
        "added": len(added),
        "removed": len(removed),
    }

    save_devices(devices)
    save_alerts(alerts)

    return {
        "devices": devices,
        "added": added,
        "removed": removed,
        "alerts": alerts,
        "stats": stats,
    }


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/devices")
def devices():
    return build_dashboard_data()


@app.websocket("/ws")
async def websocket_devices(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            await websocket.send_json(build_dashboard_data())
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass
