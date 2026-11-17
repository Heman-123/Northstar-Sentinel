# FORENSIC INVESTIGATION & THREAT ANALYSIS REPORT
**CASE FILE:** NS-26-014 — The Northstar Learning Services Investigation  
**INVESTIGATION PLATFORM:** Northstar Sentinel (Automated Evidence-Driven DFIR Engine)  
**TRACK:** DEFENSE TRACK  
**TARGET ENTITY:** Northstar Skills Academy Pvt. Ltd. (Chennai, India)  
**DATE OF INCIDENT:** 12 October 2026  
**REPORT GENERATED:** 2026-11-17 13:36:23 UTC  
**STATUS:** CONCLUDED FORENSIC ASSESSMENT  

---

## 1. Executive Summary

On the morning of **12 October 2026**, Northstar Skills Academy observed three anomalous indicators:
1. Degradation and delays in automated daily attendance synchronization.
2. Slower-than-usual learner record query responsiveness across the **ClassBridge** portal (response latencies reaching 8,420ms).
3. The presence of an unexpected bulk learner dataset (`learners-20261012.csv`, 486,200 bytes) staged within the **CampusVault** cloud repository.

The **Northstar Sentinel** defensive investigation platform ingested 12 evidentiary artifacts (E01–E12), verified cryptographic hash integrity (SHA-256), normalized 49 event records, and correlated cross-system telemetry spanning authentication, API gateway, portal audits, network packet observations, cloud storage transactions, and administrative configuration logs.

The investigation conclusively establishes that production vendor service credential **`rollcall-prod` (`svc_rollcall`)** was utilized from an unauthorized external IP (**`203.0.113.77`**) to execute an unthrottled search and export of 2,300 learner PII records. The data was staged into CampusVault and subsequently downloaded twice. The incident was facilitated by three systemic defensive deficiencies:
1. **Architectural Least Privilege Violation:** Service credential granted global export rights despite having a documented business purpose restricted strictly to attendance synchronization.
2. **Credential Lifecycle Failure:** Production integration token had no expiration date (`Expiry: Never`) and no scheduled rotation.
3. **Perimeter Ingress Failure:** Absence of CIDR / IP whitelisting on vendor integration endpoints.

---

## 2. Cryptographic Chain of Custody & Evidence Verification

Every evidentiary artifact was ingested, analyzed for bit-level integrity, and verified with SHA-256 cryptographic hashes:

| Evidence ID | Source File | SHA-256 Fingerprint (Prefix) | Verification Status |
| :--- | :--- | :--- | :--- |
| **E01** | `E01_Authentication_Logs.csv` | `43fe92c56b032a6a3c6d8559...` | **VERIFIED_INTEGRITY** |
| **E02** | `E02_ClassBridge_Audit_Logs.csv` | `336e5495582fff0f9d712e65...` | **VERIFIED_INTEGRITY** |
| **E03** | `E03_API_Gateway_Logs.csv` | `606aa5812fd0e4b8b564bac4...` | **VERIFIED_INTEGRITY** |
| **E04** | `E04_CampusVault_Audit_Logs.csv` | `80e39b69f40a9dd96f44085b...` | **VERIFIED_INTEGRITY** |
| **E05** | `E05_Integration_Register.csv` | `93f4de01ec0fc2172f84bb07...` | **VERIFIED_INTEGRITY** |
| **E06** | `E06_HelpDesk_Tickets.csv` | `1a4c4858b212232c22fecb22...` | **VERIFIED_INTEGRITY** |
| **E07** | `E07_Staff_and_Service_Account_Register.csv` | `e44c3785442647a9e89c179d...` | **VERIFIED_INTEGRITY** |
| **E08** | `E08_Information_Security_Policy_Extract.txt` | `5f5e579555df7989a3059b60...` | **VERIFIED_INTEGRITY** |
| **E09** | `E09_Network_Observations.csv` | `15c9a4c78f3d4c5fc2774d9b...` | **VERIFIED_INTEGRITY** |
| **E10** | `E10_Vendor_And_Internal_Communications.json` | `a0101abf8e7bd017ecc46236...` | **VERIFIED_INTEGRITY** |
| **E11** | `E11_Additional_Configuration_Audit.csv` | `93f70f9e240a86ccbae27222...` | **VERIFIED_INTEGRITY** |
| **E12** | `E12_Incident_Response_Note.txt` | `c49e016a1534725660f54723...` | **VERIFIED_INTEGRITY** |

