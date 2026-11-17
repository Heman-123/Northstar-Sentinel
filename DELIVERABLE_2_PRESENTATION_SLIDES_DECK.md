# CRIMEATHON ’26 — CASE FILE NS-26-014: DEFENSE TRACK
## FINAL POWERPOINT PRESENTATION (PPT) MASTER SLIDE DECK
**Project Title:** **Northstar Sentinel: Evidence-Driven API Security Monitoring and Incident Response Platform**  
**Repository:** `https://github.com/Heman-123/Northstar-Sentinel.git`  
**Target Case:** The Northstar Learning Services Investigation (Chennai Center)  

---

### SLIDE 1: Title Slide & Project Overview
* **Slide Title:** NORTHSTAR SENTINEL: Evidence-Driven Zero-Trust Defense & DFIR Platform
* **Subtitle:** Autonomous Correlation, Policy Enforcement & Incident Response for Case NS-26-014
* **Track:** DEFENSE TRACK (Tier-1 Applied Cybersecurity)
* **Team Details:**
  * Team Name: Northstar Incident Response Taskforce
  * Repository: `github.com/Heman-123/Northstar-Sentinel`
* **Visual Elements:**
  * Dark-mode badge: `CRIMEATHON'26 FINALIST`
  * Dual-shield graphic showing Forensic Evidence Engine + Zero-Trust Policy Enforcement Point (PEP).

---

### SLIDE 2: Problem Identification & Threat Landscape
* **The Incident (12 October 2026):**
  * Northstar Skills Academy detected three cascading anomalies:
    1. Attendance synchronization latency delays.
    2. Severe learner portal responsiveness degradation (latencies soaring to 8,420ms).
    3. Unexpected staging and exfiltration of 2,300 learner PII records (`learners-20261012.csv`).
* **Root Vulnerability Chain (The "Why"):**
  * **CWE-250 / OWASP API1:2023:** Architectural Privilege Creep — Integration client `rollcall-prod` granted global `learner.export` permissions despite business purpose being strictly attendance synchronization.
  * **CWE-798 / OWASP API2:2023:** Broken Authentication Hygiene — Integration token had `Expiry: Never` and `IP Restriction: None`.
  * **CWE-770 / OWASP API4:2023:** Unrestricted Resource Consumption — Complete absence of rate limiting on search/export endpoints.

---

