export const INCIDENT_METRICS = {
  caseFile: "NS-26-014",
  organization: "Northstar Skills Academy Pvt. Ltd.",
  location: "Chennai, India",
  incidentDate: "2026-10-12",
  incidentWindow: "03:15:55 IST – 03:25:00 IST (9m 5s)",
  totalRecordsImpacted: 2300,
  dataEgressTotalBytes: 972400,
  latencySpikePeakMs: 8420,
  externalAttackerIP: "203.0.113.77",
  legitimateConnectorIP: "10.10.4.12",
  compromisedIdentity: "svc_rollcall (rollcall-prod)",
  stagedBucketFile: "campusvault-exports/learner-exports/learners-20261012.csv",
  chainOfCustodyVerified: "12 / 12 Evidence Files (100% Integrity)"
};

export const EVIDENCE_MANIFEST = [
  { id: "E01", name: "E01_Authentication_Logs.csv", sha256: "a4f89d3c52e670bb4e1898e3646f9035e408ec25fbb91490cc959a4beeb7ff2e", size: "1,248 bytes", records: 14, status: "VERIFIED" },
  { id: "E02", name: "E02_ClassBridge_Audit_Logs.csv", sha256: "71c0bd63d08595a09289de68ba60be2d5ebfe6caeeeb600021c33be85e94b150", size: "892 bytes", records: 7, status: "VERIFIED" },
  { id: "E03", name: "E03_API_Gateway_Logs.csv", sha256: "df2614b10b48455fa98d0f1eb73fcece9c22883ef4b14241e7d23d8c3fc3b8a1", size: "975 bytes", records: 7, status: "VERIFIED" },
  { id: "E04", name: "E04_CampusVault_Audit_Logs.csv", sha256: "17242866c1b3f7bf270ee29c5fc04fc6f927e1f4228c2901a0db060c4fb315ff", size: "640 bytes", records: 5, status: "VERIFIED" },
  { id: "E05", name: "E05_Integration_Register.csv", sha256: "5cb63db91ecdb080825f8ceb09efb4b0053a47926b010c7104b2c1f96ba535d4", size: "480 bytes", records: 3, status: "VERIFIED" },
  { id: "E06", name: "E06_HelpDesk_Tickets.csv", sha256: "983dce31be5d76161c56b7c53e0202eef5a0dbdce01a88df5e8c17ae87b1c430", size: "820 bytes", records: 4, status: "VERIFIED" },
  { id: "E07", name: "E07_Staff_and_Service_Account_Register.csv", sha256: "67df8155bb9e96e7ef15f9b4c09d5eb64ea20f8c2ce67448df7408f654b4231b", size: "612 bytes", records: 6, status: "VERIFIED" },
  { id: "E08", name: "E08_Information_Security_Policy_Extract.txt", sha256: "8e95085e17e47a27453147d3c52e850fa7dbb1f496155981316b2512cc7d14fa", size: "1,150 bytes", records: 4, status: "VERIFIED" },
  { id: "E09", name: "E09_Network_Observations.csv", sha256: "3295e8fb855848bbdc4993189da152cf7fae69e46a781b0a50153ef69b61d2d3", size: "490 bytes", records: 3, status: "VERIFIED" },
  { id: "E10", name: "E10_Vendor_And_Internal_Communications.json", sha256: "c53051a877ff4da6bce0e4b85da812f865f126da3303c734914c810d291e6c38", size: "930 bytes", records: 2, status: "VERIFIED" },
  { id: "E11", name: "E11_Additional_Configuration_Audit.csv", sha256: "d5351a44e59048f764a85faec0c4767104b2b3a1a9e887f4339e1a53b0185122", size: "580 bytes", records: 4, status: "VERIFIED" },
  { id: "E12", name: "E12_Incident_Response_Note.txt", sha256: "e0995166fcf8fa976189bb52554e19036f112e4b52c0021bb8a4b6b61877916c", size: "890 bytes", records: 3, status: "VERIFIED" }
];

