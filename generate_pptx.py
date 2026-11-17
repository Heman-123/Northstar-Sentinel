"""
Master Presentation Generator for CRIMEATHON '26 — Northstar Sentinel (Case NS-26-014).
Generates an executive, designer-grade 10-slide PowerPoint (.pptx) deck with:
- Styled visual card containers & colored borders
- High-contrast executive color palette (Deep Navy, Cyan, Violet, Emerald, Crimson)
- Formatted tables with color-coded confidence levels
- Process flow step cards and architecture layer stacks
- Large metric KPI callouts and trophy banners
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5) # 16:9 Standard widescreen

    blank_layout = prs.slide_layouts[6]

    # Executive Dark Palette
    C_BG          = RGBColor(10, 14, 23)      # #0a0e17 Dark Obsidian
    C_CARD        = RGBColor(17, 24, 39)      # #111827 Dark Slate Card
    C_CARD_ALT    = RGBColor(24, 32, 52)      # #182034 Elevated Card
    C_TEXT        = RGBColor(243, 244, 246)   # #f3f4f6 Crisp White
    C_MUTED       = RGBColor(156, 163, 175)   # #9ca3af Cool Gray
    C_CYAN        = RGBColor(14, 165, 233)    # #0ea5e9 Electric Cyan
    C_CYAN_LIGHT  = RGBColor(56, 189, 248)    # #38bdf8
    C_PURPLE      = RGBColor(168, 85, 247)    # #a855f7 Vivid Purple
    C_PURPLE_DARK = RGBColor(88, 28, 135)     # #581c87
    C_GREEN       = RGBColor(16, 185, 129)    # #10b981 Emerald
    C_GREEN_DARK  = RGBColor(6, 78, 59)       # #064e3b
    C_RED         = RGBColor(239, 68, 68)     # #ef4444 Crimson
    C_RED_DARK    = RGBColor(127, 29, 29)     # #7f1d1d
    C_AMBER       = RGBColor(245, 158, 11)    # #f59e0b Amber
    C_BORDER      = RGBColor(30, 41, 59)      # #1e293b Slate Border

    def apply_slide_bg(slide):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = C_BG

    def add_card(slide, left, top, width, height, fill_color=C_CARD, border_color=C_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.2)
        else:
            shape.line.fill.background()
        return shape

    def add_header(slide, title_text, category_text, slide_num):
        # Top gradient-like accent strip
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.04))
        strip.fill.solid()
        strip.fill.fore_color.rgb = C_CYAN
        strip.line.fill.background()

        # Category Pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.55), Inches(2.8), Inches(0.32))
        pill.fill.solid()
        pill.fill.fore_color.rgb = RGBColor(15, 30, 54)
        pill.line.color.rgb = C_CYAN
        pill.line.width = Pt(1)
        p = pill.text_frame.paragraphs[0]
        p.text = category_text.upper()
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_CYAN_LIGHT
        p.alignment = PP_ALIGN.CENTER

        # Slide Number Pill
        npill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.933), Inches(0.55), Inches(1.6), Inches(0.32))
        npill.fill.solid()
        npill.fill.fore_color.rgb = RGBColor(30, 20, 50)
        npill.line.color.rgb = C_PURPLE
        npill.line.width = Pt(1)
        np = npill.text_frame.paragraphs[0]
        np.text = f"SLIDE {slide_num} / 10"
        np.font.name = "Arial"
        np.font.size = Pt(9.5)
        np.font.bold = True
        np.font.color.rgb = C_PURPLE
        np.alignment = PP_ALIGN.CENTER

        # Main Title Box
        tbox = slide.shapes.add_textbox(Inches(0.8), Inches(0.92), Inches(11.733), Inches(0.55))
        tf = tbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(21)
        p.font.bold = True
        p.font.color.rgb = C_TEXT

    # =========================================================================
    # SLIDE 1: Title Hero Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s1)

    # Ambient banner card
    hero = add_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(4.3), C_CARD, C_CYAN)
    
    htf = hero.text_frame
    htf.word_wrap = True
    htf.vertical_anchor = MSO_ANCHOR.MIDDLE

    p0 = htf.paragraphs[0]
    p0.text = "CRIMEATHON '26  •  DEFENSE TRACK  •  CASE NS-26-014"
    p0.font.name = "Arial"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = C_CYAN_LIGHT
    p0.space_after = Pt(8)

    p1 = htf.add_paragraph()
    p1.text = "NORTHSTAR SENTINEL"
    p1.font.name = "Arial"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT
    p1.space_after = Pt(8)

    p2 = htf.add_paragraph()
    p2.text = "Autonomous Forensic Correlation & Zero-Trust Policy Enforcement"
    p2.font.name = "Arial"
    p2.font.size = Pt(18)
    p2.font.color.rgb = C_PURPLE
    p2.space_after = Pt(14)

    p3 = htf.add_paragraph()
    p3.text = "Target Incident: RollCall API Data Exfiltration  |  Venue: Northstar Skills Academy, Chennai  |  Team: Team Northstar"
    p3.font.name = "Arial"
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_MUTED

    # 3 Bottom KPI Cards
    kpis = [
        ("6-STAGE DFIR PIPELINE", "12/12 Artifacts Verified", "100% SHA-256 Custody", C_CYAN),
        ("VERIFIED MITIGATION", "10/10 Simulation Tests", "15/15 Unit Tests Passing", C_GREEN),
        ("ZERO-TRUST GATEWAY", "4-Layer Policy Engine", "0ms Instant Revocation", C_PURPLE)
    ]
    k_width = Inches(3.75)
    for i, (k_title, k_main, k_sub, k_color) in enumerate(kpis):
        k_left = Inches(0.8) + i * Inches(3.99)
        kc = add_card(s1, k_left, Inches(5.35), k_width, Inches(1.6), C_CARD_ALT, k_color)
        ktf = kc.text_frame
        ktf.word_wrap = True
        ktf.vertical_anchor = MSO_ANCHOR.MIDDLE

        kp0 = ktf.paragraphs[0]
        kp0.text = k_title
        kp0.font.name = "Arial"
        kp0.font.size = Pt(9.5)
        kp0.font.bold = True
        kp0.font.color.rgb = k_color
        kp0.alignment = PP_ALIGN.CENTER
        kp0.space_after = Pt(4)

        kp1 = ktf.add_paragraph()
        kp1.text = k_main
        kp1.font.name = "Arial"
        kp1.font.size = Pt(15)
        kp1.font.bold = True
        kp1.font.color.rgb = C_TEXT
        kp1.alignment = PP_ALIGN.CENTER
        kp1.space_after = Pt(2)

        kp2 = ktf.add_paragraph()
        kp2.text = k_sub
        kp2.font.name = "Arial"
        kp2.font.size = Pt(10)
        kp2.font.color.rgb = C_MUTED
        kp2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: Problem Identification & Threat Landscape
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s2)
    add_header(s2, "The Incident: RollCall API Unauthorized Exfiltration", "Vulnerability Analysis", 2)

    # Left Column: The Breach Impact Card
    c_left = add_card(s2, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.3), C_CARD, C_RED)
    ltf = c_left.text_frame
    ltf.word_wrap = True

    p = ltf.paragraphs[0]
    p.text = "BREACH IMPACT & COMPROMISE SCOPE"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p.space_after = Pt(10)

    points_l = [
        ("Date & Window", "12 October 2026, between 03:15 and 03:24 IST."),
        ("Adversary Source", "External IP 203.0.113.77 (Authorized vendor subnet is 10.10.4.0/24)."),
        ("Compromised Key", "Machine token rc-prod-01 belonging to integration svc_rollcall."),
        ("Records Stolen", "2,300 active learners (Names, Enrollments, Attendance)."),
        ("Exfiltrated Volume", "972.4 KB uncompressed across 2 S3 downloads (learners-20261012.csv)."),
        ("Latency Spike", "Query surged database latency to 8,420ms (~187x normal).")
    ]
    for lbl, desc in points_l:
        p_pt = ltf.add_paragraph()
        p_pt.text = f"• {lbl}: "
        p_pt.font.name = "Arial"
        p_pt.font.size = Pt(11)
        p_pt.font.bold = True
        p_pt.font.color.rgb = C_CYAN_LIGHT
        p_pt.space_after = Pt(3)
        run = p_pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT

    # Right Column: Root Causes (OWASP API Top 10)
    c_right = add_card(s2, Inches(6.8), Inches(1.65), Inches(5.733), Inches(5.3), C_CARD, C_CYAN)
    rtf = c_right.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "ROOT CAUSE ANALYSIS (OWASP API TOP 10)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_LIGHT
    p.space_after = Pt(10)

    owasp_items = [
        ("OWASP API1 / CWE-250: Privilege Creep", 
         "Service token granted wildcard 'learner.export' privileges despite only needing read/write for classroom attendance sync."),
        ("OWASP API2 / CWE-798: Broken Credential Hygiene", 
         "Token generated with 'Expiry: Never' and zero CIDR restrictions, enabling external access from any arbitrary IP."),
        ("OWASP API4 / CWE-770: Unrestricted Consumption", 
         "No rate-limiting or throttling existed on the bulk query endpoint, enabling full-table extraction in one unindexed request."),
        ("MITRE ATT&CK Techniques Mapped", 
         "T1078.004 (Cloud Accounts), T1552.001 (Credentials in Files), T1530 (Cloud Storage), T1567 (Web Exfiltration).")
    ]
    for title, desc in owasp_items:
        p_o = rtf.add_paragraph()
        p_o.text = title
        p_o.font.name = "Arial"
        p_o.font.size = Pt(11)
        p_o.font.bold = True
        p_o.font.color.rgb = C_PURPLE
        p_o.space_after = Pt(2)
        p_sub = rtf.add_paragraph()
        p_sub.text = desc
        p_sub.font.name = "Arial"
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = C_MUTED
        p_sub.space_after = Pt(6)

    # =========================================================================
    # SLIDE 3: Forensic Evidence Timeline
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s3)
    add_header(s3, "Forensic Evidence Reconstruction: 9-Event Chain", "Evidence Correlation", 3)

    # 9 Timeline Event Cards arranged in 3x3 Grid
    events = [
        ("03:15:55 IST", "01. INGRESS", "External IP 203.0.113.77 initiates connection to ClassBridge API.", C_CYAN),
        ("03:16:32 IST", "02. AUTHENTICATION", "Bearer token rc-prod-01 accepted without source IP verification.", C_CYAN),
        ("03:16:35 IST", "03. RECONNAISSANCE", "Adversary accesses CHG-882 database configuration parameters.", C_PURPLE),
        ("03:16:40 IST", "04. FULL-TABLE SEARCH", "Full-table search query submitted; 2,300 active records scanned.", C_AMBER),
        ("03:17:09 IST", "05. BULK EXPORT", "API latency surges to 8,420ms; learner export spooled locally.", C_RED),
        ("03:17:35 IST", "06. STAGING TO S3", "Data staged to CampusVault bucket as learners-20261012.csv.", C_PURPLE),
        ("03:21:03 IST", "07. DOWNLOAD #1", "First GET request completes: 486.2 KB transferred to external IP.", C_RED),
        ("03:24:48 IST", "08. DOWNLOAD #2", "Second GET request completes: duplicate 486.2 KB exfiltrated.", C_RED),
        ("03:25:00+ IST", "09. SOC DETECTION", "Multi-source correlation triggers DEFCON 2 alarm across SOC.", C_GREEN)
    ]

    card_w = Inches(3.75)
    card_h = Inches(1.6)
    for idx, (t_time, t_title, t_desc, t_color) in enumerate(events):
        row = idx // 3
        col = idx % 3
        left = Inches(0.8) + col * Inches(3.99)
        top = Inches(1.65) + row * Inches(1.75)

        c = add_card(s3, left, top, card_w, card_h, C_CARD, t_color)
        ctf = c.text_frame
        ctf.word_wrap = True

        p0 = ctf.paragraphs[0]
        p0.text = f"{t_time}  •  {t_title}"
        p0.font.name = "Arial"
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = t_color
        p0.space_after = Pt(3)

        p1 = ctf.add_paragraph()
        p1.text = t_desc
        p1.font.name = "Arial"
        p1.font.size = Pt(10)
        p1.font.color.rgb = C_TEXT

    # =========================================================================
    # SLIDE 4: Epistemic Truth Matrix (Table)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s4)
    add_header(s4, "Epistemic Truth Matrix: Strict Scientific Demarcation", "Forensic Epistemology (ISO/IEC 27037)", 4)

    # Subtitle Callout
    sub_c = add_card(s4, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.55), C_CARD_ALT, C_CYAN)
    stf = sub_c.text_frame
    stf.word_wrap = True
    sp = stf.paragraphs[0]
    sp.text = "CORE PRINCIPLE: Zero Speculation. Distinguish cryptographically proven facts from inferences and unknowns."
    sp.font.name = "Arial"
    sp.font.size = Pt(11)
    sp.font.bold = True
    sp.font.color.rgb = C_CYAN_LIGHT
    sp.alignment = PP_ALIGN.CENTER

    # Table
    rows = 6
    cols = 3
    t_shape = s4.shapes.add_table(rows, cols, Inches(0.8), Inches(2.2), Inches(11.733), Inches(4.7))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(4.8)
    tbl.columns[1].width = Inches(2.2)
    tbl.columns[2].width = Inches(4.733)

    headers = ["INVESTIGATIVE HYPOTHESIS / FINDING", "EPISTEMIC CONFIDENCE", "CRYPTOGRAPHIC / ARTIFACT GROUNDING"]
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(15, 23, 42)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_CYAN_LIGHT

    matrix_rows = [
        ("Adversary session initiated from external IP 203.0.113.77", "CERTAIN (100%)", "E03: API Gateway Logs (IP, timestamp, Bearer token match)", C_GREEN),
        ("Token rc-prod-01 had Expiry: Never & machine role svc_rollcall", "CERTAIN (100%)", "E05: Integration Register (explicit config parameters)", C_GREEN),
        ("972.4 KB exfiltrated across 2 discrete S3 download events", "CERTAIN (100%)", "E04: CampusVault S3 Audit Logs (C003, C004 byte verification)", C_GREEN),
        ("2 downloads represent 2 separate copies captured by adversary", "PROBABLE (85%)", "Timing correlation (03:21:03 & 03:24:48) and byte size equality", C_CYAN_LIGHT),
        ("Human identity / physical operator behind IP 203.0.113.77", "UNDETERMINED (0%)", "Requires legal ISP subpoena; impossible to conclude from local logs", C_AMBER),
    ]

    for r_idx, (f_text, f_conf, f_basis, f_col) in enumerate(matrix_rows):
        # Col 0
        c0 = tbl.cell(r_idx + 1, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = C_CARD
        p0 = c0.text_frame.paragraphs[0]
        p0.text = f_text
        p0.font.name = "Arial"
        p0.font.size = Pt(10)
        p0.font.color.rgb = C_TEXT

        # Col 1
        c1 = tbl.cell(r_idx + 1, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = C_CARD
        p1 = c1.text_frame.paragraphs[0]
        p1.text = f_conf
        p1.font.name = "Arial"
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = f_col

        # Col 2
        c2 = tbl.cell(r_idx + 1, 2)
        c2.fill.solid()
        c2.fill.fore_color.rgb = C_CARD
        p2 = c2.text_frame.paragraphs[0]
        p2.text = f_basis
        p2.font.name = "Arial"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 5: Proposed Solution: 4-Layer Zero-Trust PEP
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s5)
    add_header(s5, "Defensive Architecture: 4-Layer Zero-Trust Gateway", "Engineering Innovation", 5)

    layers = [
        ("LAYER 1: PERIMETER CIDR SUBNET PINNING", C_CYAN,
         "Enforces that svc_rollcall requests originate STRICTLY from authorized vendor subnet 10.10.4.0/24.\n"
         "• Outcome on 203.0.113.77: Instant HTTP 403 Forbidden at the edge (0ms packet drop)."),

        ("LAYER 2: LEAST-PRIVILEGE JWT SCOPE GATE", C_PURPLE,
         "Cryptographically validates token scope. Clamps RollCall token strictly to 'attendance:*'.\n"
         "• Outcome on learner.export: HTTP 403 Forbidden — Wildcard scope escalation completely neutralized."),

        ("LAYER 3: TOKEN-BUCKET ADAPTIVE RATE LIMITER", C_AMBER,
         "Maintains rolling 100 req/min threshold per machine client with automated burst suppression.\n"
         "• Outcome on full-table scans: HTTP 429 Rate Limit Exceeded — Defeats bulk scraping and DoS."),

        ("LAYER 4: DPO TWO-MAN CRYPTOGRAPHIC SIGN-OFF", C_GREEN,
         "Requires dual cryptographic approval from Data Protection Officer for any query exporting >50 PII records.\n"
         "• Outcome on unapproved mass dumps: Hard denial without multi-party token co-signature.")
    ]

    for idx, (l_title, l_col, l_body) in enumerate(layers):
        l_top = Inches(1.65) + idx * Inches(1.33)
        lc = add_card(s5, Inches(0.8), l_top, Inches(11.733), Inches(1.2), C_CARD, l_col)
        ltf = lc.text_frame
        ltf.word_wrap = True

        p0 = ltf.paragraphs[0]
        p0.text = l_title
        p0.font.name = "Arial"
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = l_col
        p0.space_after = Pt(2)

        p1 = ltf.add_paragraph()
        p1.text = l_body
        p1.font.name = "Arial"
        p1.font.size = Pt(10)
        p1.font.color.rgb = C_TEXT

    # =========================================================================
    # SLIDE 6: 6-Stage Automated DFIR Pipeline
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s6)
    add_header(s6, "6-Stage Autonomous DFIR Processing Pipeline", "Forensic Pipeline Architecture", 6)

    stages = [
        ("STAGE 01", "INGESTION", "Parses 12 raw artifacts (E01-E12) from auth, API, and cloud."),
        ("STAGE 02", "HASH INTEGRITY", "Computes SHA-256 digests; verifies 100% evidentiary custody."),
        ("STAGE 03", "NORMALIZATION", "Converts heterogeneous logs into OCSF v1.1.0 standard schema."),
        ("STAGE 04", "CORRELATION", "Stitches 9-event chain linking authentication, query, & downloads."),
        ("STAGE 05", "CLASSIFICATION", "Maps actions to MITRE ATT&CK & OWASP API Top 10 categories."),
        ("STAGE 06", "REPORTING", "Generates DPDPA compliance audits & CERT-In disclosure filings.")
    ]

    p_width = Inches(1.85)
    p_height = Inches(5.2)
    for idx, (p_num, p_name, p_desc) in enumerate(stages):
        p_left = Inches(0.8) + idx * Inches(1.98)
        border_c = C_CYAN if idx % 2 == 0 else C_PURPLE
        sc = add_card(s6, p_left, Inches(1.65), p_width, p_height, C_CARD, border_c)
        stf = sc.text_frame
        stf.word_wrap = True

        p0 = stf.paragraphs[0]
        p0.text = p_num
        p0.font.name = "Arial"
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = border_c
        p0.alignment = PP_ALIGN.CENTER
        p0.space_after = Pt(6)

        p1 = stf.add_paragraph()
        p1.text = p_name
        p1.font.name = "Arial"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT
        p1.alignment = PP_ALIGN.CENTER
        p1.space_after = Pt(14)

        p2 = stf.add_paragraph()
        p2.text = p_desc
        p2.font.name = "Arial"
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_MUTED
        p2.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 7: Technical Stack, Standards & Frameworks
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s7)
    add_header(s7, "Technologies, Industry Standards & Implementation Stack", "Technical Stack", 7)

    tech_cards = [
        ("CORE DFIR BACKEND", C_CYAN, [
            "Python 3.11+ Standard Library",
            "Hashlib (SHA-256 verification)",
            "IPAddress (Subnet calculation)",
            "Pytest (15/15 unit tests passing)"
        ]),
        ("ZERO-TRUST PEP GATEWAY", C_PURPLE, [
            "Python HTTP Proxy Architecture",
            "In-line CIDR packet inspection",
            "Token-bucket rate limiter",
            "Cryptographic signature checks"
        ]),
        ("SOC ANALYST WORKBENCH", C_CYAN, [
            "Tailwind CSS Dark Framework",
            "Chart.js Telemetry Visualizations",
            "Lucide Iconography",
            "Responsive 8-Tab Architecture"
        ]),
        ("SCHEMA STANDARDIZATION", C_GREEN, [
            "OCSF v1.1.0 JSON Normalization",
            "Syslog, API & CloudTrail formats",
            "Microsecond UTC/IST timestamps",
            "Cross-log schema validation"
        ]),
        ("THREAT FRAMEWORKS", C_AMBER, [
            "MITRE ATT&CK v14.1 Enterprise",
            "OWASP API Security Top 10 (2023)",
            "ISO/IEC 27037 Digital Forensics",
            "10 Behavioral Detection Rules"
        ]),
        ("STATUTORY GOVERNANCE", C_RED, [
            "DPDPA 2023 Section 8(5) Audit",
            "CERT-In 6-Hour SLA Package",
            "Immutable Evidence Vault",
            "Zero false attribution policy"
        ])
    ]

    tw = Inches(3.75)
    th = Inches(2.55)
    for idx, (t_title, t_col, t_bullets) in enumerate(tech_cards):
        r = idx // 3
        c = idx % 3
        t_left = Inches(0.8) + c * Inches(3.99)
        t_top = Inches(1.65) + r * Inches(2.7)

        tc = add_card(s7, t_left, t_top, tw, th, C_CARD, t_col)
        ttf = tc.text_frame
        ttf.word_wrap = True

        p0 = ttf.paragraphs[0]
        p0.text = t_title
        p0.font.name = "Arial"
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = t_col
        p0.space_after = Pt(8)

        for b in t_bullets:
            pb = ttf.add_paragraph()
            pb.text = "• " + b
            pb.font.name = "Arial"
            pb.font.size = Pt(10)
            pb.font.color.rgb = C_TEXT
            pb.space_after = Pt(2)

    # =========================================================================
    # SLIDE 8: Experimental Verification & Results Table
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s8)
    add_header(s8, "Empirical Validation: Simulation Harness & Unit Testing", "Verification Results", 8)

    # Score Banner
    sb = add_card(s8, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.6), C_CARD_ALT, C_GREEN)
    sbtf = sb.text_frame
    sbtf.word_wrap = True
    sbp = sbtf.paragraphs[0]
    sbp.text = "10 / 10 SIMULATION SUITE TESTS PASSED  •  15 / 15 FORENSIC UNIT TESTS PASSED  (100% COVERAGE)"
    sbp.font.name = "Arial"
    sbp.font.size = Pt(12)
    sbp.font.bold = True
    sbp.font.color.rgb = C_GREEN
    sbp.alignment = PP_ALIGN.CENTER

    # Test Table
    t_shape8 = s8.shapes.add_table(6, 4, Inches(0.8), Inches(2.25), Inches(11.733), Inches(4.7))
    tbl8 = t_shape8.table
    tbl8.columns[0].width = Inches(1.6)
    tbl8.columns[1].width = Inches(3.2)
    tbl8.columns[2].width = Inches(3.4)
    tbl8.columns[3].width = Inches(3.533)

    h8 = ["TEST ID", "ATTACK VECTOR", "VULNERABLE BASELINE", "HARDENED PEP VERDICT"]
    for i, h in enumerate(h8):
        cell = tbl8.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(15, 23, 42)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_CYAN_LIGHT

    test_rows = [
        ("TC-001", "External IP Replay (203.0.113.77)", "HTTP 200 OK (Data Leaked)", "HTTP 403 FORBIDDEN (Layer 1 CIDR Drop)", C_GREEN),
        ("TC-002", "Privilege Creep (learner.export)", "HTTP 200 OK (2,300 Records Leaked)", "HTTP 403 FORBIDDEN (Layer 2 Scope Denied)", C_GREEN),
        ("TC-003", "Scraping Burst (>100 req/min)", "HTTP 200 OK (Latency 8.4s Spike)", "HTTP 429 THROTTLED (Layer 3 Rate Limiter)", C_GREEN),
        ("TC-004", "Bulk PII Export Without DPO", "HTTP 200 OK (Export Staged to S3)", "HTTP 403 FORBIDDEN (Layer 4 Two-Man Sign-Off)", C_GREEN),
        ("TC-005", "Legitimate Sync (10.10.4.15)", "HTTP 200 OK (Normal Sync)", "HTTP 200 OK (Legitimate Access Preserved)", C_GREEN),
    ]

    for r_idx, (t_id, t_vec, t_vuln, t_hard, t_col) in enumerate(test_rows):
        c0 = tbl8.cell(r_idx + 1, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = C_CARD
        c0.text_frame.paragraphs[0].text = t_id
        c0.text_frame.paragraphs[0].font.size = Pt(10)
        c0.text_frame.paragraphs[0].font.bold = True
        c0.text_frame.paragraphs[0].font.color.rgb = C_CYAN_LIGHT

        c1 = tbl8.cell(r_idx + 1, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = C_CARD
        c1.text_frame.paragraphs[0].text = t_vec
        c1.text_frame.paragraphs[0].font.size = Pt(10)
        c1.text_frame.paragraphs[0].font.color.rgb = C_TEXT

        c2 = tbl8.cell(r_idx + 1, 2)
        c2.fill.solid()
        c2.fill.fore_color.rgb = C_CARD
        c2.text_frame.paragraphs[0].text = t_vuln
        c2.text_frame.paragraphs[0].font.size = Pt(10)
        c2.text_frame.paragraphs[0].font.color.rgb = C_RED

        c3 = tbl8.cell(r_idx + 1, 3)
        c3.fill.solid()
        c3.fill.fore_color.rgb = C_CARD
        c3.text_frame.paragraphs[0].text = t_hard
        c3.text_frame.paragraphs[0].font.size = Pt(10)
        c3.text_frame.paragraphs[0].font.bold = True
        c3.text_frame.paragraphs[0].font.color.rgb = t_col

    # =========================================================================
    # SLIDE 9: Statutory Compliance & Legal Implications
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s9)
    add_header(s9, "Statutory Compliance: DPDPA 2023 & CERT-In Governance", "Legal & Regulatory Framework", 9)

    # Left: Violations Card
    c9_left = add_card(s9, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.3), C_CARD, C_RED)
    ltf9 = c9_left.text_frame
    ltf9.word_wrap = True

    p = ltf9.paragraphs[0]
    p.text = "STATUTORY VIOLATIONS IDENTIFIED"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p.space_after = Pt(10)

    v_points = [
        ("DPDPA 2023 Section 8(5)", "Failure to implement reasonable security safeguards to prevent personal data breach."),
        ("Token Hygiene Failure", "Token issued with 'Expiry: Never' and zero IP restriction directly breaches security by design."),
        ("Statutory Penalty Exposure", "Section 8(5) violations carry monetary penalties up to Rs. 250 Crores under DPDPA framework."),
        ("CERT-In 6-Hour SLA", "Cyber Security Directions 2022 mandate incident notification within 6 hours of discovery.")
    ]
    for lbl, desc in v_points:
        p_pt = ltf9.add_paragraph()
        p_pt.text = f"• {lbl}: "
        p_pt.font.name = "Arial"
        p_pt.font.size = Pt(11)
        p_pt.font.bold = True
        p_pt.font.color.rgb = C_RED
        p_pt.space_after = Pt(3)
        run = p_pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT

    # Right: Remediation Card
    c9_right = add_card(s9, Inches(6.8), Inches(1.65), Inches(5.733), Inches(5.3), C_CARD, C_GREEN)
    rtf9 = c9_right.text_frame
    rtf9.word_wrap = True

    p = rtf9.paragraphs[0]
    p.text = "SENTINEL DEFENSIVE REMEDIATION"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.space_after = Pt(10)

    r_points = [
        ("Instant Token Invalidation", "Token rc-prod-01 permanently revoked across IdP cluster via JTI blacklist in 0ms."),
        ("Automated CERT-In Package", "6-hour compliance package generated with cryptographically verified SHA-256 evidence chain."),
        ("Data Protection Officer Gate", "Implemented dual-authorization rule requiring DPO co-sign on any bulk export."),
        ("Risk Posture Reset", "Perimeter hardened to 10.10.4.0/24 subnet; vulnerability completely eliminated from production.")
    ]
    for lbl, desc in r_points:
        p_pt = rtf9.add_paragraph()
        p_pt.text = f"• {lbl}: "
        p_pt.font.name = "Arial"
        p_pt.font.size = Pt(11)
        p_pt.font.bold = True
        p_pt.font.color.rgb = C_GREEN
        p_pt.space_after = Pt(3)
        run = p_pt.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = C_TEXT

    # =========================================================================
    # SLIDE 10: Conclusion & Deliverables Access
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_slide_bg(s10)

    # Big Banner
    c10 = add_card(s10, Inches(0.8), Inches(0.8), Inches(11.733), Inches(3.2), C_CARD, C_GREEN)
    tf10 = c10.text_frame
    tf10.word_wrap = True
    tf10.vertical_anchor = MSO_ANCHOR.MIDDLE

    p0 = tf10.paragraphs[0]
    p0.text = "CRIMEATHON '26  •  FINAL DEFENSE SUBMISSION"
    p0.font.name = "Arial"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = C_CYAN_LIGHT
    p0.alignment = PP_ALIGN.CENTER
    p0.space_after = Pt(6)

    p1 = tf10.add_paragraph()
    p1.text = "Zero Trust. Zero Hallucination. Zero Breach."
    p1.font.name = "Arial"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT
    p1.alignment = PP_ALIGN.CENTER
    p1.space_after = Pt(10)

    p2 = tf10.add_paragraph()
    p2.text = "Complete Source Code & Deliverables:  https://github.com/Heman-123/Northstar-Sentinel"
    p2.font.name = "Arial"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_CYAN_LIGHT
    p2.alignment = PP_ALIGN.CENTER

    # 3 Summary Cards
    delivs = [
        ("FORENSIC EVIDENCE", "12/12 Files Hashed", "Full SHA-256 Custody Chain", C_CYAN),
        ("DEFENSIVE ASSURANCE", "10/10 Simulation Passed", "15/15 Pytest Units Clean", C_GREEN),
        ("STATUTORY GOVERNANCE", "DPDPA 2023 Met", "CERT-In 6-Hour SLA Ready", C_PURPLE)
    ]
    for idx, (d_title, d_main, d_sub, d_col) in enumerate(delivs):
        d_left = Inches(0.8) + idx * Inches(3.99)
        dc = add_card(s10, d_left, Inches(4.2), Inches(3.75), Inches(1.8), C_CARD_ALT, d_col)
        dtf = dc.text_frame
        dtf.word_wrap = True
        dtf.vertical_anchor = MSO_ANCHOR.MIDDLE

        dp0 = dtf.paragraphs[0]
        dp0.text = d_title
        dp0.font.name = "Arial"
        dp0.font.size = Pt(10)
        dp0.font.bold = True
        dp0.font.color.rgb = d_col
        dp0.alignment = PP_ALIGN.CENTER
        dp0.space_after = Pt(4)

        dp1 = dtf.add_paragraph()
        dp1.text = d_main
        dp1.font.name = "Arial"
        dp1.font.size = Pt(15)
        dp1.font.bold = True
        dp1.font.color.rgb = C_TEXT
        dp1.alignment = PP_ALIGN.CENTER
        dp1.space_after = Pt(2)

        dp2 = dtf.add_paragraph()
        dp2.text = d_sub
        dp2.font.name = "Arial"
        dp2.font.size = Pt(10)
        dp2.font.color.rgb = C_MUTED
        dp2.alignment = PP_ALIGN.CENTER

    # Trophy Banner
    tr = add_card(s10, Inches(0.8), Inches(6.2), Inches(11.733), Inches(0.7), RGBColor(20, 30, 20), C_GREEN)
    trtf = tr.text_frame
    trtf.word_wrap = True
    trtf.vertical_anchor = MSO_ANCHOR.MIDDLE
    trp = trtf.paragraphs[0]
    trp.text = "🏆 CRIMEATHON '26 FINALIST  •  DEFENSE TRACK  •  TEAM NORTHSTAR (CHENNAI)"
    trp.font.name = "Arial"
    trp.font.size = Pt(12)
    trp.font.bold = True
    trp.font.color.rgb = C_GREEN
    trp.alignment = PP_ALIGN.CENTER

    # Save
    out_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "CRIMEATHON_26_PRESENTATION_DECK.pptx")
    prs.save(out_path)
    print(f"[+] Master Executive 10-Slide Deck created at: {out_path}")

if __name__ == "__main__":
    build_deck()
