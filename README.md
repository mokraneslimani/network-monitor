# Network Monitoring Dashboard

Projet de supervision reseau developpe avec Python, FastAPI, Nmap et un dashboard web temps reel.

L'objectif du projet est de montrer des competences a la fois en reseau et en DevOps :

- detection des appareils presents sur un reseau local ;
- utilisation de Nmap et du ping pour collecter des informations reseau ;
- analyse simple des ports ouverts et des signaux de risque ;
- exposition des resultats via une API FastAPI et un WebSocket ;
- affichage dans un dashboard web ;
- tests automatises avec Pytest ;
- integration continue avec GitHub Actions ;
- dockerisation pour un deploiement Linux avec acces au reseau de l'hote.

## Fonctionnalites

- Scan du reseau local.
- Detection des appareils connectes.
- Recuperation des informations principales : IP, MAC, hostname, vendor, statut.
- Mesure de latence avec `ping3`.
- Scan de ports avec Nmap.
- Detection de ports sensibles.
- Calcul d'un score de risque par appareil.
- Generation d'alertes avec niveau de severite.
- Detection des nouveaux appareils et des appareils disparus.
- Dashboard web servi par FastAPI.
- Mise a jour temps reel via WebSocket.
- Graphique de latence avec Chart.js.
- Sauvegarde des resultats dans des fichiers JSON.

## Architecture

```text
network_monitoring_project/
  backend/
    __init__.py
    main.py       API FastAPI, routes HTTP, WebSocket, dashboard
    scanner.py    scan reseau, Nmap, ping, ports
    risk.py       calcul du score de risque et alertes
    storage.py    lecture/ecriture JSON
  frontend/
    index.html    interface web
    app.js        logique dashboard + WebSocket
    style.css     styles
  tests/
    test_risk.py
    test_storage.py
  data/
    devices.json  donnees generees localement
    alerts.json   alertes generees localement
  scanner.py      scanner console
  requirements.txt
  requirements-dev.txt
  Dockerfile
  docker-compose.yml
  .dockerignore
  .env.example
  .github/workflows/ci.yml
```

## Technologies

- Python
- FastAPI
- Uvicorn
- WebSocket
- Nmap
- python-nmap
- ping3
- python-dotenv
- HTML / CSS / JavaScript
- Chart.js
- Pytest
- GitHub Actions
- Docker
- Docker Compose

## Prerequis

### Pour le mode local Windows

- Python 3.12 ou plus recent.
- Nmap installe sur la machine.
- Git.

Verifier Python :

```powershell
python --version
```

Verifier Nmap :

```powershell
nmap --version
```

Si Nmap n'est pas installe, le scanner ne pourra pas fonctionner correctement.

### Pour le mode Docker Linux

- Une machine Linux.
- Docker.
- Docker Compose.

Le mode Docker utilise `network_mode: host`, qui est recommande sur Linux pour donner au scanner une visibilite directe sur le reseau de l'hote.

## Installation locale

Depuis la racine du projet :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Pour installer aussi les outils de test :

```powershell
python -m pip install -r requirements-dev.txt
```

## Configuration

Le projet utilise un fichier `.env` pour eviter de coder certaines valeurs en dur.

Créer un fichier `.env` a partir de l'exemple :

```powershell
copy .env.example .env
```

Exemple :

```env
SCAN_NETWORK=192.168.1.0/24
SCAN_INTERVAL=60
PORTS_TO_SCAN=22,80,443,3306,8080
```

Variables :

- `SCAN_NETWORK` : reseau a scanner.
- `SCAN_INTERVAL` : intervalle entre deux scans dans le scanner console.
- `PORTS_TO_SCAN` : liste des ports analyses par Nmap.

Le fichier `.env` est ignore par Git. Le fichier `.env.example` reste dans le depot pour documenter la configuration.

## Lancement local Windows

Lancer le dashboard :

```powershell
python -m uvicorn backend.main:app --reload
```

Puis ouvrir :

```text
http://localhost:8000
```

Verifier l'API :

```text
http://localhost:8000/health
```

Resultat attendu :

```json
{"status":"ok"}
```

Lancer le scanner console :

```powershell
python .\scanner.py
```

## Lancement Docker Linux

Le mode Docker est prevu pour un hote Linux afin d'utiliser le reseau de la machine hote.

Construire et lancer :

```bash
docker compose up --build -d
```

Voir les logs :

```bash
docker compose logs -f
```

Arreter :

```bash
docker compose down
```

Acceder au dashboard :

```text
http://IP_DE_LA_MACHINE_LINUX:8000
```

Le fichier `docker-compose.yml` utilise :

```yaml
network_mode: "host"
```

Ce choix permet au conteneur Docker d'utiliser directement le reseau de l'hote Linux. C'est important pour Nmap, le ping et les scans reseau.

Des capacites reseau sont aussi ajoutees :

```yaml
cap_add:
  - NET_ADMIN
  - NET_RAW
```

Elles permettent d'autoriser certains usages reseau bas niveau sans donner directement tous les privileges du mode `privileged`.

## Tests