export const TIMELINE_EVENTS = [
  {
    time: "03:15:55 IST",
    source: "Network Perimeter (E09)",
    id: "N001",
    actor: "External Flow",
    action: "TCP SYN/ACK Ingress",
    endpoint: "10.10.1.100:443",
    ip: "203.0.113.77",
    badge: "ANOMALOUS_INGRESS",
    badgeColor: "rose",
    details: "First network connection established from unrecognized external IP 203.0.113.77."
  },
  {
    time: "03:16:32 IST",
    source: "Northstar Identity (E01)",
    id: "A011",
    actor: "svc_rollcall",
    action: "identity.authenticate",
    endpoint: "auth_service",
    ip: "203.0.113.77",
    badge: "AUTHENTICATION_OK",
    badgeColor: "amber",
    details: "RollCall vendor machine service identity authenticates using static API_KEY from external IP."
  },
  {
    time: "03:16:35 IST",
    source: "Config Management (E11)",
    id: "CHG-882",
    actor: "svc_rollcall",
    action: "credential_config_read",
    endpoint: "integration_settings/rollcall",
    ip: "203.0.113.77",
    badge: "CONFIG_RECON",
    badgeColor: "rose",
    details: "Integration configuration inspected via API 5 seconds before scraping operations commenced."
  },
  {
    time: "03:16:40 IST",
    source: "API Gateway (E03)",
    id: "R003",
    actor: "rollcall-prod",
    action: "GET /v1/learners/search",
    endpoint: "/v1/learners/search",
    ip: "203.0.113.77",
    badge: "BULK_SEARCH",
    badgeColor: "rose",
    details: "Unthrottled bulk learner query returns 2,300 records. Latency spikes to 3,250ms."
  },
  {
    time: "03:17:09 IST",
    source: "API Gateway (E03)",
    id: "R004",
    actor: "rollcall-prod",
    action: "POST /v1/learners/export",
    endpoint: "/v1/learners/export",
    ip: "203.0.113.77",
    badge: "MASS_EXPORT",
    badgeColor: "rose",
    details: "Full database dump triggered. Latency spikes to 8,420ms. Least privilege violation."
  },
  {
    time: "03:17:35 IST",
    source: "CampusVault (E04)",
    id: "C001",
    actor: "svc_backend_worker",
    action: "object.put",
    endpoint: "campusvault-exports/learners-20261012.csv",
    ip: "10.10.2.50",
    badge: "DATA_STAGED",
    badgeColor: "amber",
    details: "Backend worker writes 486,200 bytes containing 2,300 learner PII records to cloud bucket."
  },
  {
    time: "03:18:50 IST",
    source: "API Gateway (E03)",
    id: "R005",
    actor: "rollcall-prod",
    action: "GET /v1/courses",
    endpoint: "/v1/courses",
    ip: "203.0.113.77",
    badge: "ENUMERATION",
    badgeColor: "blue",
    details: "Course catalog enumerated (42 courses)."
  },
  {
    time: "03:19:20 IST",
    source: "API Gateway (E03)",
    id: "R006",
    actor: "rollcall-prod",
    action: "GET /v1/attendance/all",
    endpoint: "/v1/attendance/all",
    ip: "203.0.113.77",
    badge: "ATTENDANCE_SCRAPE",
    badgeColor: "amber",
    details: "2,300 attendance rows scraped (4.19 MB transferred)."
  },
  {
    time: "03:20:12 IST",
    source: "CampusVault (E04)",
    id: "C002",
    actor: "svc_rollcall",
    action: "object.list",
    endpoint: "campusvault-exports/learner-exports/",
    ip: "203.0.113.77",
    badge: "BUCKET_LIST",
    badgeColor: "amber",
    details: "Actor enumerates files in cloud export repository to locate the newly generated file."
  },
  {
    time: "03:21:03 IST",
    source: "CampusVault (E04)",
    id: "C003",
    actor: "svc_rollcall",
    action: "object.get (Exfiltration 1)",
    endpoint: "learners-20261012.csv",
    ip: "203.0.113.77",
    badge: "DATA_EGRESS_1",
    badgeColor: "rose",
    details: "First download of staged student database (486,200 bytes egressed to external IP)."
  },
  {
    time: "03:24:48 IST",
    source: "CampusVault (E04)",
    id: "C004",
    actor: "svc_rollcall",
    action: "object.get (Exfiltration 2)",
    endpoint: "learners-20261012.csv",
    ip: "203.0.113.77",
    badge: "DATA_EGRESS_2",
    badgeColor: "rose",
    details: "Second download of staged export file (486,200 bytes). Cumulative egress: 972,400 bytes."
  },
  {
    time: "03:25:00 IST",
    source: "Network Perimeter (E09)",
    id: "N002",
    actor: "Legitimate Connector",
    action: "TCP SYN/ACK Ingress",
    endpoint: "10.10.1.100:443",
    ip: "10.10.4.12",
    badge: "NORMAL_RESUMPTION",
    badgeColor: "emerald",
    details: "Scheduled vendor connector heartbeat resumes from legitimate internal IP 10.10.4.12."
  }
];

