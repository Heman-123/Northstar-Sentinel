#!/usr/bin/env python3
"""
Northstar Sentinel - Stage 5: Explainable Risk Scoring & Prioritization
Evaluates detections using decoupled dimensions:
  1. Technical/Business Impact (Severity: 1 to 10)
  2. Evidentiary Grounding (Confidence: 1 to 10)
Produces a prioritized Risk Matrix without conflating impact with probability.
"""

import os
import json

PROCESSED_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")

SEVERITY_WEIGHTS = {
    "CRITICAL": 10.0,
    "HIGH": 7.5,
    "MEDIUM": 5.0,
    "LOW": 2.5
}

CONFIDENCE_WEIGHTS = {
    "HIGH": 9.5,
    "MEDIUM": 6.5,
    "LOW": 3.5
}

def calculate_risk_scores():
    print("[*] Northstar Sentinel Stage 5: Computing Decoupled Risk & Priority Scores...")
    det_path = os.path.join(PROCESSED_DATA_DIR, "detection_findings.json")
    
    with open(det_path, "r", encoding="utf-8") as f:
        detections = json.load(f)

    scored_findings = []

    for d in detections:
        sev_label = d.get("severity", "MEDIUM")
        conf_label = d.get("confidence", "MEDIUM")
        
        sev_score = SEVERITY_WEIGHTS.get(sev_label, 5.0)
        conf_score = CONFIDENCE_WEIGHTS.get(conf_label, 5.0)
        
        # Composite Triage Index (1-100 scale for security triage prioritization)
        # Note: Clearly designated as a Triage Index, NOT a statistical probability
        triage_index = round((sev_score * 0.6 + conf_score * 0.4) * 10, 1)

        if triage_index >= 85:
            priority_tier = "P1 - IMMEDIATE_ACTION_REQUIRED"
        elif triage_index >= 70:
            priority_tier = "P2 - HIGH_PRIORITY_REMEDIATION"
        elif triage_index >= 50:
            priority_tier = "P3 - MEDIUM_DEFENSIVE_HARDENING"
        else:
            priority_tier = "P4 - INFORMATIONAL_AUDIT"

        scored_item = {
            "detection_id": d["detection_id"],
            "title": d["title"],
            "severity_label": sev_label,
            "severity_score": sev_score,
            "confidence_label": conf_label,
            "confidence_score": conf_score,
            "triage_index": triage_index,
            "priority_tier": priority_tier,
            "mitre_technique": d.get("mitre_technique", "N/A"),
            "owasp_api": d.get("owasp_api", "N/A"),
            "evidence_references": d.get("evidence_references", []),
            "flagged_events": d.get("flagged_events", []),
            "recommended_defense": d.get("recommended_defense", "")
        }
        scored_findings.append(scored_item)

    # Sort descending by triage index
    scored_findings.sort(key=lambda x: x["triage_index"], reverse=True)

    output_path = os.path.join(PROCESSED_DATA_DIR, "prioritized_risk_matrix.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scored_findings, f, indent=2)

    print(f"[+] Risk scoring complete. {len(scored_findings)} detections prioritized.")
    for s in scored_findings:
        print(f"    - [{s['detection_id']}] {s['priority_tier']} (Index: {s['triage_index']}) | {s['title']}")
    print(f"[+] Output saved to: {output_path}\n")
    return scored_findings

if __name__ == "__main__":
    calculate_risk_scores()
