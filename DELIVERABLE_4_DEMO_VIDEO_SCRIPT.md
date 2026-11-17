# NORTHSTAR SENTINEL — DEMO VIDEO SCRIPT
## CRIMEATHON '26 · Defense Track · Case NS-26-014
### Duration: 4:30 minutes | Resolution: 1920×1080 | 30fps

> **Team:** Team Northstar · Northstar Skills Academy, Chennai
> **GitHub:** https://github.com/Heman-123/Northstar-Sentinel
> **Case Reference:** NS-26-014 | Incident Date: 12 October 2026, 03:15–03:24 IST

---

## PRE-RECORDING CHECKLIST

- [ ] Browser at **100% zoom** (Ctrl+0 to reset)
- [ ] Dashboard open at `dashboard.html` (local file, all tabs pre-loaded)
- [ ] Python mock server running: `python simulation/mock_api_server.py`
- [ ] OBS Studio **OR** Windows Game Bar (Win + G) recording at **1920×1080 / 30fps**
- [ ] **Headset microphone** plugged in (not built-in laptop mic)
- [ ] Close all notifications — **Windows Focus Assist ON** (Do Not Disturb)
- [ ] Terminal open and visible at project root directory
- [ ] GitHub repo open in second browser tab: https://github.com/Heman-123/Northstar-Sentinel
- [ ] `PRESENTATION_SLIDES.html` open in third tab, starting at Slide 1
- [ ] Silence phone and disable desktop popups (Teams, Outlook, etc.)
- [ ] **Practice narration 2× before recording**

---

## TIMESTAMPS & NARRATION

---

### [0:00–0:15] INTRO — Title Slide

**SCREEN:** `PRESENTATION_SLIDES.html` — **Slide 1 (Title Slide)**
*(Full screen. No browser chrome visible. Title animation should be complete before narration begins.)*

**PRODUCTION NOTE:** Fade in from black over 1 second. Title text should be fully rendered before voice starts.

**NARRATOR:** *(confident, measured pace — approximately 130 WPM)*

> "Welcome. We are **Team Northstar** from CRIMEATHON '26 — Defense Track.
> Our submission, **Northstar Sentinel**, is a complete Zero-Trust Digital Forensics
> and Incident Response solution — built to investigate and prevent the
> **RollCall API data breach** at Northstar Skills Academy,
> Chennai, on October 12th, 2026."

---

### [0:15–0:45] THE BREACH — Problem Statement

**SCREEN:** Switch to **Slide 2 (Problem / Attack Overview)**
*(Slide should show: external IP, token details, data exfiltration summary, OWASP tags)*

**PRODUCTION NOTE:** Keep slide visible for the full 30 seconds. Advance bullet points to match narration cadence — do not reveal all points at once.

**NARRATOR:** *(slightly slower — let the facts land)*

> "At **03:15 IST on October 12th, 2026**, an external IP address —
> **203.0.113.77** — authenticated against the academy's RollCall attendance API
> using a privileged service token called **rc-prod-01**.
>
> The token had **no expiry date, no IP restriction, and no rate limit** —
> and critically, it carried elevated scopes far beyond what the legitimate vendor
> required. The legitimate vendor's IP range was **10.10.4.0/24** —
> this attacker was operating from outside that subnet entirely.
>
> In under **nine minutes**, **2,300 student attendance records**
> — **972.4 kilobytes** of personal data — were exported and downloaded **twice**,
> leaving two clean exfiltration artifacts in the logs.
>
> The root cause: three compounding OWASP API Security failures —
> **API1 privilege creep, API2 missing token constraints,
> and API4 absence of rate limiting.**"

---

### [0:45–1:30] EVIDENCE TIMELINE — Forensic Chain of Custody

**SCREEN:**
1. Begin on **Slide 3 (Evidence Timeline / Attack Sequence)** — hold for ~15 seconds
2. Switch to `dashboard.html` → click **"Splunk ES Workbench"** tab → scroll to **Timeline accordion** and expand it

**PRODUCTION NOTE:** When switching to dashboard, ensure the Timeline accordion is pre-collapsed so the click-to-expand is visible. Mouse movement should be slow and deliberate.

**NARRATOR:** *(authoritative, methodical — treat each event like court testimony)*

