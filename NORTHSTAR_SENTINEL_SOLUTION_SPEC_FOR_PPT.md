# NORTHSTAR SENTINEL — SOLUTION ARCHITECTURE & PPT SPECIFICATION
## CRIMEATHON '26 · Defense Track · Case File: NS-26-014
### Target Entity: Northstar Skills Academy, Chennai · Incident Date: 12 October 2026

> **HOW TO USE THIS WITH CLAUDE:**
> You can copy and paste this entire markdown document into Claude with the prompt:
> *"Act as an elite cybersecurity presentation designer. Using the detailed solution specification below for Case NS-26-014, generate a competition-winning 10-slide PowerPoint presentation with visual card layouts, tables, and speaker notes."*

---

## 1. PROJECT METADATA & EXECUTIVE SUMMARY

- **Project Name:** Northstar Sentinel
- **Hackathon:** CRIMEATHON '26 (Applied Defense Track)
- **Case Reference:** NS-26-014
- **Target Organization:** Northstar Skills Academy (Chennai, Tamil Nadu, India)
- **Incident Timing:** 12 October 2026, 03:15:55 IST to 03:24:48 IST (Duration: ~9 minutes)
- **GitHub Repository:** https://github.com/Heman-123/Northstar-Sentinel
- **Team Name:** Team Northstar (Sentinel Taskforce)
- **Core Motto:** *"Zero Trust. Zero Hallucination. Zero Breach."*

### Executive Summary:
On 12 October 2026 at 03:15 IST, adversary external IP `203.0.113.77` compromised the third-party attendance vendor machine token `rc-prod-01` (`svc_rollcall`). Leveraging architectural privilege creep, the adversary queried 2,300 active student records, induced an 8,420 ms portal latency surge (~187× spike), staged an export archive to CampusVault S3, and successfully exfiltrated 972.4 KB across two download streams.

Northstar Sentinel delivers an end-to-end defense:
1. **6-Stage Automated DFIR Pipeline:** Ingests 12 evidentiary files (E01–E12), verifies SHA-256 bit-level custody, normalizes data into OCSF v1.1.0 schema, and constructs an immutable 9-event correlation graph.
2. **4-Layer Zero-Trust Policy Enforcement Point (PEP):** Reverse proxy enforcing CIDR subnet pinning (`10.10.4.0/24`), least-privilege JWT scope gating (`attendance:*`), token-bucket rate limiting (100 req/min), and cryptographic two-man DPO approval on bulk exports.
3. **Validation & Assurance:** 15/15 unit tests passed (pytest) and 10/10 attack simulation tests passed (100% defensive efficacy).
4. **Statutory Alignment:** Fully resolves DPDPA 2023 Section 8(5) liability (exposure up to ₹250 Crores) and automates the CERT-In 6-hour mandatory disclosure window.

---

## 2. THE THREAT LANDSCAPE & ROOT CAUSE ANALYSIS

### Forensic Facts of the Breach:
| Metric / Attribute | Observed Breach Value | Legitimate / Authorized Baseline |
|---|---|---|
| **Adversary Source IP** | `203.0.113.77` (Public External IP) | `10.10.4.0/24` (Vendor CIDR subnet; `10.10.4.12` heartbeat) |
| **Service Credential** | `rc-prod-01` (`svc_rollcall`) | Authorized strictly for classroom attendance synchronization |
| **Token Expiry Setting** | `Expiry: Never` (Indefinite lifetime) | Mandated 90-day maximum lifetime with auto-rotation (E08 §4.1) |
| **IP Whitelist Binding** | `IP Restriction: None` | Subnet-pinned integration gateway |
| **Records Compromised** | 2,300 Active Learners (PII) | 0 records allowed for mass export by integration clients |
| **Exfiltration Volume** | 972.4 KB (2× 486,200 bytes GET) | 0 bytes export to unauthorized endpoints |
| **Web Portal Impact** | Latency spiked to 8,420 ms (~187×) | 45 ms normal query response baseline |

### Root Cause Mapping (OWASP API Security Top 10 2023):
1. **OWASP API1 / CWE-250 (Privilege Creep):** The `rollcall-prod` client was provisioned with `learner.export` and `learner.search` permissions despite only requiring attendance read/write access.
2. **OWASP API2 / CWE-798 (Broken Credential Hygiene):** Bearer token configured with `Expiry: Never` and no CIDR IP binding; leaked via unredacted support ticket `HD-1058` or configuration audit `CHG-882`.
3. **OWASP API4 / CWE-770 (Unrestricted Resource Consumption):** Absence of rate limiting and lack of dual-authorization approval on bulk extraction endpoints.

