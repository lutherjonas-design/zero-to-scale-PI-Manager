# zero-to-scale-PI-Manager

### Context & Status
**Active Development (Early Stages)**  
A lightweight, self-hosted automation and orchestration manager built for isolated Raspberry Pi environments. The system acts as a central control plane managing local bare Git repositories, automated backups, and dynamic, dependency-aware Docker container lifecycles (including on-demand container sleep and wake cycles). The project currently runs locally on my Pi and is regularly pushed here as development progresses.

---

### Tech Stack

#### Current Implementation
* **Language:** Python 3
* **API Framework:** FastAPI, Uvicorn
* **IPC / Communication:** Unix Domain Sockets & WebSockets
* **Version Control Ingress:** Local Bare Git Repositories & Custom Git Hooks

#### Planned Architecture
* **Frontend:** React (Administrative Dashboard)
* **Reverse Proxy & Ingress:** Traefik (with Forward Auth)
* **Resilience:** Custom Pi-Watcher (Hardware watchdog daemon) & Automated Backup Solutions

---

## Quick Start & Development Setup

### 0. Handling Shared Dependencies
To synchronize data across decoupled interfaces, the contents of the `shared/` directory must be copied into both the `manager/` and `commandline/` folders. 

In production, this syncing is handled automatically on the Pi via a custom post-receive Git hook. This hook also acts as a safety barrier, preventing the active manager instance from pulling unstable or conflicting structural changes from development branches.

### 1. Installation & Environment Setup
Clone the repository and prepare the virtual environment:
```bash
# Initialize and activate the virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the System
*Ensure your virtual environment is active (`source .venv/bin/activate`) before running these components.*

#### Launch the Core Management Daemon (Server):
```bash
uvicorn manager.main:app --reload
```

#### Interact via the Administrative CLI (Client):
Open a separate terminal and run the CLI utility:
```bash
python client.py -help
```

---

## Architecture & Roadmap

### System Design
The system is split into a low-level local manager daemon, a secure CLI utility, a lightweight HTTP/HTTPS interface, a Traefik container for routing/auth, and a sandboxed Docker infrastructure. The manager container acts as the bridge between the physical local hardware and the Docker Engine API.

To automate this, I configured a bare-repository creator script on my Pi. It automatically initializes new projects with a `service.yml` manifest. This manifest defines how the manager builds, runs, and scales the containers based on specified dependencies. (This setup script will eventually be integrated directly into the Manager or CLI).

![Architecture](./Architecture.png)

### Accomplished (Production Ready)
* **Secure CLI:** Low-overhead command-line interactions established.
* **Socket Communication:** Fully functional asynchronous IPC within the host manager.
* **Structural Refactoring:** Architectural isolation of application layers into clean interface boundaries.

### Current Sprint (In Progress)
* **Service Mocking:** Designing mock service layers, test frameworks, and a central command registry pattern.

### Planned Backlog
1. **Repository Telemetry:** Detail views and status dashboards for active repositories.
2. **Docker Orchestration Layer:** Direct service-to-engine binding using a dedicated `DockerHandler`.
3. **Automated Staging:** Dynamic workspace cloning from bare repositories triggered by commit hooks.
4. **Declarative Manifests:** Schema parsing integration for incoming `service.yml` specifications.
5. **Asynchronous Task Queue:** A prioritized worker pool to handle long-running Docker image builds.
6. **Hardened API Gateway:** Containerized routing, token forwarding, and resource-saving container sleep triggers.
7. **Task Merging & Collision Prevention:** Smart queue logic to intercept, combine, or cancel redundant build jobs when multiple rapid git pushes occur.