> "Our forensic reconstruction identifies **nine discrete events**
> across the nine-minute window, each anchored to log timestamps
> and cross-verified against API gateway records.
>
> At **03:15:55** — external ingress. At **03:16:02** — the token authenticates.
> **03:16:14** — a configuration read pulls API endpoint metadata.
> **03:17:30** — a search query targets the full attendance dataset.
> **03:18:45** — bulk export is triggered. By **03:20:11** — staging is complete.
> Then, at **03:21:38** and **03:23:55** — two separate download events,
> completing the exfiltration.
>
> *(expand Timeline accordion on screen while speaking)*
>
> Every event in this chain is backed by a corresponding forensic exhibit.
> We have catalogued **twelve evidence files, E01 through E12** —
> each with a **SHA-256 hash** to establish and maintain chain of custody.
> Every hash is independently verifiable from our GitHub repository.
> This is not a reconstruction — this is a forensic record."

---

### [1:30–2:00] EPISTEMIC RIGOR — Truth Matrix

**SCREEN:**
1. Switch to **Slide 4 (Epistemic Truth Matrix overview)**  — hold for ~10 seconds
2. Switch to `dashboard.html` → click **"Epistemic Truth Matrix"** tab

**PRODUCTION NOTE:** Zoom in slowly on the Truth Matrix table in the dashboard so judges can clearly read the CERTAIN / PROBABLE / UNDETERMINED tags.

**NARRATOR:** *(deliberate, calm — this is a differentiator, emphasize it)*

> "One of the most important things a forensic analyst can do
> is **know what they don't know**.
>
> Our Epistemic Truth Matrix classifies every finding into three tiers:
> **CERTAIN** — directly evidenced in logs.
> **PROBABLE** — strongly inferred but not directly observed.
> **UNDETERMINED** — where the data does not support a conclusion.
>
> *(point to UNDETERMINED row on screen)*
>
> For example: the **human identity** behind IP 203.0.113.77 is marked
> **UNDETERMINED**. We know the machine. We know the token.
> We do not know the person — and we will **not claim to**.
>
> This is what separates rigorous digital forensics from speculation —
> and it is what makes our findings **legally defensible**."

---

### [2:00–2:45] SOLUTION — Zero-Trust PEP Architecture

**SCREEN:**
1. **Slide 5 (Architecture Diagram)** — hold for ~15 seconds
2. **Slide 6 (4-Layer PEP Pipeline)** — hold for ~15 seconds
3. Switch to `dashboard.html` → click **"Zero-Trust PEP Lab"** tab

**PRODUCTION NOTE:** On Slide 5, use a laser pointer or mouse highlight to trace data flow through the architecture. On Slide 6, pace through each layer with the narration. Dashboard tab switch should be seamless.

**NARRATOR:** *(energetic but precise — this is the solution payoff)*

> "Our solution is a **four-layer Zero-Trust Policy Enforcement Point**
> that sits in front of every sensitive API endpoint.
>
> **Layer 1 — CIDR Pinning:** Any request originating outside the vendor's
> authorized subnet — 10.10.4.0/24 — is immediately rejected. Full stop.
>
> **Layer 2 — JWT Scope Gate:** The token is validated against its declared
> scope. rc-prod-01 had no business accessing bulk export endpoints —
> the gate enforces that boundary.
>
> **Layer 3 — Rate Limiter:** Bulk queries above a defined threshold per
> session window are throttled and alerted. No silent data drains.
>
> **Layer 4 — DPO Two-Man Rule:** Any export of personal data above a
> configurable record threshold requires a secondary authorization signal
> from the Data Protection Officer. One key cannot open the vault alone.
>
> *(switch to PEP Lab tab)*
>
> The PEP Lab here lets you test each layer independently or as an
> integrated pipeline — in both Hardened and Vulnerable configurations."

---

### [2:45–3:30] LIVE ATTACK DEMO — Zero-Trust PEP in Action

**SCREEN:** `dashboard.html` — **Zero-Trust PEP Lab tab** (full screen, browser maximized)

**PRODUCTION NOTE:** This is the most critical segment. Practice this sequence at least 5 times before recording. Mouse movements should be slow and confident. Pause narration briefly after each click to let the UI respond visibly.

**ACTIONS (perform each step on screen exactly as described):**

1. Click **"Fire Live Attack"** button in the dashboard header
   → Watch the **Live Radar** tab flash an alert indicator
2. Navigate back to PEP Lab tab → Set attacker IP field to **`203.0.113.77`**
3. Click **"Transmit Crafted Packet"**
   → Dashboard displays: **HTTP 403 — BLOCKED** (red banner)
4. Toggle mode selector to **"Vulnerable"**
   → Click "Transmit Crafted Packet" again
   → Dashboard displays: **HTTP 200 — OK** (green — data exposed)
5. Toggle mode back to **"Hardened"**
   → Click "Transmit Crafted Packet" one final time
   → Dashboard displays: **HTTP 403 — BLOCKED** (red — protected)

