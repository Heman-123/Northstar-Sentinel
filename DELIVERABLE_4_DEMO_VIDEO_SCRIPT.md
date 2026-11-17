# CRIMEATHON ’26 — CASE FILE NS-26-014: DEFENSE TRACK
## DELIVERABLE 4: SIMULATION / DEMONSTRATION VIDEO SCRIPT
**Project Name:** Northstar Sentinel  
**Target Duration:** 4 minutes 30 seconds  
**Video Resolution:** 1080p 60fps  
**Host / Presenter:** Security Engineer & Incident Response Lead  

---

### TIMELINE & SCREENPLAY BREAKDOWN

#### [0:00 - 0:45] SECTION 1: Case Introduction & Threat Model
* **Visual on Screen:**
  * Browser showing Northstar Sentinel React Dashboard (`http://localhost:3000`).
  * Close-up on the Top Banner: `CASE NS-26-014 | CHENNAI LEARNING CENTER INCIDENT`.
  * Highlight the Metrics Bar: `2,300 Impacted Records`, `972.4 KB Egress`, `8,420 ms Latency Spike`.
* **Voiceover Narrative:**
  > "Hello judges and evaluators of CRIMEATHON ’26. This is the official demonstration of **Northstar Sentinel**, our evidence-driven API security monitoring and incident response platform developed for Case File NS-26-014.
  > On October 12, 2026, Northstar Skills Academy suffered an incident where an external actor abused a third-party service credential belonging to RollCall Connect from IP 203.0.113.77.
  > They exploited privilege creep and static credentials to scrape 2,300 student PII records, staged the dump into CampusVault, and downloaded it twice, spiking portal latency to 8.4 seconds.
  > Under the DEFENSE Track, we have built a complete, end-to-end platform that proves what happened with cryptographic precision, and introduces an active Zero-Trust Policy Enforcement Point that stops this attack cold."

---

#### [0:45 - 1:45] SECTION 2: Forensic Ingestion, Timeline & Epistemic Matrix
* **Visual on Screen:**
  * Switch to Terminal / VS Code: Run `python src/01_verify_ingest.py` showing SHA-256 calculation for all 12 evidence files (E01-E12).
  * Run `python src/02_normalize.py` and `python src/03_correlate.py`.
  * Return to React Web Dashboard: Click **"Incident Timeline"** tab.
  * Scroll smoothly through the timeline from `03:15:55 IST` (N001 network ingress) -> `03:16:35` (CHG-882 config read) -> `03:17:09` (R004 export) -> `03:21:03` (C003 CampusVault download).
  * Click **"Epistemic Truth Matrix"** tab. Highlight the 3 columns: Confirmed Facts vs Supported Inferences vs Unknowns.
* **Voiceover Narrative:**
  > "First, our evidentiary foundation. In the terminal, our ingestion engine computes SHA-256 digests across all 12 case evidence files, establishing an unbroken chain of custody.
  > In our web console, we visualize the chronological reconstruction in Indian Standard Time. Notice the smoking gun: at 03:16:35, the external IP reads the integration settings, and exactly five seconds later, launches the bulk search and export.
  > Crucially, our Epistemic Truth Matrix respects professional DFIR standards. We prove the machine identity was abused, but we deliberately refuse to falsely claim the human operator behind the keyboard, because true forensic integrity requires separating log-proven facts from unverified assumptions."

---

#### [1:45 - 3:00] SECTION 3: Live Attack vs. Defense Simulator (The Zero-Trust PEP)
* **Visual on Screen:**
  * Switch to **"Zero-Trust Simulator"** tab in the React Dashboard.
  * Mode set to: **`Vulnerable Baseline`**.
  * Select Scenario 1: **External IP Replay Attack (`203.0.113.77`)**.
  * Click **`Dispatch Simulated Packet`**.
  * Output: Red box showing `HTTP 200 — PERMITTED (VULNERABILITY EXPOSED)`.
  * Select Scenario 2: **Excessive Scope Abuse (`POST /v1/learners/export`)**.
  * Click **`Dispatch Simulated Packet`**.
  * Output: Red box showing `HTTP 200 — PERMITTED (MASS EXFILTRATION)`.
  * NOW toggle switch to: **`Sentinel Shield (Hardened)`**.
  * Run Scenario 1 again: Output turns bright green: `HTTP 403 FORBIDDEN — BLOCKED: UNAUTHORIZED_SOURCE_IP`.
  * Run Scenario 2 again: Output turns bright green: `HTTP 403 FORBIDDEN — BLOCKED: PRIVILEGE_CREEP_BLOCKED`.
  * Run Scenario 3 (Burst Scraping): Output shows: `HTTP 429 — BLOCKED: RATE_LIMIT_EXCEEDED`.
  * Run Scenario 4 (Legitimate Sync): Output shows: `HTTP 200 — PERMITTED (AUTHORIZED BY SENTINEL)`.
* **Voiceover Narrative:**
  > "Now let's demonstrate the core defensive innovation: our Zero-Trust Policy Enforcement Point.
  > In Vulnerable Baseline mode, observe what happens when an attacker replays the RollCall token from external IP 203.0.113.77: the server responds with HTTP 200, exposing student data. When they request a bulk export, the server obliges, despite RollCall being an attendance integration!
  > Now, we switch on the **Sentinel Shield**.
  > Watch the immediate difference:
  > When the attacker attempts the same request from the external IP, our Perimeter Filter instantly drops the connection with HTTP 403: Unauthorized Source IP.
  > When a request attempts to touch the learner export endpoint, our Scope Gate rejects it with HTTP 403: Privilege Creep Blocked.
  > When an automated script attempts burst scraping, our Token Bucket limiter clamps the traffic with HTTP 429.
  > And most importantly, legitimate daily attendance synchronization from internal IP 10.10.4.12 continues completely uninterrupted."

---

#### [3:00 - 4:00] SECTION 4: Automated Verification Test Harness & Pytest
* **Visual on Screen:**
  * Switch to Terminal.
  * Run: `python simulation/test_hardened_api.py`.
  * Show all 10 automated test cases executing and passing with `OK`.
  * Run: `python tests/test_pipeline.py`.
  * Show end-to-end pipeline test suite passing with `OK`.
* **Voiceover Narrative:**
  > "To prove that our defense is not just a UI simulation, we run our automated Python test harness against the hardened simulation server.
  > Ten out of ten rigorous security unit tests pass with 100% success.
  > Tests verify source IP validation, granular scope checking, rate limit triggers at the 11th request, and our dual-key cryptographic DPO approval requirement for bulk PII downloads."

---

#### [4:00 - 4:30] SECTION 5: Summary, Repository Access & Conclusion
* **Visual on Screen:**
  * Show GitHub repository page: `https://github.com/Heman-123/Northstar-Sentinel.git`.
  * Scroll through the comprehensive README with architecture diagrams and setup instructions.
* **Voiceover Narrative:**
  > "All source code, evidence processors, tests, and the React frontend are published on our public GitHub repository at github.com/Heman-123/Northstar-Sentinel.
  > Northstar Sentinel turns forensic evidence into actionable, automated Zero-Trust defense, fully neutralizing the attack vectors of Case NS-26-014.
  > Thank you for your time, and we look forward to your questions."

---
*End of Video Script*
