# 🎬 NORTHSTAR SENTINEL — MASTER DEMO VIDEO PRODUCTION SCRIPT
## CRIMEATHON '26 · Defense Track · Case File: NS-26-014
### Target Duration: 4 Minutes 45 Seconds | Format: 1080p 60fps / 30fps | Pacing: ~135 WPM

---

## 📋 PRE-RECORDING CHECKLIST & STAGING

Before pressing record, prepare your environment exactly as follows:

| Item | Setup Action |
|---|---|
| **Recording Software** | OBS Studio (recommended) or Windows Game Bar (`Win + G`). Resolution: **1920×1080**, Framerate: **30fps or 60fps**, Audio Bitrate: **320 kbps**. |
| **Audio Setup** | Use a dedicated USB microphone or headset mic. Avoid laptop built-in mics. Position mic 3–4 inches from mouth with pop filter or slight off-axis angle. |
| **Browser Staging** | Open Chrome or Edge at **100% zoom** (`Ctrl + 0`). Open two tabs: <br>• **Tab 1:** `dashboard.html` (Local file: `file:///C:/Users/DELL/.gemini/antigravity/scratch/Northstar-Sentinel/dashboard.html`)<br>• **Tab 2:** `CRIMEATHON_26_PRESENTATION_DECK.pptx` or `reports/PRESENTATION_SLIDES.html` |
| **Terminal Staging** | Open Windows Terminal or Command Prompt at `C:\Users\DELL\.gemini\antigravity\scratch\Northstar-Sentinel`. Run tests beforehand so you can display the clean output cleanly. |
| **Notifications** | Turn ON Windows **Focus Assist / Do Not Disturb**. Close Discord, Slack, WhatsApp, and browser notification popups. |
| **Rehearsal** | Read through the script twice aloud to lock in pronunciation of technical terms: *OCSF*, *CIDR*, *DPDPA 2023*, *CERT-In*, *Epistemic*. |

---

## ⏱️ VIDEO TIMELINE AT A GLANCE

```
[0:00 - 0:25] ── ACT 1: The Hook & Case Classification              (25 sec)
[0:25 - 1:05] ── ACT 2: The Breach & Root Cause Deconstruction      (40 sec)
[1:05 - 1:45] ── ACT 3: Forensic Chain & Epistemic Rigor            (40 sec)
[1:45 - 2:30] ── ACT 4: The 4-Layer Zero-Trust Architecture         (45 sec)
[2:30 - 3:35] ── ACT 5: THE LIVE ATTACK & ZERO-TRUST DEMO          (65 sec) ★ CLIMAX
[3:35 - 4:10] ── ACT 6: Empirical Verification & Evidence Vault     (35 sec)
[4:10 - 4:40] ── ACT 7: Statutory Governance & DPDPA Compliance     (30 sec)
[4:40 - 5:00] ── ACT 8: Conclusion & Hackathon Winning Close       (20 sec)
                                                     TOTAL RUNTIME: 4 min 40 sec
```

---

## 🎙️ SECOND-BY-SECOND SCRIPT & SCREENPLAY

---

### [0:00 – 0:25] ACT 1: THE HOOK & CASE CLASSIFICATION (25s)

**SCREEN:** 
Start on `dashboard.html`. Full screen (`F11`). The camera slowly zooms in or focuses on the top enterprise command bar: the glowing **DEFCON 2 : ELEVATED RISK** badge, the pulsating **PEP PROXY: ONLINE** status, and the case classification: `ES-00024 [NS-26-014] • CRIMEATHON '26 DEFENSE TRACK`.

**ACTION:**
Hover the mouse cursor over the header metrics: `2,300 Learners Impacted`, `972.4 KB Egress Volume`, `8,420 ms Latency Spike`.

**NARRATOR (Firm, urgent, highly authoritative):**
> "At 3:15 AM on October 12th, 2026, an external threat actor bypassed the perimeter of Northstar Skills Academy in Chennai. 
> Within nine minutes, 2,300 active student records were exfiltrated, core database latencies surged by one-hundred and eighty-seven times, and the institution faced a potential statutory penalty of up to 250 Crores under India's DPDPA 2023.
> 
> Welcome to **Northstar Sentinel** — our competition-grade Zero-Trust Digital Forensics and Automated Incident Response platform built for CRIMEATHON '26 Defense Track."

---

### [0:25 – 1:05] ACT 2: THE BREACH & ROOT CAUSE DECONSTRUCTION (40s)

**SCREEN:**
Switch to presentation Slide 2 (or click on the **Attack Surface Topology** tab in `dashboard.html`). Show the node network mapping external IP `203.0.113.77` attacking `svc_rollcall`.

**ACTION:**
Smoothly gesture cursor across the three root cause cards: Privilege Creep, Credential Hygiene, and Resource Consumption.