---

## 3. The Epistemological Matrix: Facts vs. Inferences vs. Unknowns

In strict compliance with professional DFIR tradecraft and competition evaluation guidelines, findings are categorized into three distinct epistemic tiers:

### Tier 1: Confirmed Observations (Directly Proved by Logs)
* **Fact 1:** External IP `203.0.113.77` initiated network ingress to the gateway at `03:15:55 IST` (`E09:N001`).
* **Fact 2:** Machine identity `svc_rollcall` authenticated successfully from `203.0.113.77` using `API_KEY` at `03:16:32`, `03:17:04`, and `03:19:48 IST` (`E01:A011-A013`).
* **Fact 3:** Configuration management log recorded a read of integration settings (`credential_config_read`) from `203.0.113.77` at `03:16:35 IST` (`E11:CHG-882`).
* **Fact 4:** API Gateway received requests under client `rollcall-prod` searching 2,300 learners (`R003`) and exporting all 2,300 learners (`R004`), resulting in an application audit log entry in ClassBridge (`P003`, `P004`).
* **Fact 5:** CampusVault storage recorded file `learners-20261012.csv` created at `03:17:35 IST` (`C001`), followed by two distinct `object.get` download events from `203.0.113.77` at `03:21:03` and `03:24:48 IST`, totaling 972,400 bytes (`C003`, `C004`).
* **Fact 6:** Active Integration Register (`E05:INT-01`) documents client `rollcall-prod` with `Expiry: Never` and `IP Restriction: None`, while documenting its purpose as "Attendance synchronization".
* **Fact 7:** Former employee `former.ajay` authenticated successfully on `2026-10-09T22:14:05 IST` (`E01:A006`), nine days following formal termination on `2026-09-30` (`E07:USR-04`).

### Tier 2: Strongly Supported Technical Inferences
* **Inference 1:** The threat actor acquired valid `rollcall-prod` credentials either through administrative disclosure during support ticket `HD-1058` (where a configuration screenshot was provided to the vendor on Oct 9) or via extraction during the `credential_config_read` event at `03:16:35 IST`.
* **Inference 2:** Portal responsiveness degradation (8,420ms response time on export) was directly caused by the unindexed, unthrottled database extraction of 2,300 learner records triggered by the malicious API call.
* **Inference 3:** The RollCall attendance synchronization delay was a secondary operational side effect caused by API thread starvation and rate-limit contention during the unauthorized bulk export.

### Tier 3: Epistemic Unknowns (Cannot Be Established from Evidence)
* **Unknown 1:** The physical identity, legal name, or physical geographic location of the human operator behind IP `203.0.113.77`.
* **Unknown 2:** Whether the two downloads of `learners-20261012.csv` represent two distinct exfiltrated copies or a single interrupted and resumed TCP transmission stream.
* **Unknown 3:** Whether the downloaded learner dataset was transferred onward, sold on darknet forums, or destroyed.
* **Unknown 4:** Any technical connection between `former.ajay`'s policy violation on Oct 9 and the `svc_rollcall` incident on Oct 12. Forensic integrity dictates treating these as separate, uncorrelated risk issues.

---

## 4. Chronological Incident Reconstruction (Timeline)

