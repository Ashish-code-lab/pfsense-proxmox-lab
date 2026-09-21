# pfSense Lab Controller on Proxmox VE (`pfsense-lab`)

A clean, professional control dashboard and interactive curriculum guide for building, operating, and automating a pfSense firewall lab on Proxmox VE. It teaches every network and virtualization concept step-by-step, validates the hypervisor environment automatically via a 12-point automated preflight engine, and controls the Proxmox hypervisor through its native REST API.

---

## Key Features

1. **Interactive 12-Step Lab Curriculum**:
   - Covers everything from virtual bridge provisioning (`vmbr1`), pfSense VM creation, VirtIO networking, console initialization, DHCP configuration, firewall rules, NAT port forwards, to DNS resolution.
   - Includes full terminal command boxes with one-click copy, collapsible "Why This Matters" architectural explanations, "Expected Outcome" indicators, and structured "If It Fails" troubleshooting guidance.
   - Per-step progress tracking (checkbox toggles) and Markdown-capable user notes saved persistently in SQLite.
   - Global keyword search across all 12 steps and commands.

2. **12-Point Automated Preflight Engine**:
   - Proxmox node reachability & API ticket authentication
   - CPU virtualization extensions (`vmx`/`svm`) verification
   - WAN bridge (`vmbr0`) and physical uplink detection
   - Isolated LAN bridge (`vmbr1`) absence/presence verification
   - Storage pool availability and free disk capacity checks
   - ISO installation media presence (`pfSense-CE-*.iso`)
   - IP subnet collision detection (ensuring lab LAN does not collide with home router WAN)
   - VM ID collision prevention and resource sizing checks

3. **Centralized Safety Model & Guardrails**:
   - Centralized action registry with 4 safety classifications:
     - `SAFE` (read-only queries, telemetry, consoles)
     - `MUTATING` (starting VMs, creating bridges, taking snapshots)
     - `DISRUPTIVE` (rebooting VMs, applying live network bridge changes)
     - `DESTRUCTIVE` (deleting VMs, rolling back/deleting snapshots)
   - Triple execution modes:
     - **LIVE**: Directly executes operations against the configured Proxmox VE REST API.
     - **DRY-RUN**: Intercepts mutating/destructive actions, returning exact API endpoints, HTTP methods, and payload payloads without modifying hypervisor state.
     - **DEMO**: Fully offline, high-fidelity mock engine simulating realistic VM telemetry, network interfaces, storage pools, and snapshots for learning and staging without a physical hypervisor.
   - Guardrails: All destructive actions require explicit confirmation and are blocked unless `ALLOW_DESTRUCTIVE=True`.
   - Comprehensive audit logging recording timestamp, user, action, safety class, target, execution mode, parameter JSON, result status, and detailed message.

4. **Proxmox Virtual Machine Management**:
   - Real-time VM inventory, CPU, RAM, and disk utilization metrics.
   - Power state management: Start, Shutdown (ACPI), Stop (force kill), Reboot.
   - Snapshot management: Create memory/disk snapshots, view snapshot tree hierarchies, roll back, and delete.
   - Embedded noVNC HTML5 console launcher with dynamic ticket/port resolution.

5. **Integrated Utilities & Tools**:
   - **IPv4 Subnet Calculator**: Netmask, wildcard, CIDR prefix, usable host range, broadcast address, and automated home network collision alerts.
   - **Cryptographic Credential Generator**: Generates high-entropy passwords with configurable length and special characters.
   - **Firewall Rule & NAT Generator**: Generates step-by-step WebGUI instructions and raw pfSense `config.xml` / `pf.conf` stanzas for standard lab scenarios.
   - **Scenario-Based Knowledge Quiz**: 10 scenario-based questions evaluating network isolation, packet filter ordering, and hypervisor architecture, complete with instant grading and answer explanations.