**NARRATOR (Analytical, diagnostic tone):**
> "To defeat an adversary, we must first dissect the failure. 
> The legitimate vendor, RollCall, operates strictly within internal subnet `10.10.4.0/24`. Yet, adversary IP `203.0.113.77` authenticated machine token `rc-prod-01` without resistance.
> 
> Why did this succeed? Our forensic audit identified three critical OWASP API Top 10 vulnerabilities:
> First — **Architectural Privilege Creep**: An attendance integration was granted wildcard `learner.export` permissions.
> Second — **Broken Credential Hygiene**: The service token was configured with `Expiry: Never` and zero CIDR restrictions, having leaked via an unredacted support ticket.
> And Third — **Unrestricted Resource Consumption**: The API had zero rate-limiting, allowing a full unindexed table scan that crippled the portal."

---

### [1:05 – 1:45] ACT 3: FORENSIC EVIDENCE CHAIN & EPISTEMIC RIGOR (40s)

**SCREEN:**
Switch back to `dashboard.html`. Click **Splunk ES Workbench** tab and expand the **Forensic Evidence Timeline**, then switch to the **Epistemic Truth Matrix** tab.

**ACTION:**
Hover over the colored badges: Green for `CERTAIN`, Cyan for `PROBABLE`, Amber for `UNDETERMINED`.

**NARRATOR (Precise, scientific confidence):**
> "Real digital forensics demands absolute integrity. 
> Sentinel ingested twelve heterogeneous evidence artifacts — from authentication logs to S3 cloud trails — all bit-level verified with SHA-256 cryptographic hashes.
> 
> Here is our nine-event chronological timeline: from the initial TCP ingress at 03:15:55, through the unauthorized database read CHG-882, the bulk export surge, to the two staging downloads in CampusVault totaling 972.4 kilobytes.
> 
> Crucially, we enforce the **ISO/IEC 27037 Epistemic Truth Matrix**. 
> While we prove with 100% mathematical certainty that IP `203.0.113.77` executed the exfiltration, we refuse to guess the human operator's identity without an ISP court subpoena. We also forensically prove that former employee Ajay's offboarding issue is completely unlinked to this breach. Zero speculation. Zero hallucination."

---

### [1:45 – 2:30] ACT 4: THE 4-LAYER ZERO-TRUST ARCHITECTURE (45s)

**SCREEN:**
Switch to presentation Slide 5 (or show the architecture diagram). Then switch to `dashboard.html` and click on the **Zero-Trust PEP Lab** tab.

**ACTION:**
Point to each of the four distinct defensive layers as they are named.

**NARRATOR (Enthusiastic, solution-oriented):**
> "Knowing the attack path, how do we guarantee this can never happen again?
> We engineered the **Northstar Sentinel Zero-Trust Policy Enforcement Point** — an in-line reverse proxy operating across four defensive layers:
> 
> **Layer 1: CIDR Subnet Pinning.** Integration machine accounts are strictly pinned to vendor CIDR `10.10.4.0/24`. Any packet from an external IP is dropped at the edge in zero milliseconds.
> 
> **Layer 2: Least-Privilege Scope Gating.** Tokens are clamped strictly to `attendance:*`. Any attempt to call `learner.export` is rejected with HTTP 403.
> 
> **Layer 3: Adaptive Token-Bucket Rate Limiter.** Capped at 100 requests per minute with automated burst suppression, preventing table scraping and denial of service.
> 
> **Layer 4: DPO Two-Man Rule.** Any query attempting to access bulk learner PII requires dual cryptographic sign-off from the Data Protection Officer."

---

### [2:30 – 3:35] ACT 5: THE LIVE ATTACK & ZERO-TRUST DEMONSTRATION (65s) ★ CLIMAX

**SCREEN:**
Stay on `dashboard.html` in the **Zero-Trust PEP Lab** tab. This is the live interactive core of the demo.

**ACTION 1:**
Point to the **Simulation Mode** toggle. Ensure it is set to **Hardened (Zero-Trust PEP Active)** in glowing green.
Point to the input fields:
• Endpoint: `POST /v1/learners/export`
• Ingress IP: `203.0.113.77` (the attacker IP)

**NARRATOR:**
> "Now, let us watch Northstar Sentinel defend in real time.
> Here is our interactive Zero-Trust PEP Lab. We load the exact adversarial payload: external IP `203.0.113.77` calling `POST /v1/learners/export`."

**ACTION 2:**
Click the **"Transmit Crafted Packet"** button.
Immediately show the verdict box turning green:
`HTTP 403 FORBIDDEN — BLOCKED BY PERIMETER_IP_FILTER`
`External IP 203.0.113.77 rejected at Layer 1. Client rollcall-prod is pinned strictly to subnet 10.10.4.0/24.`

**NARRATOR:**
> "We transmit... and it is instantly BLOCKED. HTTP 403 Forbidden. 
> Layer 1 Subnet Pinning drops the connection immediately. No database queries, zero data leakage."

