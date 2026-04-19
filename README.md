# Network Monitoring Project

Projet de supervision reseau et de detection simple d'anomalies de securite.

Le projet scanne le reseau local, detecte les appareils connectes, recupere les informations principales, analyse les ports ouverts, calcule un score de risque et affiche les resultats dans un dashboard temps reel.

## Arborescence

```text
network_monitoring_project/
  backend/
    __init__.py
    main.py
    scanner.py
    risk.py
    storage.py
  frontend/
    index.html
    app.js
    style.css
  data/
    devices.json
    alerts.json
  scanner.py
  requirements.txt
  README.md
```

## Role des fichiers

- `backend/scanner.py` : scan reseau, ping et scan de ports.
- `backend/risk.py` : calcul du risque et generation des alertes.
- `backend/storage.py` : lecture et sauvegarde JSON.
- `backend/main.py` : API FastAPI, WebSocket et serveur du frontend.
- `frontend/` : interface web du dashboard.
- `scanner.py` : version console du scanner.
- `data/` : donnees sauvegardees.

## Installation

```powershell
cd "C:\Users\mokra\Downloads\network_monitoring_project"
python -m pip install -r requirements.txt
```

## Lancer le dashboard

```powershell
cd "C:\Users\mokra\Downloads\network_monitoring_project"
python -m uvicorn backend.main:app --reload
```

Puis ouvrir :

```text
http://localhost:8000
```

## Lancer le scanner console

```powershell
cd "C:\Users\mokra\Downloads\network_monitoring_project"
python .\scanner.py
```

## Fonctionnalites

- Detection des appareils du reseau local.
- Recuperation IP, MAC, hostname, vendor, statut, latence.
- Scan de ports importants.
- Detection de ports sensibles.
- Detection des nouveaux appareils.
- Detection des appareils disparus.
- Score de risque par appareil.
- Alertes avec severite.
- Dashboard temps reel avec WebSocket.
- Graphique de latence avec Chart.js.

## Limites

Le projet ne remplace pas un SIEM ou un scanner de vulnerabilites complet.
Il detecte des signaux simples : appareils inconnus, ports sensibles, latence elevee et changements entre scans.