export const DETECTION_RULES = [
  {
    id: "DET-001",
    title: "Unrecognized Ingress Source IP for Vendor Service Account",
    severity: "CRITICAL",
    confidence: "HIGH",
    triageScore: 98.0,
    tier: "P1 - IMMEDIATE_ACTION",
    mitre: "T1078.004",
    owasp: "API2:2023",
    evidence: ["E01:A011", "E01:A012", "E01:A013", "E09:N001"],
    defense: "Enforce API Gateway CIDR whitelisting pinning rollcall-prod exclusively to 10.10.4.12."
  },
  {
    id: "DET-002",
    title: "Architectural Privilege Creep: Excessive Integration Scopes",
    severity: "HIGH",
    confidence: "HIGH",
    triageScore: 83.0,
    tier: "P2 - HIGH_PRIORITY",
    mitre: "T1098",
    owasp: "API1:2023",
    evidence: ["E05:INT-01", "E08:Sec4.2"],
    defense: "Implement fine-grained OAuth2 scope restriction limiting RollCall strictly to attendance.sync."
  },
  {
    id: "DET-003",
    title: "Unthrottled Bulk Learner PII Data Acquisition",
    severity: "CRITICAL",
    confidence: "HIGH",
    triageScore: 98.0,
    tier: "P1 - IMMEDIATE_ACTION",
    mitre: "T1530",
    owasp: "API4:2023",
    evidence: ["E02:P003", "E02:P004", "E03:R003", "E03:R004"],
    defense: "Deploy token-bucket rate limiting (max 50 req/min) and hard pagination limits (50 rows/page)."
  },
  {
    id: "DET-004",
    title: "Perpetual Production Credential with Indefinite Validity",
    severity: "HIGH",
    confidence: "HIGH",
    triageScore: 83.0,
    tier: "P2 - HIGH_PRIORITY",
    mitre: "T1552.001",
    owasp: "API2:2023",
    evidence: ["E05:INT-01", "E08:Sec4.1", "E12:Section1"],
    defense: "Deploy HashiCorp Vault / AWS Secrets Manager enforcing mandatory 30-day automated secret rotation."
  },
  {
    id: "DET-005",
    title: "Unrestricted Network Perimeter Policy for External Integration",
    severity: "HIGH",
    confidence: "HIGH",
    triageScore: 83.0,
    tier: "P2 - HIGH_PRIORITY",
    mitre: "T1190",
    owasp: "API2:2023",
    evidence: ["E05:INT-01", "E08:Sec4.2"],
    defense: "Mandate IP whitelisting in integration register as a strict deployment gating condition."
  },
  {
    id: "DET-006",
    title: "Configuration Read Invocation on Secret Settings Preceding Extraction",
    severity: "HIGH",
    confidence: "HIGH",
    triageScore: 83.0,
    tier: "P2 - HIGH_PRIORITY",
    mitre: "T1087 / T1552",
    owasp: "API7:2023",
    defense: "Audit and mask configuration endpoints; require step-up MFA authorization to view secrets."
  },
  {
    id: "DET-007",
    title: "Staged Learner Export Object Retrieval from Cloud Storage",
    severity: "CRITICAL",
    confidence: "HIGH",
    triageScore: 98.0,
    tier: "P1 - IMMEDIATE_ACTION",
    mitre: "T1567",
    owasp: "API1:2023",
    evidence: ["E04:C003", "E04:C004"],
    defense: "Block external GET access to export buckets; require short-lived pre-signed URLs (15m TTL)."
  },
  {
    id: "DET-008",
    title: "Dormant Terminated Account Post-Offboarding Successful Authentication",
    severity: "HIGH",
    confidence: "HIGH",
    triageScore: 83.0,
    tier: "P2 - HIGH_PRIORITY",
    mitre: "T1078.002",
    owasp: "API2:2023",
    evidence: ["E01:A006", "E07:USR-04", "E08:Sec8.2"],
    defense: "Implement automated HR-to-IdP SCIM synchronization for immediate deprovisioning on termination."
  },
  {
    id: "DET-009",
    title: "Unapproved Bulk Learner Data Export (Missing DPO/Business Justification)",
    severity: "HIGH",
    confidence: "HIGH",
    triageScore: 83.0,
    tier: "P2 - HIGH_PRIORITY",
    mitre: "T1560",
    owasp: "API1:2023",
    evidence: ["E06:HD-1062", "E06:HD-1069", "E08:Sec5.3", "E10:VND-221"],
    defense: "Enforce Two-Man Rule: Bulk exports require asynchronous DPO cryptographic signing token."
  },
  {
    id: "DET-010",
    title: "Duplicate / Repeated Retrieval of Sensitive Staged Export",
    severity: "MEDIUM",
    confidence: "HIGH",
    triageScore: 68.0,
    tier: "P3 - MEDIUM_PRIORITY",
    mitre: "T1567.002",
    owasp: "API1:2023",
    evidence: ["E04:C003", "E04:C004"],
    defense: "Enforce One-Time-Download links that auto-delete after the first successful byte retrieval."
  }
];