### SLIDE 3: Forensic Evidence Correlation & Epistemic Matrix
* **The Epistemological Matrix (Judges' Core Evaluation Standard):**
  * **Confirmed Facts:**
    * IP `203.0.113.77` connected at `03:15:55 IST` (`E09:N001`) and authenticated machine account `svc_rollcall` (`E01:A011`).
    * Read config settings at `03:16:35 IST` (`E11:CHG-882`), queried 2,300 records at `03:16:40 IST` (`E03:R003`), and exported database at `03:17:09 IST` (`E03:R004`).
    * CampusVault object downloaded twice totaling 972,400 bytes (`E04:C003`, `C004`).
  * **Supported Inferences:**
    * Secret leaked via support screenshot (`E06:HD-1058`) or read directly via config API (`E11:CHG-882`).
    * Portal latency spike directly caused by 2,300-row unindexed database query.
  * **Epistemic Unknowns (Zero Hallucination Attribution):**
    * Identity/location of human operator behind IP `203.0.113.77`.
    * No proven link between `former.ajay`'s post-termination login and RollCall incident.

---

### SLIDE 4: Proposed Solution: Northstar Sentinel Dual Engine
* **Pillar 1: Evidence-Driven DFIR Intelligence Pipeline (Stages 1–6):**
  * Ingests heterogeneous logs, computes SHA-256 integrity digests, normalizes to unified OCSF schema, executes 9 cross-source correlation rules, and triggers 10 explainable detection rules (DET-001 to DET-010).
* **Pillar 2: Zero-Trust Policy Enforcement Point (PEP Reverse Proxy):**
  * In-line defensive gateway intercepting requests to `ClassBridge` and `CampusVault`:
    1. *Source IP CIDR Pinning:* Restricts vendor integrations strictly to authorized subnets (`10.10.4.0/24`).
    2. *Strict Least-Privilege Scope Gate:* Hard blocks out-of-scope endpoints (HTTP 403).
    3. *Token-Bucket Rate Limiter:* Enforces 10 req/min throttling (HTTP 429).
    4. *Two-Man Export Authorization:* Blocks bulk PII staging without cryptographic DPO sign-off.

---

### SLIDE 5: System Architecture & Workflow Pipeline
* **Flowchart Architecture:**
  ```text
  [Raw Evidence E01-E12] ──► [SHA-256 Hashing] ──► [OCSF Normalizer]
                                                           │
                                                           ▼
  [Zero-Trust PEP Proxy] ◄── [DET 1-10 Rules] ◄── [Correlation Graph]
           │
           ├── Block Non-Whitelisted IP (HTTP 403)
           ├── Block Privilege Creep (HTTP 403)
           ├── Clamp Scraping Bursts (HTTP 429)
           └── Require Two-Man DPO Approval for PII Exports
  ```
* **Interactive Frontend:**
  * Real-time React 18 + Tailwind CSS SOC Command Center providing live packet inspection, scrubbable IST timeline, and live attack-vs-shield simulation.

---

### SLIDE 6: Technologies, Standards & Tools Used
* **Languages & Core Backend:** Python 3.9+ (Standard Library: `hashlib`, `ipaddress`, `csv`, `json`, `http.server`, `unittest`), FastAPI, Uvicorn, Pytest.
* **Frontend Web Application:** React JS 18, Tailwind CSS, Lucide React Icons.
* **Security & Governance Standards:**
  * MITRE ATT&CK Framework: `T1078.004`, `T1552.001`, `T1530`, `T1567`, `T1098`.
  * OWASP API Security Top 10 (2023): `API1`, `API2`, `API4`, `API7`.
  * Open Cybersecurity Schema Framework (OCSF) Event Normalization.
  * Digital Personal Data Protection Act (DPDPA 2023) Compliance Mapping.

---

### SLIDE 7: Experimental Results & Safe Verification
* **Test Harness Execution (`simulation/test_hardened_api.py`):**
  * **10 / 10 Tests Passed (100% Pass Rate)**
* **Before vs. After Defense Metrics:**
  | Metric / Attack Vector | Vulnerable Baseline (Before) | Northstar Sentinel Hardened (After) |
  | :--- | :--- | :--- |
  | External IP Replay (`203.0.113.77`) | **SUCCESS (HTTP 200)** — PII Leaked | **BLOCKED (HTTP 403)** — Unauthorized IP |
  | Out-of-Scope Learner Export | **SUCCESS (HTTP 200)** — Mass Staged | **BLOCKED (HTTP 403)** — Privilege Creep Blocked |
  | Burst Scraping (>10 queries/min) | **ALLOWED (HTTP 200)** — Latency 8.4s | **THROTTLED (HTTP 429)** — Rate Limit Exceeded |
  | Unapproved Bulk PII Export | **STAGED (HTTP 200)** — 2,300 Records | **BLOCKED (HTTP 403)** — DPO Token Missing |
  | Legitimate Sync (`10.10.4.12`) | **ALLOWED (HTTP 200)** | **ALLOWED (HTTP 200)** — Authenticated & Scoped |

---

### SLIDE 8: Future Enhancements & Enterprise Roadmap
1. **Dynamic Ephemeral Secrets with HashiCorp Vault:** Eliminate static tokens; issue 15-minute rolling tokens tied to client mTLS certificates.
2. **AI-Driven Behavioral Baseline Engine:** Machine learning models analyzing API payload entropy and access time-of-day baselines.
3. **Automated SOAR Quarantine Playbook:** Immediate automated token invalidation and firewall IP shunning upon detection of configuration inspection (`credential_config_read`).
4. **Automated DPDPA Regulatory Compliance Reporting:** Instant generation of forensic notification dossiers for India's Data Protection Board within statutory deadlines.

---
**Thank You — Northstar Sentinel Incident Command**  
*Accessible Repository: `https://github.com/Heman-123/Northstar-Sentinel.git`*