**NARRATOR:** *(confident, unhurried — let the demo breathe)*

> "Watch our Zero-Trust PEP in action.
>
> We've set the attacker's IP — **203.0.113.77** — and transmitted a
> crafted packet that mirrors the exact request profile from October 12th.
>
> *(click Transmit — pause 1 second)*
>
> **Blocked. HTTP 403.** Layer 1 CIDR filter triggers immediately —
> the IP is not in the authorized 10.10.4.0/24 range, and the
> connection is refused before the token is even evaluated.
>
> Now, let's switch to the **Vulnerable baseline** — the state the
> academy's API was in on the night of the breach.
>
> *(toggle to Vulnerable — click Transmit — pause 1 second)*
>
> **HTTP 200. The same request succeeds.** Data is accessible.
> No block, no alert, no audit trail — exactly what the attacker exploited.
>
> Back to Hardened —
>
> *(toggle to Hardened — click Transmit — pause 1 second)*
>
> **HTTP 403. Blocked again.** This is exactly what failed on October 12th —
> and exactly what Northstar Sentinel ensures will never happen again."

---

### [3:30–4:00] TEST RESULTS, DETECTION RULES & EVIDENCE VAULT

**SCREEN:**
1. `dashboard.html` → **"Detection Rules"** tab — scroll slowly so all 10 rules are visible
2. Switch to **"Evidence Vault"** tab — scroll to show all 12 entries with SHA-256 hashes

**PRODUCTION NOTE:** Zoom in gently (Ctrl+"+") on the Detection Rules table so MITRE ATT&CK IDs are legible — especially T1078.004, T1552.001, T1530, T1567. Reset zoom before switching tabs.

**NARRATOR:** *(factual, measured — deliver the numbers crisply)*

> "Our defensive framework includes **ten custom detection rules**,
> each mapped directly to a MITRE ATT&CK technique relevant to this incident —
> covering credential abuse under T1078.004, credential exposure T1552.001,
> cloud data staging T1530, and exfiltration via web services T1567.
>
> *(switch to Evidence Vault tab)*
>
> Against this framework, we ran **15 unit tests** covering individual
> PEP layer logic, and **10 end-to-end simulation tests** replicating
> the full October 12th attack sequence.
>
> **All 25 tests pass. 100% pass rate.**
>
> And here — the **Evidence Vault** — 12 forensic exhibits, E01 through E12,
> every one SHA-256 verified. The chain of custody is complete,
> intact, and independently auditable."

---

### [4:00–4:20] COMPLIANCE — DPDPA 2023 Mapping

**SCREEN:** `dashboard.html` → **"DPDPA 2023 Audit"** tab
*(Scroll slowly through the compliance mapping table so judges can read the section references)*

**PRODUCTION NOTE:** Keep pace slow here — judges who care about compliance will want to read the table. If the table has expandable rows, click to expand the §8(5) entry.

**NARRATOR:** *(serious, precise — compliance carries penalty weight)*

> "Every finding in this investigation maps directly to India's
> **Digital Personal Data Protection Act, 2023**.
>
> The specific provision at the center of this breach:
> **Section 8(5)** — the obligation on data fiduciaries to implement
> appropriate technical and organizational safeguards for personal data.
>
> The academy's failure to enforce token constraints, IP restrictions,
> and access controls is a textbook §8(5) violation —
> with **penalty exposure up to ₹250 Crores** under the Act.
>
> Additionally, under **CERT-In guidelines**, a breach of this nature
> triggers a **mandatory 6-hour reporting obligation**.
>
> Our Zero-Trust PEP is not just a technical solution —
> it is a **statutory compliance control**, demonstrably mapped
> to India's operative data protection law."

---

### [4:20–4:30] CONCLUSION — GitHub & Closing Statement

**SCREEN:**
1. Switch to GitHub tab: **https://github.com/Heman-123/Northstar-Sentinel**
   *(scroll slowly past README to show project structure)*
2. Switch to **Slide 10 (Conclusion / Closing Slide)**

**PRODUCTION NOTE:** End on the closing slide — not on the browser. Fade to black over 1–2 seconds after the final line. Do not cut abruptly.

**NARRATOR:** *(strong, unhurried close — project confidence)*

> "Everything you've seen today is live on GitHub —
> all **six DFIR pipeline stages**, the **15 unit tests**,
> the **Zero-Trust PEP gateway**, the **simulation server**,
> and this full **interactive dashboard**.
>
> Northstar Sentinel is a production-grade forensic and prevention framework —
> built in a hackathon window, grounded in real statutory obligations,
> and proven against a real attack pattern.
>
> **Zero Trust. Zero Hallucination. Zero Breach.**
>
> Thank you, CRIMEATHON '26 judges."