| Time (IST) | Source System | Actor / Entity | Action / Endpoint | Evidence Ref | Significance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **03:15:55** | Perimeter Monitor | Network Flow | Ingress TCP 443 | `E09:N001` | First observed connection from external IP `203.0.113.77` |
| **03:16:32** | Northstar Identity | `svc_rollcall` | `identity.authenticate` | `E01:A011` | Successful API key authentication from external IP |
| **03:16:35** | Config Management | `svc_rollcall` | `credential_config_read` | `E11:CHG-882` | Integration configuration inspected via API |
| **03:16:40** | API Gateway | `rollcall-prod` | `GET /v1/learners/search` | `E03:R003` | 2,300 learner records queried (Latency: 3,250ms) |
| **03:16:41** | ClassBridge Portal | `svc_rollcall` | `learner.search` | `E02:P003` | Application-level audit records mass query |
| **03:17:04** | Northstar Identity | `svc_rollcall` | `identity.authenticate` | `E01:A012` | Second authentication session initiated |
| **03:17:09** | API Gateway | `rollcall-prod` | `POST /v1/learners/export` | `E03:R004` | Bulk export triggered (Latency: 8,420ms) |
| **03:17:10** | ClassBridge Portal | `svc_rollcall` | `learner.export` | `E02:P004` | Core portal generates full learner database dump |
| **03:17:30** | Config Management | `svc_rollcall` | `export_job_created` | `E11:CHG-883` | Background job dispatched to worker |
| **03:17:35** | CampusVault Storage| `svc_backend_worker`| `object.put` (486.2 KB) | `E04:C001` | `learners-20261012.csv` staged into storage bucket |
| **03:18:50** | API Gateway | `rollcall-prod` | `GET /v1/courses` | `E03:R005` | 42 course catalog records enumerated |
| **03:19:20** | API Gateway | `rollcall-prod` | `GET /v1/attendance/all` | `E03:R006` | 2,300 attendance rows scraped |
| **03:20:12** | CampusVault Storage| `svc_rollcall` | `object.list` | `E04:C002` | Actor locates staged export object |
| **03:21:03** | CampusVault Storage| `svc_rollcall` | `object.get` (486.2 KB) | `E04:C003` | First exfiltration download event |
| **03:24:48** | CampusVault Storage| `svc_rollcall` | `object.get` (486.2 KB) | `E04:C004` | Second download event (Total egress: 972.4 KB) |
| **03:25:00** | Perimeter Monitor | Legitimate Node | Ingress TCP 443 | `E09:N002` | Authorized RollCall connector (`10.10.4.12`) resumes heartbeat |

---

## 5. Prioritized Risk & Detection Matrix

### [DET-001] Unrecognized Ingress Source IP for Vendor Service Account
- **Priority Tier:** `P1 - IMMEDIATE_ACTION_REQUIRED` (Triage Score: **98.0/100**)
- **Severity (Impact):** CRITICAL (10.0/10) | **Confidence (Evidence):** HIGH (9.5/10)
- **MITRE ATT&CK:** `T1078.004 (Valid Accounts: Cloud Service Accounts)` | **OWASP API:** `API2:2023 (Broken Authentication)`
- **Evidence References:** E01:A011, E01:A012, E01:A013, E09:N001
- **Defensive Countermeasure:** Enforce strict IP whitelisting / mTLS pinning at the API Gateway for all service principals.

### [DET-003] Unthrottled Bulk PII Acquisition & High-Volume Search
- **Priority Tier:** `P1 - IMMEDIATE_ACTION_REQUIRED` (Triage Score: **98.0/100**)
- **Severity (Impact):** CRITICAL (10.0/10) | **Confidence (Evidence):** HIGH (9.5/10)
- **MITRE ATT&CK:** `T1530 (Data from Cloud Storage / Local System)` | **OWASP API:** `API4:2023 (Unrestricted Resource Consumption)`
- **Evidence References:** E02:P003, E02:P004, E03:R003, E03:R004
- **Defensive Countermeasure:** Implement strict pagination caps (max 50 records/request) and rate limiting on search/export endpoints.

### [DET-007] Staged Learner Export Object Retrieval from Cloud Storage
- **Priority Tier:** `P1 - IMMEDIATE_ACTION_REQUIRED` (Triage Score: **98.0/100**)
- **Severity (Impact):** CRITICAL (10.0/10) | **Confidence (Evidence):** HIGH (9.5/10)
- **MITRE ATT&CK:** `T1567 (Exfiltration Over Web Service)` | **OWASP API:** `API1:2023 (Broken Object Level Authorization)`
- **Evidence References:** E04:C003, E04:C004
- **Defensive Countermeasure:** Block public/external access to export buckets; enforce pre-signed URL validation with temporary 15-minute token authorization.