Les tests automatises se concentrent sur les parties deterministes du projet :

- calcul de risque ;
- generation d'alertes ;
- comparaison entre anciens et nouveaux appareils.

Lancer les tests :

```powershell
python -m pytest -v
```

Les tests ne lancent pas un vrai scan reseau. Le scan depend de Nmap, du reseau local, du pare-feu et des permissions systeme. Il est donc valide par test fonctionnel manuel.

## CI/CD

Le projet utilise GitHub Actions pour l'integration continue.

Le workflow `.github/workflows/ci.yml` se lance a chaque push ou pull request.

Il effectue les actions suivantes :

1. recuperation du code ;
2. installation de Python ;
3. installation de Nmap ;
4. installation des dependances de developpement ;
5. execution des tests Pytest ;
6. verification que l'image Docker se construit correctement.

Commande executee pour les tests :

```bash
python -m pytest -v
```

Commande executee pour verifier Docker :

```bash
docker build -t network-monitoring .
```

Cette CI permet de verifier automatiquement que le code reste testable et que la configuration Docker est valide.

## Choix d'architecture

Le projet garde une architecture simple :

```text
frontend -> API FastAPI -> scanner reseau -> analyse risque -> dashboard
```

Ce choix permet d'avoir une application facile a lancer et a presenter.

Pour le mode Linux DevOps, Docker est utilise avec le mode reseau `host`. Ainsi, le scanner lance depuis le conteneur peut acceder au reseau reel de l'hote Linux.

Une architecture plus avancee pourrait separer le scanner et l'API :

```text
scanner worker -> stockage -> API -> dashboard
```

Cette separation serait plus adaptee a un environnement de production plus complexe, mais elle ajouterait aussi plus de composants a gerer. Pour ce projet, l'architecture actuelle reste volontairement simple, fonctionnelle et demonstrable.

## Difficultes rencontrees et solutions

### Acces au reseau depuis Docker

Probleme :

Un conteneur Docker utilise normalement un reseau isole. Dans ce mode, Nmap peut ne pas voir correctement le reseau local.

Solution :

Pour Linux, le projet utilise :

```yaml
network_mode: "host"
```

Cela permet au conteneur d'utiliser directement les interfaces reseau de l'hote.

Limite :

Ce mode est surtout pertinent sur Linux. Sur Windows avec Docker Desktop, le comportement reseau n'est pas equivalent. Pour cette raison, le mode local Python reste recommande pour le developpement Windows.

### Permissions reseau

Probleme :

Nmap et le ping peuvent necessiter des permissions reseau particulieres.

Solution :

Le fichier `docker-compose.yml` ajoute :

```yaml
cap_add:
  - NET_ADMIN
  - NET_RAW
```

Cela donne au conteneur les capacites necessaires pour certains usages reseau sans utiliser directement `privileged: true`.

### WebSocket avec Uvicorn

Probleme :

Le dashboard utilise un WebSocket sur `/ws`. Uvicorn doit etre installe avec le support WebSocket.

Solution :

Le fichier `requirements.txt` utilise :

```text
uvicorn[standard]
```

Cela installe les dependances necessaires au fonctionnement du WebSocket.

### Tests et scan reseau

Probleme :

Un vrai scan reseau n'est pas stable dans une CI, car il depend du reseau local, de Nmap, du pare-feu et des droits systeme.

Solution :

Les tests automatises ciblent les modules deterministes comme `risk.py` et `storage.py`. Le scan reseau est valide manuellement dans l'environnement cible.

## Securite et limites

Ce projet est un outil de demonstration et d'apprentissage. Il ne remplace pas :

- un SIEM ;
- un IDS/IPS ;
- un scanner de vulnerabilites complet ;
- une solution de monitoring de production.

Le projet detecte des signaux simples :

- appareils inconnus ;
- hostname inconnu ;
- fabricant inconnu ;
- ports sensibles ouverts ;
- latence elevee ;
- apparition ou disparition d'appareils.

Le scan doit etre execute uniquement sur un reseau que vous possedez ou pour lequel vous avez une autorisation explicite.

## Commandes utiles

Lancer en local :

```powershell
python -m uvicorn backend.main:app --reload
```

Lancer le scanner console :

```powershell
python .\scanner.py
```

Lancer les tests :

```powershell
python -m pytest -v
```

Lancer avec Docker sur Linux :

```bash
docker compose up --build -d
```

Voir les logs Docker :

```bash
docker compose logs -f
```

Arreter Docker :

```bash
docker compose down
```

## Competences mises en avant

- Programmation Python.
- Creation d'une API avec FastAPI.
- Utilisation de WebSocket pour le temps reel.
- Scan reseau avec Nmap.
- Analyse de ports et scoring de risque.
- Gestion de fichiers JSON.
- Tests unitaires avec Pytest.
- Configuration par variables d'environnement.
- Versioning avec Git.
- CI avec GitHub Actions.
- Dockerisation d'une application Python.
- Deploiement Linux avec Docker Compose et `network_mode: host`.
- Analyse des contraintes reseau liees aux conteneurs.
