# Northstar Sentinel 🛡️
### Evidence-Driven API Security Monitoring and Incident Response Platform
**CRIMEATHON ’26 — Official Submission: CASE FILE NS-26-014**  
**Selected Track:** `DEFENSE TRACK`  
**Target Organization:** Northstar Skills Academy Pvt. Ltd. (Chennai, India)  
**Repository:** [https://github.com/Heman-123/Northstar-Sentinel.git](https://github.com/Heman-123/Northstar-Sentinel.git)  

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![React Version](https://img.shields.io/badge/react-18.2.0-cyan.svg)](https://reactjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/tailwindcss-3.3-38bdf8.svg)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security Track](https://img.shields.io/badge/Track-DEFENSE-emerald.svg)](#)
[![Tests Passing](https://img.shields.io/badge/Tests-10%2F10%20Passed-brightgreen.svg)](#)

---

## 📌 Executive Overview

**Northstar Sentinel** is an enterprise-grade digital forensics and zero-trust API defense platform engineered specifically for **Case File NS-26-014 (The Northstar Learning Services Investigation)**. 

On 12 October 2026, Northstar Skills Academy detected suspicious activity where an external threat actor leveraged a third-party vendor service identity (`rollcall-prod`) to query and exfiltrate 2,300 learner PII records, causing significant application responsiveness degradation (latency spiking to 8,420 ms) and unapproved cloud storage staging.

Northstar Sentinel delivers:
1. **Cryptographic Chain-of-Custody:** Ingestion and SHA-256 verification of all 12 evidentiary artifacts (E01–E12).
2. **Unified Semantic Normalizer:** Ingests disparate log sources into an OCSF-aligned schema.
3. **Multi-Source Correlation Engine:** Connects authentication, API gateway requests, configuration changes, and cloud storage events across bounded time windows.
4. **Behavioral & Policy Detection Engine:** 10 deterministic, explainable rules (DET-001 to DET-010) with decoupled **Severity** and **Confidence** scoring.
5. **Zero-Trust Policy Enforcement Point (PEP):** Active defensive gateway providing CIDR IP whitelisting, strict least-privilege scoping, token-bucket rate limiting, and dual-authorization approval for bulk exports.
6. **SOC Command Center (React + Tailwind CSS):** A dark-mode web application featuring an interactive timeline, epistemic truth matrix, rule manager, and a live Attack vs. Shield Simulator.

---

## 🏛️ System Architecture

```text
                           EVIDENTIARY LOG FEEDS (E01 - E12)
   [Auth Logs]  [ClassBridge Audits]  [Gateway Logs]  [CampusVault S3]  [Network PCAP]
         │              │                   │                │                │
         └──────────────┴───────────────────┼────────────────┴────────────────┘
                                            ▼
                          ┌───────────────────────────────────┐
                          │   STAGE 1: INGESTION & SHA-256    │
                          │   (Immutable Chain of Custody)    │
                          └─────────────────┬─────────────────┘
                                            ▼
                          ┌───────────────────────────────────┐
                          │     STAGE 2: OCSF NORMALIZATION   │
                          │   (Unified Semantic Event Model)  │
                          └─────────────────┬─────────────────┘
                                            ▼
                          ┌───────────────────────────────────┐
                          │   STAGE 3: CORRELATION ENGINE     │
                          │  (9 Multi-Source Entity Linkages) │
                          └─────────────────┬─────────────────┘
                                            ▼
                          ┌───────────────────────────────────┐
                          │   STAGE 4: DETECTION ENGINE       │
                          │  (DET-001 to DET-010 Rule Suite)  │
                          └─────────────────┬─────────────────┘
                                            ▼
                          ┌───────────────────────────────────┐
                          │   STAGE 5: DECOUPLED RISK MATRIX  │
                          │  (Severity vs. Evidence Weight)   │
                          └─────────────────┬─────────────────┘
                                            │
               ┌────────────────────────────┴───────────────────────────┐
               ▼                                                        ▼
┌───────────────────────────────┐                       ┌───────────────────────────────┐
│     STAGE 6: DFIR REPORT      │                       │ ZERO-TRUST POLICY ENFORCEMENT │
│   (Markdown & JSON Outputs)   │                       │      POINT (PEP GATEWAY)      │
│  • Epistemic Truth Matrix     │                       │  • Source IP CIDR Pinning     │
│  • Chronological Timeline     │                       │  • Least-Privilege Scope Gate │
│  • Regulatory DPDPA Audit     │                       │  • Token-Bucket Rate Limiter  │
└───────────────────────────────┘                       │  • Two-Man Export Gate        │
                                                        └───────────────┬───────────────┘
                                                                        ▼
                                                        ┌───────────────────────────────┐
                                                        │ REACT + TAILWIND CSS COMMAND  │
                                                        │  • Interactive IST Timeline   │
                                                        │  • Live Attack vs Shield Lab  │
                                                        │  • Epistemic Matrix Inspector │
                                                        └───────────────────────────────┘
```

---

## ⚖️ The Epistemological Matrix: Facts vs. Inferences vs. Unknowns

In strict compliance with professional DFIR tradecraft and competition evaluation guidelines, Northstar Sentinel enforces zero-hallucination attribution:

| Category | Finding & Forensic Evidence | Case Reference |
| :--- | :--- | :--- |
| **Confirmed Facts (Log-Proven)** | External IP `203.0.113.77` connected at `03:15:55 IST` and authenticated `svc_rollcall`. | `E09:N001`, `E01:A011` |
| **Confirmed Facts (Log-Proven)** | Settings read via API at `03:16:35 IST`, followed by 2,300 learner search & export. | `E11:CHG-882`, `E03:R003, R004` |
| **Confirmed Facts (Log-Proven)** | `learners-20261012.csv` (486.2 KB) created in CampusVault and downloaded twice. | `E04:C001, C003, C004` |
| **Confirmed Facts (Log-Proven)** | Integration Register records `Expiry: Never` and `IP Restriction: None`. | `E05:INT-01` |
| **Confirmed Facts (Log-Proven)** | Former employee `former.ajay` authenticated on Oct 9, 9 days post-departure. | `E01:A006`, `E07:USR-04` |
| **Supported Inferences** | Credential exposed via ticket screenshot (`HD-1058`) or config read (`CHG-882`). | `E06:HD-1058`, `E12` |
| **Supported Inferences** | Latency surge (8,420ms) was caused by unindexed 2,300-row database query. | `E03:R004`, `E02:P004` |
| **Supported Inferences** | Attendance sync failure was caused by rate-limit & thread contention. | `E06:HD-1041`, `E03:R004` |
| **Confirmed Unknowns** | Physical human identity or location behind IP `203.0.113.77`. | Undetermined |
| **Confirmed Unknowns** | Whether 2 downloads represent 2 unique copies or an interrupted TCP stream. | Undetermined |
| **Confirmed Unknowns** | Whether downloaded learner data was distributed externally or destroyed. | Undetermined |
| **Confirmed Unknowns** | Any connection between `former.ajay` and the RollCall incident (treated as separate). | Disconnected |

---

## 🛡️ Detection Rules Catalog (DET-001 to DET-010)

| Rule ID | Rule Title | Severity | Confidence | MITRE ATT&CK | OWASP API |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **DET-001** | Unrecognized Ingress Source IP for Vendor Service Account | **CRITICAL** | **HIGH** | `T1078.004` | API2:2023 |
| **DET-002** | Architectural Privilege Creep: Excessive Integration Scopes | **HIGH** | **HIGH** | `T1098` | API1:2023 |
| **DET-003** | Unthrottled Bulk Learner PII Data Acquisition | **CRITICAL** | **HIGH** | `T1530` | API4:2023 |
| **DET-004** | Perpetual Production Credential with Indefinite Validity | **HIGH** | **HIGH** | `T1552.001` | API2:2023 |
| **DET-005** | Unrestricted Network Perimeter Policy for External Integration | **HIGH** | **HIGH** | `T1190` | API2:2023 |
| **DET-006** | Configuration Read Invocation on Secret Settings Preceding Extraction | **HIGH** | **HIGH** | `T1087 / T1552`| API7:2023 |
| **DET-007** | Staged Learner Export Object Retrieval from Cloud Storage | **CRITICAL** | **HIGH** | `T1567` | API1:2023 |
| **DET-008** | Dormant Terminated Account Post-Offboarding Successful Auth | **HIGH** | **HIGH** | `T1078.002` | API2:2023 |
| **DET-009** | Unapproved Bulk Learner Data Export (Missing DPO Justification) | **HIGH** | **HIGH** | `T1560` | API1:2023 |
| **DET-010** | Duplicate / Repeated Retrieval of Sensitive Staged Export | **MEDIUM** | **HIGH** | `T1567.002` | API1:2023 |

---

## 🚀 Quickstart & Execution Instructions

### Prerequisites
* **Python:** 3.9 or higher (standard library execution)
* **Node.js:** 16.x or higher & npm (for React Dashboard)
* **Operating System:** Windows, Linux, or macOS

### 1. Clone the Repository
```bash
git clone https://github.com/Heman-123/Northstar-Sentinel.git
cd Northstar-Sentinel
```

### 2. Run the 6-Stage Python DFIR Pipeline
The pipeline runs entirely out of the box with zero external dependencies:
```bash
# Stage 1: Ingest & Compute SHA-256 Hashes
python src/01_verify_ingest.py

# Stage 2: Normalize Events to OCSF Standard
python src/02_normalize.py

# Stage 3: Correlate Multi-Source Events
python src/03_correlate.py

# Stage 4: Run Behavioral Detection Rules (DET 1-10)
python src/04_detect.py

# Stage 5: Calculate Decoupled Risk & Priority Matrix
python src/05_risk_scoring.py

# Stage 6: Generate Formal DFIR Investigation Report
python src/06_generate_report.py
```
*Generated reports and matrices will be stored in `data/processed/` and `reports/`.*

### 3. Run Automated Verification Tests
Execute the comprehensive test harness:
```bash
# Run security test suite against Zero-Trust PEP
python simulation/test_hardened_api.py

# Run end-to-end pipeline test suite
python tests/test_pipeline.py
```

### 4. Windows One-Click Execution (Instant Setup)
For Windows users (or testing without Node.js/npm), run these scripts directly from PowerShell or CMD:
```powershell
# 1. Run full 6-stage DFIR pipeline & 11 automated security tests
.\run_pipeline.bat

# 2. Launch Enterprise SOC Command Center (Opens Splunk ES-inspired Workbench in browser)
.\start_soc_dashboard.bat

# 3. Simulate live attack traffic against Zero-Trust PEP
.\fire_attack.bat
```
*The SOC Dashboard opens immediately at `http://127.0.0.1:8765` or by opening `dashboard.html` directly in any browser (Chrome, Edge).*

### 5. Launch via React (Optional Node.js Development)
```bash
cd frontend
npm install
npm start
```
*Open [http://localhost:3000](http://localhost:3000) to view the React build.*

---

## 🧪 Automated Test Results Summary

```text
======================================================================
 NORTHSTAR SENTINEL - DEFENSIVE TEST SUITE EXECUTION
======================================================================
test_01_legitimate_attendance_sync_allowed ... ok
test_02_learner_search_denied_for_rollcall_scope ... ok
test_03_bulk_learner_export_denied_for_rollcall ... ok
test_04_unapproved_external_source_ip_denied ... ok
test_05_spoofed_or_bogus_ip_string ... ok
test_06_rate_limiting_enforcement ... ok
test_07_course_catalog_access_denied_without_scope ... ok
test_08_bulk_export_requires_dual_authorization_token ... ok
test_09_bulk_export_permitted_with_valid_dpo_token ... ok
test_10_unknown_client_rejected ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.048s

OK (100% Pass Rate)
```

---

## 📁 Repository Structure

```text
Northstar-Sentinel/
│
├── README.md                                  # Complete Project Documentation
├── DELIVERABLE_1_ONE_PAGE_PROBLEM_STATEMENT.md # Hackathon Deliverable 1
├── DELIVERABLE_2_PRESENTATION_SLIDES_DECK.md   # Hackathon Deliverable 2 (PPT Deck)
├── DELIVERABLE_4_DEMO_VIDEO_SCRIPT.md          # Hackathon Deliverable 4 (Demo Script)
├── GIT_PUSH_GUIDE.md                           # Step-by-Step Push Instructions
├── requirements.txt                            # Python Dependencies
│
├── data/
│   ├── raw/                                    # Original Case Evidence (E01-E12)
│   └── processed/                              # Processed Hashes, Events & Detections
│
├── src/                                        # Core DFIR & Detection Pipeline
│   ├── 01_verify_ingest.py                     # SHA-256 Hashing & Ingestion
│   ├── 02_normalize.py                         # Unified OCSF Normalizer
│   ├── 03_correlate.py                         # Graph & Entity Correlation
│   ├── 04_detect.py                            # Behavioral Rule Engine (DET-01 to 10)
│   ├── 05_risk_scoring.py                      # Decoupled Severity & Confidence Scoring
│   ├── 06_generate_report.py                   # Automated DFIR Report Generator
│   └── gateway_defense.py                      # Zero-Trust Policy Enforcement Point (PEP)
│
├── simulation/                                 # Safe Local Simulation Lab
│   ├── mock_api_server.py                      # Dual-Mode Demo Server (Port 8765)
│   └── test_hardened_api.py                    # 10 Automated Defensive Tests
│
├── tests/                                      # Pipeline Unit Tests
│   └── test_pipeline.py
│
├── reports/                                    # Generated Forensic Reports
│   └── NORTHSTAR_SENTINEL_INVESTIGATION_REPORT.md
│
└── frontend/                                   # React + Tailwind CSS SOC Dashboard
    ├── package.json
    ├── tailwind.config.js
    ├── public/
    └── src/
        ├── App.js                              # Main Dashboard Component
        ├── data/incidentData.js                # Embedded Forensic Telemetry
        └── components/
            ├── Header.jsx                      # Navigation & Status Bar
            ├── MetricsOverview.jsx             # Key Performance Indicators
            ├── IncidentTimeline.jsx            # Scrubbable Visual IST Timeline
            ├── LiveDefenseSimulator.jsx        # Attack vs. Shield Interactive Lab
            ├── DetectionMatrix.jsx             # Rule Inspector (DET-01 to DET-10)
            ├── EpistemicMatrix.jsx             # Facts vs. Inferences vs. Unknowns
            └── EvidenceChainOfCustody.jsx       # SHA-256 Digest Vault
```

---

## 🔒 Confidentiality & Safe Harbors Compliance

* **Synthetic Data Only:** All learner records, credentials, IP addresses (`203.0.113.0/24`, `198.51.100.0/24`), and employee identities are synthetic and local to this fictional case study.
* **No External Scanning:** The local mock server binds strictly to `127.0.0.1:8765`. Zero external networks, public IP addresses, or real-world targets are contacted.
* **No Confidential Data:** No real passwords, live API keys, or production tokens are committed to this repository.

---
**Northstar Sentinel Taskforce | CRIMEATHON ’26 Finalist**  
*Lead Author & Maintainer: Heman-123*