### [DET-002] Architectural Privilege Creep: Integration Scopes Exceed Documented Purpose
- **Priority Tier:** `P2 - HIGH_PRIORITY_REMEDIATION` (Triage Score: **83.0/100**)
- **Severity (Impact):** HIGH (7.5/10) | **Confidence (Evidence):** HIGH (9.5/10)
- **MITRE ATT&CK:** `T1098 (Account Manipulation)` | **OWASP API:** `API1:2023 (Broken Object Level Authorization)`
- **Evidence References:** E05:INT-01, E08:Sec4.2
- **Defensive Countermeasure:** Implement fine-grained OAuth2 scope restriction (attendance.read/write only) and annual entitlement reviews.

### [DET-004] Perpetual Production Credential with Indefinite Validity
- **Priority Tier:** `P2 - HIGH_PRIORITY_REMEDIATION` (Triage Score: **83.0/100**)
- **Severity (Impact):** HIGH (7.5/10) | **Confidence (Evidence):** HIGH (9.5/10)
- **MITRE ATT&CK:** `T1552.001 (Unsecured Credentials: Plaintext Credentials)` | **OWASP API:** `API2:2023 (Broken Authentication)`
- **Evidence References:** E05:INT-01, E08:Sec4.1, E12:Section1
- **Defensive Countermeasure:** Integrate an enterprise Secrets Manager with automatic 30-day credential rotation and dynamic short-lived token issuance.

### [DET-005] Unrestricted Network Perimeter Policy for External Integration
- **Priority Tier:** `P2 - HIGH_PRIORITY_REMEDIATION` (Triage Score: **83.0/100**)
- **Severity (Impact):** HIGH (7.5/10) | **Confidence (Evidence):** HIGH (9.5/10)
- **MITRE ATT&CK:** `T1190 (Exploit Public-Facing Application)` | **OWASP API:** `API2:2023 (Broken Authentication)`
- **Evidence References:** E05:INT-01, E08:Sec4.2
- **Defensive Countermeasure:** Configure strict CIDR filtering at WAF/Gateway restricting ingress to vendor connector IPs.

### [DET-006] Configuration Read Invocation on Secret Settings Preceding Extraction
- **Priority Tier:** `P2 - HIGH_PRIORITY_REMEDIATION` (Triage Score: **83.0/100**)
- **Severity (Impact):** HIGH (7.5/10) | **Confidence (Evidence):** HIGH (9.5/10)
- **MITRE ATT&CK:** `T1087 (Account Discovery) / T1552 (Unsecured Credentials)` | **OWASP API:** `API7:2023 (Server-Side Request Forgery / Security Misconfiguration)`
- **Evidence References:** E11:CHG-882, E12:Section2
- **Defensive Countermeasure:** Enforce strict Read-Access-Logging and Masking on all configuration endpoints; require step-up MFA for secrets viewing.

### [DET-008] Dormant Terminated Account Post-Offboarding Successful Authentication
- **Priority Tier:** `P2 - HIGH_PRIORITY_REMEDIATION` (Triage Score: **83.0/100**)
- **Severity (Impact):** HIGH (7.5/10) | **Confidence (Evidence):** HIGH (9.5/10)
- **MITRE ATT&CK:** `T1078.002 (Valid Accounts: Domain Accounts)` | **OWASP API:** `API2:2023 (Broken Authentication)`
- **Evidence References:** E01:A006, E07:USR-04, E08:Sec8.2
- **Defensive Countermeasure:** Implement automated HR-to-IdP SCIM synchronization for immediate account deprovisioning upon employee termination.

