"""
Generates the official CRIMEATHON '26 Deliverable 2 PowerPoint (.pptx) deck.
Auto-installs python-pptx if not present.
"""
import sys
import subprocess

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
except ImportError:
    print("[*] Installing python-pptx for PowerPoint generation...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

import os

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5) # 16:9 standard widescreen

    blank_layout = prs.slide_layouts[6]

    # Color palette
    BG_COLOR = RGBColor(11, 15, 25)        # #0b0f19
    CARD_BG = RGBColor(17, 23, 38)         # #111726
    TEXT_LIGHT = RGBColor(241, 245, 249)   # #f1f5f9
    TEXT_MUTED = RGBColor(148, 163, 184)   # #94a3b8
    CYAN_ACCENT = RGBColor(56, 189, 248)   # #38bdf8
    PURPLE_ACCENT = RGBColor(168, 85, 247) # #a855f7
    RED_ACCENT = RGBColor(248, 113, 113)   # #f87171
    GREEN_ACCENT = RGBColor(74, 222, 128)  # #4ade80

    def set_slide_bg(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

    def add_header(slide, title_text, category_text, slide_num):
        # Category / Badge
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category_text.upper()
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

        # Title
        p2 = tf.add_paragraph()
        p2.text = title_text
        p2.font.name = "Arial"
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_LIGHT

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.4), Inches(1.2), Inches(0.4))
        np = num_box.text_frame.paragraphs[0]
        np.alignment = PP_ALIGN.RIGHT
        np.text = f"SLIDE {slide_num} / 8"
        np.font.name = "Arial"
        np.font.size = Pt(11)
        np.font.bold = True
        np.font.color.rgb = PURPLE_ACCENT

    # -------------------------------------------------------------
    # SLIDE 1: Title
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)

    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.5))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "CRIMEATHON '26 — DEFENSE TRACK MASTER PRESENTATION"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "NORTHSTAR SENTINEL"
    p2.font.name = "Arial"
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_LIGHT
    p2.space_after = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "Autonomous Forensic Correlation, Behavioral Detection & Zero-Trust Incident Response"
    p3.font.name = "Arial"
    p3.font.size = Pt(20)
    p3.font.color.rgb = PURPLE_ACCENT
    p3.space_after = Pt(24)

    p4 = tf1.add_paragraph()
    p4.text = "Target Case: NS-26-014 (Northstar Skills Academy, Chennai) | Track: Applied Defense | Team: Sentinel Taskforce"
    p4.font.name = "Arial"
    p4.font.size = Pt(12)
    p4.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 2: Problem Identification & Threat Landscape
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "Problem Identification & Threat Landscape", "Vulnerability Analysis", 2)

    box = s2.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "The Breach Event (12 October 2026):"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RED_ACCENT
    p.space_after = Pt(6)

    bullets = [
        "Unscheduled attendance sync failures, portal latencies soaring to 8,420ms, and exfiltration of 2,300 learner PII records.",
        "Compromised integration token (rc-prod-01) belonging to service account svc_rollcall.",
        "Total uncompressed exfiltration volume: 972.4 KB across 2 staging downloads (learners-20261012.csv)."
    ]
    for b in bullets:
        bp = tf.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(13)
        bp.font.color.rgb = TEXT_LIGHT
        bp.space_after = Pt(4)

    p = tf.add_paragraph()
    p.text = "Root Vulnerability Breakdown:"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.space_before = Pt(12)
    p.space_after = Pt(6)

    vulns = [
        "CWE-250 / OWASP API1: Architectural Privilege Creep — Integration client granted learner.export permissions despite attendance-only scope.",
        "CWE-798 / OWASP API2: Broken Credential Hygiene — Integration token configured with Expiry: Never and IP Restriction: None.",
        "CWE-770 / OWASP API4: Unrestricted Resource Consumption — Complete absence of rate limiting and two-man approval controls on bulk export endpoints."
    ]
    for v in vulns:
        vp = tf.add_paragraph()
        vp.text = "• " + v
        vp.font.size = Pt(13)
        vp.font.color.rgb = TEXT_LIGHT
        vp.space_after = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 3: Forensic Epistemology (ISO/IEC 27037)
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "Forensic Evidence Correlation & Epistemic Truth Matrix", "Forensic Epistemology (ISO/IEC 27037)", 3)

    box = s3.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    sections = [
        ("CONFIRMED FACTS (Direct Artifact Evidence)", GREEN_ACCENT, [
            "External IP 203.0.113.77 authenticated machine account svc_rollcall via valid Bearer token at 03:15:55 IST.",
            "Client queried 2,300 records at 03:16:40 IST (E03:R003) and executed bulk export at 03:17:09 IST (E03:R004).",
            "CampusVault object learners-20261012.csv downloaded twice totaling 972,400 bytes (E04:C003, C004)."
        ]),
        ("SUPPORTED INFERENCES (Corroborated Telemetry)", CYAN_ACCENT, [
            "Credential leak occurred via unredacted support screenshot HD-1058 (E06) or unauthorized config read CHG-882 (E11).",
            "Web portal latency spike (8,420ms) was caused by full-table scan triggered by unindexed 2,300-row query."
        ]),
        ("EPISTEMIC UNKNOWNS (Rigorous Non-Attribution)", PURPLE_ACCENT, [
            "Identity/physical location of the human operator behind 203.0.113.77 remains unproven (requires ISP subpoena).",
            "Post-termination login by former employee Ajay (former.ajay, Oct 9) is an offboarding failure, NOT causally linked to RollCall."
        ])
    ]

    for title, col, items in sections:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)

        for item in items:
            ip = tf.add_paragraph()
            ip.text = "  • " + item
            ip.font.size = Pt(12)
            ip.font.color.rgb = TEXT_LIGHT
            ip.space_after = Pt(3)

    # -------------------------------------------------------------
    # SLIDE 4: Proposed Solution: Dual-Engine Architecture
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "Proposed Solution: Northstar Sentinel Dual Engine", "Defensive Innovation", 4)

    box = s4.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "PILLAR 1: Evidence-Driven DFIR Intelligence Pipeline (Stages 1–6)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(6)

    p1_items = [
        "Cryptographic Integrity: SHA-256 ingestion verifying 12/12 evidence files without chain-of-custody breaks.",
        "OCSF Schema Normalization: Standardizes heterogeneous syslog, auth, API, and cloud trail formats into single schema.",
        "Correlation & Behavioral Detection: 9 correlation rules and 10 explainable behavioral rules (DET-001 to DET-010) mapped to MITRE ATT&CK."
    ]
    for it in p1_items:
        ip = tf.add_paragraph()
        ip.text = "• " + it
        ip.font.size = Pt(13)
        ip.font.color.rgb = TEXT_LIGHT
        ip.space_after = Pt(4)

    p = tf.add_paragraph()
    p.text = "PILLAR 2: Zero-Trust Policy Enforcement Point (PEP Reverse Proxy)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p.space_before = Pt(12)
    p.space_after = Pt(6)

    p2_items = [
        "CIDR Subnet Pinning: Restricts RollCall integration strictly to authorized subnet 10.10.4.0/24 (HTTP 403 on external).",
        "Strict Least-Privilege Scope Gate: Clamps tokens to attendance:* only, dropping learner.export privilege creep.",
        "Token-Bucket Rate Limiter: Enforces 10 req/min throttling to defeat bulk scraping (HTTP 429).",
        "Two-Man DPO Cryptographic Rule: Hard blocks bulk PII export without dual cryptographic approval token."
    ]
    for it in p2_items:
        ip = tf.add_paragraph()
        ip.text = "• " + it
        ip.font.size = Pt(13)
        ip.font.color.rgb = TEXT_LIGHT
        ip.space_after = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 5: Architecture & Data Pipeline
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "System Architecture & Processing Pipeline", "System Architecture", 5)

    box = s5.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "DATA FLOW & PIPELINE TOPOLOGY:"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(8)

    flow = [
        "1. Evidence Ingestion & Hashing: Computes SHA-256 digests across all 12 evidence artifacts (E01-E12).",
        "2. Normalization Engine: Parses raw logs into standardized OCSF JSON events with UTC/IST timestamps.",
        "3. Correlation Engine: Applies multi-source correlation linking auth events, API calls, and object downloads.",
        "4. Detection Engine: Evaluates 10 behavioral rules, generating MITRE ATT&CK alerts and triage risk scores.",
        "5. Zero-Trust PEP Gateway: Real-time reverse proxy inspecting HTTP traffic, validating CIDR, scope, and rate limits.",
        "6. Splunk ES Incident Workbench: High-density analyst GUI with live telemetry radar, topology graph, and SOAR response."
    ]
    for step in flow:
        sp = tf.add_paragraph()
        sp.text = step
        sp.font.size = Pt(13)
        sp.font.color.rgb = TEXT_LIGHT
        sp.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 6: Technologies, Standards & Tools Used
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, "Technologies, Standards & Frameworks Used", "Technical Stack", 6)

    box = s6.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    techs = [
        ("Core Backend & Forensic Pipeline:", "Python 3.9+ (Standard Library: hashlib, ipaddress, csv, json, http.server, unittest), Pytest."),
        ("Frontend & SOC Workbench:", "HTML5, Tailwind CSS, Lucide Icons, Modern Splunk Enterprise Security Dark Theme layout."),
        ("Schema Standards:", "Open Cybersecurity Schema Framework (OCSF v1.1.0) event normalization."),
        ("Threat Framework:", "MITRE ATT&CK v14.1 (T1078.004, T1552.001, T1530, T1567, T1098)."),
        ("API Security Standard:", "OWASP API Security Top 10 (2023) — API1: BOLA, API2: Broken Auth, API4: Unrestricted Resource Consumption."),
        ("Legal & Statutory Governance:", "Digital Personal Data Protection Act (DPDPA 2023) Section 8(5) & CERT-In 6-Hour Reporting Mandate.")
    ]

    for title, desc in techs:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = "• " + title + " "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_after = Pt(4)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_LIGHT

    # -------------------------------------------------------------
    # SLIDE 7: Experimental Verification & Results
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, "Experimental Results & Verification Matrix", "Empirical Validation", 7)

    box = s7.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SIMULATION TEST HARNESS EXECUTION: 10 / 10 TESTS PASSED (100% PASS RATE)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = GREEN_ACCENT
    p.space_after = Pt(12)

    results = [
        ("External IP Replay (203.0.113.77):", "Vulnerable: ALLOWED (HTTP 200, PII Leaked) -> Hardened: BLOCKED (HTTP 403 Forbidden)"),
        ("Privilege Creep (learner.export):", "Vulnerable: ALLOWED (HTTP 200, Mass Staged) -> Hardened: BLOCKED (HTTP 403 Forbidden)"),
        ("High-Frequency Scraping (>10 req/min):", "Vulnerable: ALLOWED (Portal Degraded 8.4s) -> Hardened: THROTTLED (HTTP 429 Rate Limit Exceeded)"),
        ("Unapproved Bulk Export:", "Vulnerable: STAGED (2,300 records exposed) -> Hardened: BLOCKED (HTTP 403 Missing DPO Two-Man Sign-Off)"),
        ("Legitimate Integration Request:", "Vulnerable: ALLOWED -> Hardened: ALLOWED (HTTP 200 OK via Whitelisted 10.10.4.15)")
    ]

    for title, desc in results:
        p = tf.add_paragraph()
        p.text = "• " + title + " "
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.space_after = Pt(4)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_LIGHT

    # -------------------------------------------------------------
    # SLIDE 8: Statutory Impact & Incident Response Plan
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, "Statutory Compliance & Strategic Roadmap", "Governance & Outlook", 8)

    box = s8.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True

    sections_s8 = [
        ("DPDPA 2023 & CERT-In Legal Exposure:", RED_ACCENT, [
            "Section 8(5) Penalty Exposure: Failure to protect personal data attracts penalties up to Rs. 250 Crores.",
            "CERT-In Mandate: Obligatory incident reporting within 6 hours of discovery under Cyber Security Directions 2022."
        ]),
        ("Immediate 24-Hour Remediation Actions:", CYAN_ACCENT, [
            "Emergency revocation and regeneration of RollCall integration token rc-prod-01.",
            "Deployment of in-line PEP reverse proxy enforcing subnet pinning (10.10.4.0/24).",
            "Offboarding audit disabling dormant accounts (former.ajay) and implementing auto-deprovisioning."
        ]),
        ("Future Roadmap:", PURPLE_ACCENT, [
            "Production rollout of automated SOAR playbooks for automated IP isolation and token invalidation.",
            "Expansion of OCSF correlation to hybrid cloud and multi-tenant SaaS environments."
        ])
    ]

    for title, col, items in sections_s8:
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)

        for item in items:
            ip = tf.add_paragraph()
            ip.text = "  • " + item
            ip.font.size = Pt(12)
            ip.font.color.rgb = TEXT_LIGHT
            ip.space_after = Pt(3)

    out_path = os.path.join(os.path.dirname(__file__), "reports", "CRIMEATHON_26_PRESENTATION_DECK.pptx")
    prs.save(out_path)
    print(f"[+] Master 8-Slide PowerPoint Presentation Deck successfully created at:\n    {out_path}")

if __name__ == "__main__":
    create_deck()
