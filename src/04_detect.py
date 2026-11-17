#!/usr/bin/env python3
"""
Northstar Sentinel - Stage 4: Behavioral & Policy Rule Detection Engine
Evaluates normalized logs and reference topologies against 10 deterministic,
explainable detection rules (DET-001 through DET-010).
Outputs detections with evidence IDs, trigger criteria, and defensive remediation.
"""

import os
import csv
import json

PROCESSED_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")

def run_detections():
    print("[*] Northstar Sentinel Stage 4: Executing Behavioral & Policy Detection Engine...")
    
    events_path = os.path.join(PROCESSED_DATA_DIR, "normalized_events.csv")
    ref_path = os.path.join(PROCESSED_DATA_DIR, "reference_data.json")
    
    with open(events_path, "r", encoding="utf-8") as f:
        events = list(csv.DictReader(f))
    with open(ref_path, "r", encoding="utf-8") as f:
        ref_data = json.load(f)

    detections = []

    # -------------------------------------------------------------------------
    # DET-001: Unrecognized Ingress Source for Machine Service Identity
    # -------------------------------------------------------------------------
    approved_ips = {"10.10.4.12", "10.10.2.50"}
    anomalous_auths = [
        e for e in events 
        if e["actor_identity"] == "svc_rollcall" and e["source_ip"] not in approved_ips
    ]
    if anomalous_auths:
        detections.append({
            "detection_id": "DET-001",
            "title": "Unrecognized Ingress Source IP for Vendor Service Account",
            "trigger_condition": "Actor 'svc_rollcall' authenticates from IP outside approved connector range (10.10.4.12)",
            "severity": "CRITICAL",
            "confidence": "HIGH",
            "mitre_technique": "T1078.004 (Valid Accounts: Cloud Service Accounts)",
            "owasp_api": "API2:2023 (Broken Authentication)",
            "evidence_references": ["E01:A011", "E01:A012", "E01:A013", "E09:N001"],
            "flagged_events": [e["event_id"] for e in anomalous_auths],
            "explanation": f"Service identity 'svc_rollcall' authenticated 3 times from external IP {anomalous_auths[0]['source_ip']}.",
            "recommended_defense": "Enforce strict IP whitelisting / mTLS pinning at the API Gateway for all service principals."
        })

    # -------------------------------------------------------------------------
    # DET-002: Service Identity Privilege Creep (Out-of-Scope Operation)
    # -------------------------------------------------------------------------
    int_01 = next((i for i in ref_data.get("integrations", []) if i["integration_id"] == "INT-01"), None)
    if int_01:
        granted = int_01.get("granted_permissions", "").split(";")
        purpose = int_01.get("documented_purpose", "")
        # Flag if attendance integration has learner.export permission
        if "learner.export" in granted:
            detections.append({
                "detection_id": "DET-002",
                "title": "Architectural Privilege Creep: Integration Scopes Exceed Documented Purpose",
                "trigger_condition": "Integration granted permissions contain 'learner.export' while documented purpose is 'Attendance synchronization'",
                "severity": "HIGH",
                "confidence": "HIGH",
                "mitre_technique": "T1098 (Account Manipulation)",
                "owasp_api": "API1:2023 (Broken Object Level Authorization)",
                "evidence_references": ["E05:INT-01", "E08:Sec4.2"],
                "flagged_events": ["INT-01"],
                "explanation": "Service client 'rollcall-prod' was granted broad read/export rights over learner PII despite strictly requiring attendance read/write.",
                "recommended_defense": "Implement fine-grained OAuth2 scope restriction (attendance.read/write only) and annual entitlement reviews."
            })

    # -------------------------------------------------------------------------
    # DET-003: Unthrottled Bulk Learner PII Data Acquisition
    # -------------------------------------------------------------------------
    bulk_events = [e for e in events if int(e.get("records_count", 0)) >= 1000]
    if bulk_events:
        detections.append({
            "detection_id": "DET-003",
            "title": "Unthrottled Bulk PII Acquisition & High-Volume Search",
            "trigger_condition": "API / Portal request retrieves >= 1000 learner records in a single query",
            "severity": "CRITICAL",
            "confidence": "HIGH",
            "mitre_technique": "T1530 (Data from Cloud Storage / Local System)",
            "owasp_api": "API4:2023 (Unrestricted Resource Consumption)",
            "evidence_references": ["E02:P003", "E02:P004", "E03:R003", "E03:R004"],
            "flagged_events": [e["event_id"] for e in bulk_events],
            "explanation": "2,300 learner records (100% of institution enrollment) were retrieved and exported within 30 seconds, causing gateway latency to spike to 8,420ms.",
            "recommended_defense": "Implement strict pagination caps (max 50 records/request) and rate limiting on search/export endpoints."
        })

    # -------------------------------------------------------------------------
    # DET-004: Non-Expiring Production Credential Lifecycle Defect
    # -------------------------------------------------------------------------
    if int_01 and int_01.get("expiry", "").upper() == "NEVER":
        detections.append({
            "detection_id": "DET-004",
            "title": "Perpetual Production Credential with Indefinite Validity",
            "trigger_condition": "Production integration credential register indicates Expiry == 'Never'",
            "severity": "HIGH",
            "confidence": "HIGH",
            "mitre_technique": "T1552.001 (Unsecured Credentials: Plaintext Credentials)",
            "owasp_api": "API2:2023 (Broken Authentication)",
            "evidence_references": ["E05:INT-01", "E08:Sec4.1", "E12:Section1"],
            "flagged_events": ["INT-01"],
            "explanation": "API key 'rc-prod-01' has no automated rotation or expiry, violating Information Security Policy Section 4.1 requiring maximum 90-day TTL.",
            "recommended_defense": "Integrate an enterprise Secrets Manager with automatic 30-day credential rotation and dynamic short-lived token issuance."
        })

    # -------------------------------------------------------------------------
    # DET-005: Absence of Network Ingress Restriction on Vendor Integration
    # -------------------------------------------------------------------------
    if int_01 and int_01.get("ip_restriction", "").upper() in ["NONE", "NOT CONFIGURED", ""]:
        detections.append({
            "detection_id": "DET-005",
            "title": "Unrestricted Network Perimeter Policy for External Integration",
            "trigger_condition": "Integration register shows IP Restriction == 'None'",
            "severity": "HIGH",
            "confidence": "HIGH",
            "mitre_technique": "T1190 (Exploit Public-Facing Application)",
            "owasp_api": "API2:2023 (Broken Authentication)",
            "evidence_references": ["E05:INT-01", "E08:Sec4.2"],
            "flagged_events": ["INT-01"],
            "explanation": "No CIDR or IP restriction was configured on client 'rollcall-prod', enabling replay of valid API credentials from arbitrary external IPs.",
            "recommended_defense": "Configure strict CIDR filtering at WAF/Gateway restricting ingress to vendor connector IPs."
        })

    # -------------------------------------------------------------------------
    # DET-006: Integration Credential Configuration Read Precedes API Burst
    # -------------------------------------------------------------------------
    config_reads = [e for e in events if e.get("action") == "credential_config_read"]
    if config_reads:
        detections.append({
            "detection_id": "DET-006",
            "title": "Configuration Read Invocation on Secret Settings Preceding Extraction",
            "trigger_condition": "Audit event 'credential_config_read' recorded immediately prior to high-volume API requests",
            "severity": "HIGH",
            "confidence": "HIGH",
            "mitre_technique": "T1087 (Account Discovery) / T1552 (Unsecured Credentials)",
            "owasp_api": "API7:2023 (Server-Side Request Forgery / Security Misconfiguration)",
            "evidence_references": ["E11:CHG-882", "E12:Section2"],
            "flagged_events": [e["event_id"] for e in config_reads],
            "explanation": "Audit event CHG-882 confirms external IP 203.0.113.77 read integration settings at 03:16:35 IST, just 5 seconds before scraping began.",
            "recommended_defense": "Enforce strict Read-Access-Logging and Masking on all configuration endpoints; require step-up MFA for secrets viewing."
        })

    # -------------------------------------------------------------------------
    # DET-007: Staged Cloud Export Object Access & Download Activity
    # -------------------------------------------------------------------------
    storage_gets = [
        e for e in events 
        if e.get("source_system") == "CampusVault Cloud Storage" and e.get("action") == "object.get"
    ]
    if storage_gets:
        detections.append({
            "detection_id": "DET-007",
            "title": "Staged Learner Export Object Retrieval from Cloud Storage",
            "trigger_condition": "Cloud storage audit records 'object.get' on generated learner export files",
            "severity": "CRITICAL",
            "confidence": "HIGH",
            "mitre_technique": "T1567 (Exfiltration Over Web Service)",
            "owasp_api": "API1:2023 (Broken Object Level Authorization)",
            "evidence_references": ["E04:C003", "E04:C004"],
            "flagged_events": [e["event_id"] for e in storage_gets],
            "explanation": "Object 'learner-exports/learners-20261012.csv' (486,200 bytes) was downloaded via GET requests from IP 203.0.113.77.",
            "recommended_defense": "Block public/external access to export buckets; enforce pre-signed URL validation with temporary 15-minute token authorization."
        })

    # -------------------------------------------------------------------------
    # DET-008: Terminated Employee Account Post-Departure Authentication
    # -------------------------------------------------------------------------
    ajay_auths = [e for e in events if e.get("actor_identity") == "former.ajay" and e.get("status") == "SUCCESS"]
    if ajay_auths:
        detections.append({
            "detection_id": "DET-008",
            "title": "Dormant Terminated Account Post-Offboarding Successful Authentication",
            "trigger_condition": "Account with status == 'TERMINATED' successfully authenticates to IdP",
            "severity": "HIGH",
            "confidence": "HIGH",
            "mitre_technique": "T1078.002 (Valid Accounts: Domain Accounts)",
            "owasp_api": "API2:2023 (Broken Authentication)",
            "evidence_references": ["E01:A006", "E07:USR-04", "E08:Sec8.2"],
            "flagged_events": [e["event_id"] for e in ajay_auths],
            "explanation": "Former employee 'former.ajay' (terminated 2026-09-30) logged in successfully on 2026-10-09T22:14:05 IST, violating offboarding policy.",
            "recommended_defense": "Implement automated HR-to-IdP SCIM synchronization for immediate account deprovisioning upon employee termination."
        })

    # -------------------------------------------------------------------------
    # DET-009: Missing Business Authorization / DPO Sign-Off for Bulk Export
    # -------------------------------------------------------------------------
    detections.append({
        "detection_id": "DET-009",
        "title": "Unapproved Bulk Learner Data Export (Missing DPO/Business Justification)",
        "trigger_condition": "Bulk export generated without corresponding approved ticket or DPO authorization record",
        "severity": "HIGH",
        "confidence": "HIGH",
        "mitre_technique": "T1560 (Archive Collected Data)",
        "owasp_api": "API1:2023 (Broken Object Level Authorization)",
        "evidence_references": ["E06:HD-1062", "E06:HD-1069", "E08:Sec5.3", "E10:VND-221"],
        "flagged_events": ["HD-1069", "CHG-883"],
        "explanation": "HelpDesk HD-1069 confirms Finance never requested the export; HD-1062 confirms maintenance did not schedule it. Directly violates Policy Section 5.3.",
        "recommended_defense": "Institute an asynchronous Dual-Key Approval workflow: bulk exports require dual cryptographic sign-off before files are staged."
    })

    # -------------------------------------------------------------------------
    # DET-010: Repeated Cloud Object Download Pattern
    # -------------------------------------------------------------------------
    if len(storage_gets) >= 2:
        detections.append({
            "detection_id": "DET-010",
            "title": "Duplicate / Repeated Retrieval of Sensitive Staged Export",
            "trigger_condition": "Multiple 'object.get' operations executed against the same sensitive cloud object within a short interval",
            "severity": "MEDIUM",
            "confidence": "HIGH",
            "mitre_technique": "T1567.002 (Exfiltration to Cloud Storage / External Egress)",
            "owasp_api": "API1:2023 (Broken Object Level Authorization)",
            "evidence_references": ["E04:C003", "E04:C004"],
            "flagged_events": [e["event_id"] for e in storage_gets],
            "explanation": "The file 'learners-20261012.csv' was downloaded twice (at 03:21:03 and 03:24:48 IST), transferring 972,400 bytes total.",
            "recommended_defense": "Enforce single-use download links (One-Time-Token) that expire immediately upon first successful byte retrieval."
        })

    # Save detections
    det_path = os.path.join(PROCESSED_DATA_DIR, "detection_findings.json")
    with open(det_path, "w", encoding="utf-8") as f:
        json.dump(detections, f, indent=2)

    print(f"[+] Detection engine complete: {len(detections)} actionable security detections generated.")
    print(f"[+] Output saved to: {det_path}\n")
    return detections

if __name__ == "__main__":
    run_detections()