export const EPISTEMIC_MATRIX = {
  confirmedFacts: [
    { id: "FACT-1", claim: "External IP 203.0.113.77 connected to Gateway at 03:15:55 IST.", citation: "E09:N001" },
    { id: "FACT-2", claim: "Machine identity svc_rollcall authenticated 3 times from 203.0.113.77.", citation: "E01:A011, A012, A013" },
    { id: "FACT-3", claim: "Configuration audit logged credential_config_read from 203.0.113.77 at 03:16:35 IST.", citation: "E11:CHG-882" },
    { id: "FACT-4", claim: "rollcall-prod queried 2,300 learners (R003) and executed mass export (R004).", citation: "E03:R003, R004; E02:P003, P004" },
    { id: "FACT-5", claim: "learners-20261012.csv created in CampusVault and downloaded twice (972.4 KB total).", citation: "E04:C001, C003, C004" },
    { id: "FACT-6", claim: "Integration Register INT-01 specifies Expiry: Never, IP Restriction: None.", citation: "E05:INT-01" },
    { id: "FACT-7", claim: "former.ajay authenticated successfully on Oct 9, 9 days post-termination date.", citation: "E01:A006; E07:USR-04" }
  ],
  supportedInferences: [
    { id: "INF-1", claim: "Credential was acquired via HD-1058 support screenshot disclosure or CHG-882 config read.", citation: "E06:HD-1058, E11:CHG-882, E12" },
    { id: "INF-2", claim: "Portal response latency spike (8,420ms) was caused by unthrottled table scan of 2,300 records.", citation: "E03:R004, E02:P004" },
    { id: "INF-3", claim: "RollCall attendance sync delay was caused by API thread exhaustion during mass export.", citation: "E06:HD-1041, E03:R004" }
  ],
  epistemicUnknowns: [
    { id: "UNK-1", claim: "Physical identity, real name, or location of human operator behind IP 203.0.113.77.", citation: "E12:Section2" },
    { id: "UNK-2", claim: "Whether two downloads represent two distinct copies or an interrupted/resumed stream.", citation: "E04:C003, C004" },
    { id: "UNK-3", claim: "Whether the downloaded learner data was stored, published, or distributed onward.", citation: "E12" },
    { id: "UNK-4", claim: "Any causal or technical link between former.ajay's login and the RollCall incident.", citation: "Forensic separation" }
  ]
};