**ACTION 3:**
Now click the **"Vulnerable Baseline"** toggle button (turns Red).
Click **"Transmit Crafted Packet"** again.
Show the verdict box turning red:
`HTTP 200 OK — VULNERABILITY EXPOSED (DATA LEAKED)`

**NARRATOR:**
> "Now, let's revert to the vulnerable baseline that Northstar had on October 12th.
> We send the exact same packet... and it succeeds with HTTP 200 OK. 2,300 records exposed.
> Switch back to Hardened mode — transmit again — instantly blocked."

**ACTION 4:**
Now click the red **"Fire Live Attack"** button in the top navigation bar.
Watch the Live Radar banner update, then click **"SOAR Actions"** button.
In the SOAR modal, click **"Shun Attacker IP (203.0.113.77)"**.
Show the smooth slide-in **Toast Notification** at the top right:
`SOAR PLAYBOOK EXECUTED: IP 203.0.113.77 shunned across perimeter firewall. Rule activated in 0ms.`
Show the note automatically added to the investigation thread.

**NARRATOR:**
> "We can also trigger automated SOAR containment. With one click, our SOAR playbook shuns IP `203.0.113.77` across perimeter firewalls in zero milliseconds, revokes token `rc-prod-01` across the IdP cluster, and logs the action into the forensic notes thread."

---

### [3:35 – 4:10] ACT 6: EMPIRICAL VERIFICATION & EVIDENCE VAULT (35s)

**SCREEN:**
Quickly switch to your open Terminal showing the test outputs, then back to `dashboard.html` on the **Detection Rules (10)** and **Evidence Vault** tabs.

**ACTION:**
Scroll through the terminal showing:
`15 passed in 0.42s` (pytest)
`SIMULATION COMPLETE: 10 / 10 TESTS PASSED (100% Pass Rate)`

**NARRATOR (Confident, engineering-focused):**
> "We don't just demonstrate concepts; we write production-tested code.
> Our test suite covers **15 out of 15 automated unit tests** in Pytest, validating timestamp alignment, OCSF normalization, and hash verification with 100% pass rates.
> 
> Furthermore, our mock attack simulation harness executed **10 out of 10 attack vectors** — testing privilege escalation, rate exhaustion, and token replay — all blocked by our PEP proxy.
> Every single piece of evidence is tracked here in our Evidence Vault with verifiable SHA-256 digests."

---

### [4:10 – 4:40] ACT 7: STATUTORY GOVERNANCE & DPDPA COMPLIANCE (30s)

**SCREEN:**
Switch to `dashboard.html` and click on the **DPDPA 2023 Audit** tab (or presentation Slide 9).

**ACTION:**
Highlight Section 8(5) penalty callout and the CERT-In 6-Hour SLA timer.

**NARRATOR (Executive, regulatory depth):**
> "A technical defense is incomplete without legal certainty. 
> Under Section 8(5) of India's Digital Personal Data Protection Act 2023, data fiduciaries face statutory penalties of up to 250 Crores for failure to protect personal data.
> 
> Northstar Sentinel automatically compiles the formal incident disclosure package, satisfying India's **CERT-In 6-Hour mandatory reporting requirement** with an immutable chain of custody. By deploying our PEP proxy, the blast radius is immediately reset to zero."

---

### [4:40 – 5:00] ACT 8: CONCLUSION & HACKATHON WINNING CLOSE (20s)

**SCREEN:**
Switch to presentation Slide 10 (or show your live GitHub repository page: `github.com/Heman-123/Northstar-Sentinel`).
Display the trophy banner: **🏆 CRIMEATHON '26 FINALIST — DEFENSE TRACK**.

**NARRATOR (Inspiring, impactful, decisive):**
> "Every line of code — the 6-stage DFIR engine, the Zero-Trust reverse proxy, the automated test harness, and this analyst workbench — is open-source, fully documented, and live on GitHub right now.
> 
> Northstar Sentinel: **Zero Trust. Zero Hallucination. Zero Breach.**
> Thank you, CRIMEATHON '26 judges. We are ready for your questions."

---

## 💡 PRESENTER PRO-TIPS FOR WINNING

1. **Energy Curve:** Start strong and confident, speak steadily during the technical breakdown (Acts 2–4), peak with high energy during the Live Attack Demo (Act 5), and close with decisive authority (Act 8).
2. **Mouse Movements:** Keep cursor movements smooth and deliberate. Do NOT frantically wiggle the mouse. Point directly to the elements you are discussing.
3. **Audio Quality:** Do a 15-second mic check first. Listen with headphones to ensure there is zero background hum or air conditioner noise.
4. **One-Take Strategy:** If you make a minor stumble in speech, pause for 2 seconds, take a breath, and re-read the sentence. You can easily cut out the 2-second pause in free video editors like CapCut, Clipchamp, or Premiere.
5. **Video Description & Link:** Once uploaded to YouTube (Unlisted) or Google Drive, paste the video link at the very top of your GitHub `README.md` and submission portal.