*(Fade to black)*

---

## PRODUCTION TIPS

### Recording Setup

| Setting | Value |
|---|---|
| Resolution | 1920 × 1080 (Full HD) |
| Frame Rate | 30fps |
| Output Format | MP4 (H.264) |
| Audio | Headset mic, 48 kHz, mono |
| Bitrate | ≥ 8 Mbps video, ≥ 128 kbps audio |

### OBS Studio Configuration
1. **Sources:** Add `Display Capture` → select your primary monitor
2. **Output:** Settings → Output → Recording → MP4, CRF 18 (high quality)
3. **Audio:** Settings → Audio → Sample Rate 48 kHz → select headset mic
4. **Hotkeys:** Set Start/Stop Recording hotkeys so you don't reach for the mouse mid-demo
5. **Preview:** Always preview your capture before recording — check for cursor lag

### Windows Game Bar (Fallback)
- Press **Win + G** to open Game Bar overlay
- Click the record button or press **Win + Alt + R** to start/stop
- Files saved to `%USERPROFILE%\Videos\Captures\`
- **Note:** Game Bar captures the focused window only — make sure your browser is maximized and focused

### Voice & Delivery
- Target pace: **130–140 words per minute** (slower = clearer for judges)
- Pause **1 full second** after each major demo action — let the UI respond visually
- Do **NOT** use the built-in laptop microphone — room echo will undermine credibility
- Record narration in a small, carpeted room or with a jacket/blanket behind you to dampen reverb
- If you stumble, **pause 3 seconds and restart that sentence** — edit in post

### Practice Protocol
1. Run through slides + dashboard demo **without recording** — fix any browser/server issues
2. Practice narration aloud **twice at full pace** — time yourself
3. **Third run: record** — do not stop unless critical error occurs (a stumble is recoverable in editing)

### Post-Recording
- Trim 1–2 seconds of silence from start and end
- Light colour grade if needed (Brightness +5, Contrast +10 in DaVinci Resolve free)
- Export at H.264 / AAC, YouTube-compatible preset
- **Upload to YouTube (Unlisted)** or Google Drive (link sharing ON)
- Paste the video link at the **very top of your GitHub README.md** — judges click the README first

---

## WHAT JUDGES WILL NOTICE

| Criterion | What Demonstrates It |
|---|---|
| **Epistemic precision** | Explicitly marking human identity as UNDETERMINED; not over-claiming |
| **Live demo credibility** | Real HTTP 403 / 200 switching in PEP Lab — not a mock screenshot |
| **Chain of custody** | SHA-256 hashes on all 12 evidence files, E01–E12, in Evidence Vault |
| **Statutory compliance** | DPDPA 2023 §8(5) mapping with specific penalty figures (₹250 Cr) |
| **Test coverage** | 15 unit + 10 simulation = 25/25 passing — zero failures |
| **MITRE ATT&CK alignment** | 10 detection rules mapped to T1078.004, T1552.001, T1530, T1567 |
| **Professional presentation** | Clean dashboard, no typos, no lag, no browser notifications on screen |
| **Reproducibility** | Full source on GitHub — judges can clone and run it themselves |

---

## QUICK REFERENCE — KEY FACTS FOR NARRATION

> Use these verbatim to avoid factual errors during delivery:

- **Incident window:** 12 October 2026, **03:15–03:24 IST** (9 minutes)
- **Attack source:** `203.0.113.77` (external — NOT in `10.10.4.0/24`)
- **Token:** `rc-prod-01` (JTI) — no expiry, no IP restriction, no rate limit
- **Data exfiltrated:** 2,300 student attendance records · **972.4 KB** · **2 downloads**
- **OWASP failures:** API1 (privilege creep) · API2 (no constraints) · API4 (no rate limit)
- **MITRE TTPs:** T1078.004 · T1552.001 · T1530 · T1567
- **PEP layers:** CIDR pinning → JWT scope gate → rate limiter → DPO two-man rule
- **Tests:** 15/15 unit + 10/10 simulation = **100% pass rate**
- **Penalty exposure:** DPDPA 2023 §8(5) — up to **₹250 Crores**
- **Reporting deadline:** CERT-In **6-hour mandatory** reporting obligation
- **Evidence files:** E01–E12 (12 files, all SHA-256 verified)
- **GitHub:** https://github.com/Heman-123/Northstar-Sentinel

---

*Script authored for CRIMEATHON '26 — Defense Track — Case NS-26-014*
*Team Northstar · Northstar Skills Academy, Chennai*