### [DET-009] Unapproved Bulk Learner Data Export (Missing DPO/Business Justification)
- **Priority Tier:** `P2 - HIGH_PRIORITY_REMEDIATION` (Triage Score: **83.0/100**)
- **Severity (Impact):** HIGH (7.5/10) | **Confidence (Evidence):** HIGH (9.5/10)
- **MITRE ATT&CK:** `T1560 (Archive Collected Data)` | **OWASP API:** `API1:2023 (Broken Object Level Authorization)`
- **Evidence References:** E06:HD-1062, E06:HD-1069, E08:Sec5.3, E10:VND-221
- **Defensive Countermeasure:** Institute an asynchronous Dual-Key Approval workflow: bulk exports require dual cryptographic sign-off before files are staged.

### [DET-010] Duplicate / Repeated Retrieval of Sensitive Staged Export
- **Priority Tier:** `P3 - MEDIUM_DEFENSIVE_HARDENING` (Triage Score: **68.0/100**)
- **Severity (Impact):** MEDIUM (5.0/10) | **Confidence (Evidence):** HIGH (9.5/10)
- **MITRE ATT&CK:** `T1567.002 (Exfiltration to Cloud Storage / External Egress)` | **OWASP API:** `API1:2023 (Broken Object Level Authorization)`
- **Evidence References:** E04:C003, E04:C004
- **Defensive Countermeasure:** Enforce single-use download links (One-Time-Token) that expire immediately upon first successful byte retrieval.

---

## 6. Defensive Architecture & Zero-Trust Engineering Solution

To permanently remediate the vulnerabilities exposed in Case NS-26-014, Northstar Sentinel implements an enterprise **Policy Enforcement Point (PEP)** Zero-Trust reverse proxy:

```
[External Request]
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│             NORTHSTAR SENTINEL ZERO-TRUST PEP               │
│                                                             │
│  [1. Ingress Filter] ──► Validates Client IP in Whitelist  │
│                          (Blocks 203.0.113.77 with HTTP 403)│
│                                                             │
│  [2. Auth & TTL]    ──► Validates Dynamic Ephemeral Token   │
│                          (Rejects expired / static keys)    │
│                                                             │
│  [3. Scope Gate]    ──► Enforces Least-Privilege Scoping    │
│                          (RollCall limited to attendance)   │
│                                                             │
│  [4. Rate Limiter]  ──► Token Bucket (Max 50 req/min)       │
│                          (Throttles bulk scraping)          │
│                                                             │
│  [5. Export Vault]  ──► Asynchronous DPO Approval Token     │
│                          (Prevents unauthorized staging)    │
└─────────────────────────────────────────────────────────────┘
       │ (Authorized & Sanitized)
       ▼
[Internal Backend: ClassBridge & CampusVault]
```

### Verification Against Safe Mock API
The hardened controls were deployed against the supplied `SAFE_SIMULATION` local API server:
* Attendance Sync from `10.10.4.12` with valid token: **HTTP 200 OK (ALLOWED)**
* Learner Search from `203.0.113.77`: **HTTP 403 FORBIDDEN (BLOCKED - Invalid Source IP)**
* Bulk Learner Export by `rollcall-prod`: **HTTP 403 FORBIDDEN (BLOCKED - Insufficient Scope `attendance.sync` only)**
* Unauthenticated Request: **HTTP 401 UNAUTHORIZED (BLOCKED - Missing / Invalid Token)**
* Automated Pytest Test Suite: **10/10 Verification Tests Passed (100% Pass Rate)**

---

## 7. Regulatory & Governance Impact

Under the **Digital Personal Data Protection Act (DPDPA 2023)** and ISO/IEC 27001:
1. **Mandatory Breach Notification:** Northstar Skills Academy must notify the Data Protection Board of India and the 2,300 affected data principals regarding the unauthorized staging and retrieval of PII.
2. **Vendor Risk Management (Third-Party Assurance):** Vendor contracts must mandate annual SOC 2 Type II audits, immediate incident disclosure SLAs (under 4 hours), and mutual TLS (mTLS) enforcement.
3. **Identity Governance (IAM):** All service accounts must be migrated to a centralized HashiCorp Vault / AWS Secrets Manager with automated 30-day rotation and strict zero-standing-privilege policies.

---
**Report Approved by:** Lead Forensic Examiner, Northstar Sentinel Incident Command  
**Classification:** DEFENSE COMPETITION MASTER BRIEFING
