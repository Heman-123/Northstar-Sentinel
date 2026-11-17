# CRIMEATHON ’26 — CASE FILE NS-26-014: THE NORTHSTAR LEARNING SERVICES INVESTIGATION
## OFFICIAL PARTICIPANT DELIVERABLE 1: ONE-PAGE PROBLEM STATEMENT
**TRACK SELECTION:** **`DEFENSE TRACK`**  
**PROJECT IDENTIFIER:** **NORTHSTAR SENTINEL** (Evidence-Driven API Security & Incident Response Platform)  
**SUBMISSION TEAM REPO:** `https://github.com/Heman-123/Northstar-Sentinel.git`  

---

### 1. Cybersecurity Problem Definition
The incident at Northstar Skills Academy Pvt. Ltd. stems from an **Architectural Least-Privilege Scope Failure combined with Credential Lifecycle Deficiencies in Third-Party SaaS Integrations**. Specifically:
1. **Excessive Scope / Privilege Creep:** Machine identity `svc_rollcall` (`rollcall-prod`), registered strictly for *Attendance Synchronization*, was over-provisioned with global search and mass export scopes (`learner.search`, `learner.export`).
2. **Credential Hygiene Failure:** The production integration credential (`rc-prod-01`) possessed **no expiration date** (`Expiry: Never`) and lacked network ingress boundaries (`IP Restriction: None`), directly violating Information Security Policy Section 4.1 & 4.2.
3. **Data Loss Prevention & Rate-Limiting Absence:** Core portal `ClassBridge` and cloud storage `CampusVault` lacked unthrottled query safeguards, egress DLP controls, and dual-authorization mechanisms, allowing an unauthorized external actor to query, stage, and download 100% of institution learner PII without human intervention.

### 2. Evidentiary Citations (Evidence & Event Cross-Correlation)
* **Ingress from Unrecognized External IP:** `E09:N001` (TCP ingress from `203.0.113.77` at 03:15:55 IST) followed by machine authentications `E01:A011`, `A012`, `A013` (03:16:32–03:19:48 IST).
* **Configuration Reconnaissance:** `E11:CHG-882` records actor `svc_rollcall` executing `credential_config_read` on `integration_settings/rollcall` from `203.0.113.77` at 03:16:35 IST, 5 seconds prior to API abuse.
* **Unthrottled Scraping & Mass Export:** `E03:R003` / `E02:P003` (`GET /v1/learners/search`, 2,300 records, 3,250ms latency) and `E03:R004` / `E02:P004` (`POST /v1/learners/export`, 2,300 records, 8,420ms latency).
* **Cloud Staging & Exfiltration:** `E11:CHG-883` dispatched export job; `E04:C001` wrote 486,200 bytes to `campusvault-exports/learner-exports/learners-20261012.csv`. Actor executed bucket listing (`E04:C002`) and two separate downloads totaling 972,400 bytes (`E04:C003` at 03:21:03 and `E04:C004` at 03:24:48 IST).
* **Unauthorized Business Operations:** `E06:HD-1062` & `HD-1069` confirm neither maintenance nor Finance authorized the export. `E10:VND-221` confirms vendor initiated no export and operates strictly from `10.10.4.12`.

### 3. Technical and Business Impact
* **Technical Impact:** Server resource starvation (portal latency spiked by ~187x from 45ms to 8,420ms), rate-limit contention causing attendance sync delays, database table-scan exhaustion, and unauthorized staging/egress of 972.4 KB.
* **Business Impact:** Compromise of 2,300 active student records (PII). Triggers mandatory regulatory breach notification under the **Digital Personal Data Protection Act (DPDPA 2023)** with potential statutory penalties, institutional reputational damage, and vendor breach of contract.

### 4. Epistemic Separation: Facts vs. Assumptions vs. Unknowns
| Tier 1: Confirmed Facts (Log-Proven) | Tier 2: Strongly Supported Inferences | Tier 3: Confirmed Unknowns (Unattributed) |
| :--- | :--- | :--- |
| • Key `rc-prod-01` has no expiry & no IP filter (`E05:INT-01`).<br>• IP `203.0.113.77` invoked config read & APIs (`E01`, `E03`, `E11`).<br>• 2,300 records exported & downloaded twice (`E04`).<br>• Former employee `former.ajay` logged in on Oct 9 (`E01:A006`). | • Token exposed via ticket screenshot (`E06:HD-1058`) or config read (`E11:CHG-882`).<br>• Latency surge caused by unindexed 2,300 record dump.<br>• Attendance sync delay caused by backend thread contention. | • Physical identity / location of human operator behind `203.0.113.77`.<br>• Whether two downloads represent two unique copies or an interrupted TCP stream.<br>• Whether data was distributed onward or destroyed.<br>• No connection proven between `former.ajay` and RollCall. |

### 5. Proposed Scope and Intended Outcome
* **Scope:** 100% offline, local defensive architecture (`127.0.0.1:8765`). Zero external network calls.
* **Intended Outcome:** Deploy **Northstar Sentinel Zero-Trust Policy Enforcement Point (PEP)** featuring:
  1. *Perimeter Ingress Whitelisting:* Blocks unauthorized source CIDRs (rejects `203.0.113.77` with HTTP 403).
  2. *Granular Least-Privilege Scoping:* Restricts RollCall strictly to `attendance:sync` (rejects search/export with HTTP 403).
  3. *Rate-Limiting Throttler:* Clamps requests to max 10/min, eliminating database exhaustion and scraping.
  4. *Two-Man Export Gate:* Demands cryptographic DPO token before staging PII dumps into CampusVault.
  5. *Full Observability:* Automated 6-stage DFIR pipeline with 10 deterministic detection rules (DET-001 to DET-010) and an interactive React + Tailwind CSS SOC Dashboard.