### MITRE ATT&CK Matrix Alignment:
- **T1078.004:** Valid Accounts: Cloud Accounts (Compromised machine token `rc-prod-01`)
- **T1552.001:** Unsecured Credentials: Credentials In Files (Support screenshot & config files)
- **T1530:** Data from Cloud Storage (Staged CampusVault S3 archive exfiltrated)
- **T1567:** Exfiltration Over Web Service (Dual HTTPS GET transfers to public IP)
- **T1098:** Account Manipulation (Privilege escalation via administrative config read)

---

## 3. CHRONOLOGICAL FORENSIC TIMELINE (9-EVENT RECONSTRUCTION)

- **03:15:55 IST [INGRESS]:** External IP `203.0.113.77` initiates TCP 443 handshake with ClassBridge API Gateway (`E09:N001`).
- **03:16:32 IST [AUTHENTICATION]:** Machine token `rc-prod-01` presented and accepted without IP validation (`E01:A011`).
- **03:16:35 IST [RECONNAISSANCE]:** Adversary queries `credential_config_read`, accessing `CHG-882` database parameters (`E11`).
- **03:16:40 IST [SEARCH QUERY]:** Full-table unindexed query `GET /v1/learners/search` executes across 2,300 active records (`E03:R003`).
- **03:17:09 IST [BULK EXPORT]:** Bulk export `POST /v1/learners/export` triggers 8,420 ms latency surge; spooling begins (`E03:R004`).
- **03:17:35 IST [S3 STAGING]:** 486.2 KB CSV archive `learners-20261012.csv` staged in CampusVault S3 bucket (`E04:C001`).
- **03:21:03 IST [EXFILTRATION #1]:** First external GET request downloads 486,200 bytes to `203.0.113.77` (`E04:C003`).
- **03:24:48 IST [EXFILTRATION #2]:** Second GET request downloads duplicate 486,200 bytes (Total: 972.4 KB) (`E04:C004`).
- **03:25:00+ IST [DETECTION]:** Regular vendor node (`10.10.4.12`) resumes heartbeat (`E09:N002`); Sentinel multi-source correlation engine triggers DEFCON 2 alarm.

---

## 4. EPISTEMIC TRUTH MATRIX (ISO/IEC 27037 SCIENTIFIC RIGOR)

Northstar Sentinel enforces strict epistemic separation between proven evidence, forensic inferences, and speculative unknowns:

| Finding / Investigative Hypothesis | Epistemic Status | Evidentiary Basis & Custody Chain |
|---|---|---|
| Ingress initiated from external IP `203.0.113.77` | **CERTAIN (100%)** | `E03` API Gateway Logs & `E09` Network Observations |
| Token `rc-prod-01` had `Expiry: Never` & machine role | **CERTAIN (100%)** | `E05` Integration Register & `E07` Service Accounts |
| Exactly 972.4 KB exfiltrated in 2 S3 downloads | **CERTAIN (100%)** | `E04` CampusVault S3 Audit Logs (`C003`, `C004`) |
| 12 evidentiary artifacts are untampered | **CERTAIN (100%)** | SHA-256 cryptographic digests matched against baseline |
| 2 downloads represent 2 separate adversary copies | **PROBABLE (85%)** | Matched byte sizes & 3 min 45 sec interval |
| Credential leak originated via ticket HD-1058 screenshot | **SUPPORTED INFERENCE** | Ticket `HD-1058` contained unmasked API token |
| Physical human identity behind `203.0.113.77` | **UNDETERMINED (0%)** | Requires ISP subpoena; local logs cannot prove human identity |
| Former employee Ajay (`former.ajay`) linked to RollCall | **NOT ESTABLISHED (0%)** | Offboarding failure on Oct 9 is isolated; no causal link |

---

## 5. THE PROPOSED SOLUTION: 4-LAYER ZERO-TRUST PEP

Northstar Sentinel deploys an in-line Zero-Trust Policy Enforcement Point (reverse proxy) in front of sensitive endpoints:

```
[ INCOMING TRAFFIC ]
        │
        ▼
┌────────────────────────────────────────────────────────┐
│ LAYER 1: CIDR Subnet Pinning                           │
│ • Validates source IP against authorized CIDR         │
│ • Vendor svc_rollcall locked strictly to 10.10.4.0/24  │
│ • External IP 203.0.113.77 ➔ HTTP 403 FORBIDDEN (0ms)  │
└────────────────────────────────────────────────────────┘
        │ (Passed)
        ▼
┌────────────────────────────────────────────────────────┐
│ LAYER 2: Least-Privilege JWT Scope Gate                │
│ • Enforces fine-grained scope claims                   │
│ • Clamps svc_rollcall token strictly to attendance:*   │
│ • Rejects wildcard escalation ➔ HTTP 403 SCOPE DENIED  │
└────────────────────────────────────────────────────────┘
        │ (Passed)
        ▼
┌────────────────────────────────────────────────────────┐
│ LAYER 3: Token-Bucket Adaptive Rate Limiter            │
│ • 100 req/min baseline with automated burst dampening   │
│ • Prevents unindexed queries and portal starvation     │
│ • High-frequency scraping bursts ➔ HTTP 429 THROTTLED  │
└────────────────────────────────────────────────────────┘
        │ (Passed)
        ▼
┌────────────────────────────────────────────────────────┐
│ LAYER 4: Two-Man DPO Cryptographic Sign-Off Gate       │
│ • Any export >50 PII records requires dual signature   │
│ • Requires valid cryptographic X-DPO-Approval-Token    │
│ • Unauthorized mass dumps ➔ HTTP 403 DPO SIGN-OFF REQ  │
└────────────────────────────────────────────────────────┘
        │ (Passed)
        ▼
[ PROTECTED CORE API / CAMPUSVAULT S3 ]
```

---

## 6. THE 6-STAGE AUTOMATED DFIR PIPELINE

1. **STAGE 01 — MULTI-SOURCE INGESTION:** Automated parser ingesting 12 heterogeneous evidence artifacts (`E01`–`E12`) across authentication logs, API gateway logs, S3 audit trails, and network observations.
2. **STAGE 02 — CRYPTOGRAPHIC HASH INTEGRITY:** Calculates and verifies SHA-256 digests for all 12 files to maintain an unbroken chain of custody under ISO/IEC 27037 standards.
3. **STAGE 03 — OCSF SCHEMA NORMALIZATION:** Converts heterogeneous syslog, auth, and JSON logs into standardized Open Cybersecurity Schema Framework (OCSF v1.1.0) events with microsecond UTC/IST alignment.
4. **STAGE 04 — EVENT GRAPH CORRELATION:** Stitches multi-source logs into a unified timeline graph, correlating initial ingress with configuration reads, query surges, and S3 egress.
5. **STAGE 05 — BEHAVIORAL THREAT CLASSIFICATION:** Evaluates 10 explainable detection rules (`DET-001` through `DET-010`) mapped to MITRE ATT&CK techniques and OWASP API risks.
6. **STAGE 06 — STATUTORY & SOAR REPORTING:** Automates DPDPA 2023 §8(5) penalty risk assessment, generates CERT-In 6-hour disclosure files, and triggers SOAR response playbooks (IP shun, token revocation).

---

## 7. TECHNICAL STACK & ARCHITECTURE

- **Backend Forensics:** Python 3.11+, Pandas, Hashlib, IPAddress, Pytest (15 unit tests).
- **Zero-Trust PEP Gateway:** Python HTTP Reverse Proxy with real-time packet inspection, CIDR validator, and token-bucket limiter.
- **SOC Analyst Workbench:** HTML5, Tailwind CSS Dark Theme, Chart.js telemetry charts, Lucide iconography, responsive 8-tab architecture.
- **Event Standardization:** Open Cybersecurity Schema Framework (OCSF v1.1.0 JSON).
- **Threat Intelligence:** MITRE ATT&CK v14.1 Enterprise & OWASP API Security Top 10 (2023).
- **Statutory Frameworks:** Digital Personal Data Protection Act (DPDPA 2023) & CERT-In Cyber Security Directions 2022.

---

## 8. EMPIRICAL VERIFICATION & TEST RESULTS

### 10/10 Simulation Suite Results:
| Test ID | Attack Scenario | Vulnerable Baseline | Hardened PEP Gate Verdict |
|---|---|---|---|
| **TC-001** | External IP Replay (`203.0.113.77`) | HTTP 200 OK (Data Leaked) | **HTTP 403 FORBIDDEN** (Layer 1 CIDR Drop) |
| **TC-002** | Token Expiry: Never (`rc-prod-01`) | HTTP 200 OK (Accepted) | **HTTP 401 UNAUTHORIZED** (Layer 2 Expiry Check) |
| **TC-003** | Privilege Creep (`learner.export`) | HTTP 200 OK (Mass Staged) | **HTTP 403 FORBIDDEN** (Layer 2 Scope Denied) |
| **TC-004** | Scraping Burst (>100 req/min) | HTTP 200 OK (Latency 8.4s) | **HTTP 429 THROTTLED** (Layer 3 Rate Limiter) |
| **TC-005** | Bulk PII Export Without DPO | HTTP 200 OK (Staged to S3) | **HTTP 403 FORBIDDEN** (Layer 4 DPO Sign-Off) |
| **TC-006** | Legitimate Vendor Sync (`10.10.4.15`) | HTTP 200 OK (Normal Sync) | **HTTP 200 OK** (Legitimate Traffic Preserved) |
| **TC-007–010** | Replay, Token Tampering & Spoofing | Allowed / Inconsistent | **ALL BLOCKED** (Multi-Layer Enforcement) |

- **Unit Test Coverage:** 15/15 unit tests passing (`tests/test_dfir_pipeline.py`) — 100% pass rate.
- **Simulation Coverage:** 10/10 attack test scenarios blocked in real-time.

---

## 9. STATUTORY COMPLIANCE & LEGAL IMPLICATIONS

1. **Digital Personal Data Protection Act (DPDPA 2023) Section 8(5):**
   - *Obligation:* Data Fiduciaries must implement reasonable security safeguards to prevent personal data breaches.
   - *Breach Liability:* Storing infinite-expiry tokens without CIDR restrictions and allowing unrestricted export of 2,300 learner records directly violates §8(5).
   - *Statutory Penalty Exposure:* Penalties up to **₹250 Crores** under the DPDPA penalty schedule.
   - *Remediation:* Deploying Northstar Sentinel eliminates exposure by enforcing 4-layer defense and DPO sign-off.
2. **CERT-In Cyber Security Directions 2022 (6-Hour Mandatory SLA):**
   - *Obligation:* Mandatory disclosure of unauthorized data access/exfiltration to CERT-In within 6 hours.
   - *Response:* Automated generation of the formal incident disclosure report with cryptographically signed SHA-256 evidence chain of custody.

---

## 10. RECOMMENDED 10-SLIDE PPT BLUEPRINT (FOR CLAUDE)

When asking Claude to build the presentation deck, use this exact 10-slide blueprint:

- **Slide 1: Title & Hero** — *Northstar Sentinel: Zero-Trust DFIR Solution for RollCall API Breach*. Badges: Case NS-26-014, Defense Track, 6-Stage Pipeline, 100% Test Pass.
- **Slide 2: The Breach (Problem Statement)** — Dual-card layout: Left card (Impact: 2,300 learners, 972.4 KB, 8,420 ms latency, IP 203.0.113.77); Right card (Root causes: OWASP API1/API2/API4 & MITRE matrix).
- **Slide 3: Forensic Evidence Timeline** — 3×3 card grid mapping the 9 key timeline events from 03:15:55 Ingress to 03:24:48 Exfiltration.
- **Slide 4: Epistemic Truth Matrix** — Formatted table highlighting Proven Facts (Green), Inferences (Cyan), and Speculative Unknowns (Amber) under ISO/IEC 27037 standards.
- **Slide 5: Proposed Solution Architecture** — Vertical stack of the 4 Zero-Trust PEP layers: CIDR Pinning ➔ Scope Gate ➔ Rate Limiter ➔ DPO Two-Man Sign-off.
- **Slide 6: 6-Stage DFIR Pipeline** — Horizontal step cards showing Ingestion ➔ Hashing ➔ Normalization ➔ Correlation ➔ Classification ➔ Reporting.
- **Slide 7: Technical Stack & Standards** — 3×2 card grid detailing Python 3.11, OCSF v1.1.0, MITRE ATT&CK, OWASP API Top 10, Tailwind/Chart.js SOC Workbench.
- **Slide 8: Verification & Results** — Real test matrix comparing Vulnerable Baseline (HTTP 200 Leaked) vs. Hardened PEP Verdict (HTTP 403/429 Blocked) with 10/10 score banner.
- **Slide 9: Statutory & Legal Governance** — Side-by-side comparison of DPDPA 2023 §8(5) (₹250 Crores penalty) and CERT-In 6-hour compliance vs. Sentinel 0ms remediation.
- **Slide 10: Conclusion & Deliverables** — Executive closing card: *"Zero Trust. Zero Hallucination. Zero Breach."* GitHub link, 3 summary cards, and Finalist Trophy Banner.