6. **Self-Contained Frontend**:
   - Pure semantic HTML5 + responsive CSS.
   - System font stack (`system-ui`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`, `sans-serif`).
   - Zero external CDNs, npm packages, or third-party web fonts required.
   - Accessible color palette adhering to WCAG AA contrast standards.
   - Server-side SVG sparklines, status indicators, and storage utilization gauges.

---

## System Architecture

```
                       ┌──────────────────────────────────────────────┐
                       │           pfSense Lab Controller             │
                       │     (Python 3.11+ / Flask / SQLite3)         │
                       └───────┬──────────────────────────────┬───────┘
                               │                              │
                     REST API / Demo Engine                 Admin
                               │                              │
        ┌──────────────────────▼───────────────────────┐      │
        │             Proxmox VE Hypervisor            │      │
        │ ┌──────────────────────────────────────────┐ │      │
        │ │ Physical Uplink (eno1/eth0)              │ │      │
        │ └────────────────────┬─────────────────────┘ │      │
        │                      │                       │      │
        │       ┌──────────────▼─────────────┐         │      │
        │       │  vmbr0 (WAN Bridge / DHCP) │         │      │
        │       └──────────────┬─────────────┘         │      │
        │                      │ vtnet0 (WAN)          │      │
        │          ┌───────────▼──────────┐            │      │
        │          │   pfSense Router VM  │            │      │
        │          │      (FreeBSD)       │            │      │
        │          └───────────┬──────────┘            │      │
        │                      │ vtnet1 (LAN)          │      │
        │       ┌──────────────▼─────────────┐         │      │
        │       │ vmbr1 (Isolated LAN Switch)│         │      │
        │       └──────────────┬─────────────┘         │      │
        │                      │                       │      │
        │      ┌───────────────┴───────────────┐       │      │
        │      ▼                               ▼       │      │
        │  [Client VM 1]                  [Client VM 2]│      │
        │  (Linux/Debian)                (Windows Lab) │      │
        └──────────────────────────────────────────────┴──────┘
```
## Home page
<img width="1918" height="1018" alt="image" src="https://github.com/user-attachments/assets/9aa7d740-41e0-4e2e-87fe-9ad0b0d1bff4" />

---

## Getting Started

### 1. Prerequisites
- Python 3.10+ (Python 3.11+ recommended)
- `sqlite3` (built into Python standard library)
- Proxmox VE 7.x or 8.x (optional; fully functional in `DEMO_MODE`)

### 2. Environment Variables & Configuration
Configure environment variables via `.env` or system environment:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | `dev-insecure-secret-key-change-in-production` | Session signing key |
| `DATABASE_PATH` | `instance/pfsense_lab.sqlite` | SQLite database location |
| `DEMO_MODE` | `true` | When true, simulates hypervisor API for standalone demo |
| `DRY_RUN` | `false` | When true, intercepts mutations and logs simulated execution |
| `ALLOW_DESTRUCTIVE`| `false` | Gatekeeper switch required to delete VMs or snapshots |
| `PROXMOX_HOST` | `192.168.1.200` | IP or hostname of Proxmox VE server |
| `PROXMOX_PORT` | `8006` | Proxmox management port (HTTPS) |
| `PROXMOX_USER` | `root@pam` | Proxmox API user |
| `PROXMOX_NODE` | `pve` | Proxmox target node name |
| `PROXMOX_VERIFY_SSL`| `false` | Verify self-signed SSL certificates |
| `PFSENSE_HOST` | `192.168.10.1` | pfSense LAN gateway IP |
| `PFSENSE_USER` | `admin` | pfSense WebGUI admin user |

### 3. Running the Application

To run using Gunicorn (production WSGI):
```bash
gunicorn -b 0.0.0.0:3000 --workers=2 --threads=4 wsgi:app
```
Or via npm wrapper:
```bash
npm start
```

Access the dashboard at `http://localhost:3000`.

### 4. First-Run Setup
Upon initial launch, the application detects an uninitialized database and redirects to `/auth/first-run`. Create the initial administrator username and password (minimum 6 characters).

---

## Testing & Quality Assurance

The test suite runs with `pytest` and provides comprehensive test coverage across blueprints, database state, authorization, safety gates, and preflight calculations:

```bash
# Run the test suite
pytest -v

# Run with test coverage report
pytest --cov=pfsense_lab --cov-report=term-missing
```

All 25 automated tests validate:
- Authentication & brute-force rate-limiting
- First-run administrator onboarding
- 12-step curriculum structural integrity and per-step note persistence
- Preflight calculation engine & rule evaluation
- Centralized safety model validations (`SAFE`, `MUTATING`, `DRY_RUN`, `ALLOW_DESTRUCTIVE`)
- All blueprint view endpoints and server-rendered templates

---

## Assumptions & Design Decisions

1. **Storage Engine**: SQLite was selected without any third-party ORM (e.g. SQLAlchemy) per the strict constraints, using standard Python `sqlite3`, row factories, parameterized queries, and WAL journal mode for lightweight concurrency.
2. **Proxmox API Authentication**: The Proxmox service supports both API Token format (`PVEAPIToken=USER@REALM!TOKENID=UUID`) and credential Ticket/CSRF token workflows. When self-signed SSL certificates are used on local Proxmox installations, SSL verification can be toggled via `PROXMOX_VERIFY_SSL`.
3. **Demo Mode Fidelity**: In `DEMO_MODE=True`, all VM statistics, node metrics, bridges (`vmbr0`, `vmbr1`), storage pools, ISO images, tasks, and snapshots return realistic enterprise virtualization data. Mutating actions in Demo Mode simulate successful state transitions and write audit events without communicating with an external host.
4. **Port Binding**: Dev server and container ingress explicitly bind to port `3000` on `0.0.0.0` to comply with container reverse-proxy requirements.
5. **Chart Generation**: All system gauges, network topology diagrams, and resource bars are generated as server-side SVG strings in `pfsense_lab/charts.py`, avoiding external JavaScript chart libraries or canvas dependencies.