export const SIMULATION_SCENARIOS = [
  {
    id: "SCENARIO_ATTACK_1",
    name: "External IP Replay Attack",
    description: "Adversary uses stolen static token from external IP 203.0.113.77 to call /v1/attendance/sync.",
    client: "rollcall-prod",
    sourceIp: "203.0.113.77",
    endpoint: "/v1/attendance/sync",
    dpoToken: null,
    vulnerableResult: { status: 200, label: "PERMITTED (VULNERABILITY EXPOSED)", color: "rose", desc: "Gateway accepts valid key without checking source IP." },
    hardenedResult: { status: 403, label: "BLOCKED: UNAUTHORIZED_SOURCE_IP", color: "emerald", desc: "Sentinel Zero-Trust PEP blocks non-whitelisted IP." }
  },
  {
    id: "SCENARIO_ATTACK_AUTOBAN",
    name: "Repeat Threat Actor & Auto-Shunning (Active Ban)",
    description: "Adversary repeatedly attempts malicious requests from suspicious IP. Triggers Sentinel's Adaptive Threat Auto-Banning.",
    client: "rollcall-prod",
    sourceIp: "198.51.100.99",
    endpoint: "/v1/attendance/sync",
    dpoToken: null,
    vulnerableResult: { status: 200, label: "PERMITTED (NO REPUTATION / BAN ENFORCEMENT)", color: "rose", desc: "Vulnerable server continues answering repeat unauthorized requests." },
    hardenedResult: { status: 403, label: "BLOCKED: ADAPTIVE_THREAT_AUTO_SHUNNING (AUTO-BANNED)", color: "emerald", desc: "Sentinel automatically quarantined the IP. All connections dropped at Layer 0." }
  },
  {
    id: "SCENARIO_ATTACK_2",
    name: "Excessive Scope Abuse (Bulk Export)",
    description: "RollCall token attempts POST /v1/learners/export to dump 2,300 student records.",
    client: "rollcall-prod",
    sourceIp: "10.10.4.12",
    endpoint: "/v1/learners/export",
    dpoToken: null,
    vulnerableResult: { status: 200, label: "PERMITTED (MASS EXFILTRATION)", color: "rose", desc: "ClassBridge generates dump despite out-of-scope request." },
    hardenedResult: { status: 403, label: "BLOCKED: PRIVILEGE_CREEP_BLOCKED", color: "emerald", desc: "Scope Gate restricts client rollcall-prod strictly to attendance:sync." }
  },
  {
    id: "SCENARIO_ATTACK_3",
    name: "Automated Scraping / Burst Denial-of-Service",
    description: "Adversary fires rapid burst of 15 queries in 10 seconds to scrape learner search API.",
    client: "rollcall-prod",
    sourceIp: "10.10.4.12",
    endpoint: "/v1/learners/search",
    dpoToken: null,
    vulnerableResult: { status: 200, label: "PERMITTED (DATABASE EXHAUSTION)", color: "rose", desc: "Queries execute unthrottled, portal latency spikes to 8.4s." },
    hardenedResult: { status: 429, label: "BLOCKED: RATE_LIMIT_EXCEEDED", color: "emerald", desc: "Token Bucket limiter clamps burst at max 10 req/min." }
  },
  {
    id: "SCENARIO_LEGITIMATE",
    name: "Legitimate Attendance Synchronization",
    description: "RollCall connector node 10.10.4.12 synchronizes daily attendance records.",
    client: "rollcall-prod",
    sourceIp: "10.10.4.12",
    endpoint: "/v1/attendance/sync",
    dpoToken: null,
    vulnerableResult: { status: 200, label: "PERMITTED (NORMAL)", color: "emerald", desc: "Request succeeds." },
    hardenedResult: { status: 200, label: "PERMITTED (AUTHORIZED BY SENTINEL)", color: "emerald", desc: "IP verified, scope validated, within rate limit." }
  }
];
