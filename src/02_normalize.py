#!/usr/bin/env python3
"""
Northstar Sentinel - Stage 2: Unified Semantic Event Normalizer (USEN)
Normalizes disparate log sources into a standardized, OCSF-aligned schema.
Preserves original timestamps, source fields, and timezone offsets (+05:30 IST).
"""

import os
import csv
import json
from datetime import datetime

RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")

def normalize_all_events():
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    normalized_events = []
    
    print("[*] Northstar Sentinel Stage 2: Normalizing Log Feeds into Common Event Schema...")

    # 1. E01 - Authentication Logs
    e01_path = os.path.join(RAW_DATA_DIR, "E01_Authentication_Logs.csv")
    with open(e01_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            normalized_events.append({
                "event_id": row["event_id"],
                "evidence_id": "E01",
                "timestamp": row["timestamp"],
                "source_system": "Northstar Identity",
                "actor_identity": row["identity"],
                "source_ip": row["source_ip"],
                "action": "identity.authenticate",
                "target_resource": "auth_service",
                "status": row["status"],
                "bytes": 0,
                "records_count": 1,
                "raw_details": json.dumps({"auth_method": row["auth_method"], "user_agent": row["user_agent"]})
            })

    # 2. E02 - ClassBridge Audit Logs
    e02_path = os.path.join(RAW_DATA_DIR, "E02_ClassBridge_Audit_Logs.csv")
    with open(e02_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            normalized_events.append({
                "event_id": row["audit_id"],
                "evidence_id": "E02",
                "timestamp": row["timestamp"],
                "source_system": "ClassBridge Portal",
                "actor_identity": row["actor_identity"],
                "source_ip": row["source_ip"],
                "action": row["action"],
                "target_resource": row["resource"],
                "status": row["status"],
                "bytes": 0,
                "records_count": int(row.get("records_impacted", 1)),
                "raw_details": json.dumps({"records_impacted": row["records_impacted"]})
            })

    # 3. E03 - API Gateway Logs
    e03_path = os.path.join(RAW_DATA_DIR, "E03_API_Gateway_Logs.csv")
    with open(e03_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            normalized_events.append({
                "event_id": row["request_id"],
                "evidence_id": "E03",
                "timestamp": row["timestamp"],
                "source_system": "API Gateway",
                "actor_identity": row["client_id"],
                "source_ip": row["source_ip"],
                "action": f"{row['method']} {row['path']}",
                "target_resource": row["path"],
                "status": f"HTTP_{row['status_code']}",
                "bytes": int(row.get("bytes_sent", 0)),
                "records_count": 0,
                "raw_details": json.dumps({
                    "api_key_id": row["api_key_id"],
                    "response_time_ms": row["response_time_ms"]
                })
            })

    # 4. E04 - CampusVault Audit Logs
    e04_path = os.path.join(RAW_DATA_DIR, "E04_CampusVault_Audit_Logs.csv")
    with open(e04_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            normalized_events.append({
                "event_id": row["event_id"],
                "evidence_id": "E04",
                "timestamp": row["timestamp"],
                "source_system": "CampusVault Cloud Storage",
                "actor_identity": row["actor_identity"],
                "source_ip": row["source_ip"],
                "action": row["action"],
                "target_resource": f"{row['bucket']}/{row['object_key']}",
                "status": f"HTTP_{row['http_status']}",
                "bytes": int(row.get("bytes_transferred", 0)),
                "records_count": 1 if row["action"] == "object.get" else 0,
                "raw_details": json.dumps({"bucket": row["bucket"], "object_key": row["object_key"]})
            })

    # 5. E09 - Network Observations
    e09_path = os.path.join(RAW_DATA_DIR, "E09_Network_Observations.csv")
    with open(e09_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            normalized_events.append({
                "event_id": row["obs_id"],
                "evidence_id": "E09",
                "timestamp": row["timestamp"],
                "source_system": "Network Perimeter Monitor",
                "actor_identity": "network_flow",
                "source_ip": row["source_ip"],
                "action": f"tcp_flow_{row['port']}",
                "target_resource": f"{row['destination_ip']}:{row['port']}",
                "status": row["flags"],
                "bytes": int(row.get("bytes_transferred", 0)),
                "records_count": 0,
                "raw_details": json.dumps({"notes": row["notes"], "protocol": row["protocol"]})
            })

    # 6. E11 - Additional Configuration Audit
    e11_path = os.path.join(RAW_DATA_DIR, "E11_Additional_Configuration_Audit.csv")
    with open(e11_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            normalized_events.append({
                "event_id": row["audit_id"],
                "evidence_id": "E11",
                "timestamp": row["timestamp"],
                "source_system": "Configuration Management",
                "actor_identity": row["actor"],
                "source_ip": row["source_ip"],
                "action": row["action"],
                "target_resource": row["target_entity"],
                "status": row["status"],
                "bytes": 0,
                "records_count": 0,
                "raw_details": json.dumps({"details": row["details"]})
            })

    # Sort normalized events chronologically
    normalized_events.sort(key=lambda x: x["timestamp"])

    # Write normalized events to CSV
    norm_csv_path = os.path.join(PROCESSED_DATA_DIR, "normalized_events.csv")
    fieldnames = [
        "event_id", "evidence_id", "timestamp", "source_system",
        "actor_identity", "source_ip", "action", "target_resource",
        "status", "bytes", "records_count", "raw_details"
    ]
    with open(norm_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(normalized_events)

    # Process and preserve reference context
    reference_data = {}
    
    # E05 Integrations
    with open(os.path.join(RAW_DATA_DIR, "E05_Integration_Register.csv"), "r", encoding="utf-8") as f:
        reference_data["integrations"] = list(csv.DictReader(f))
        
    # E07 Staff Register
    with open(os.path.join(RAW_DATA_DIR, "E07_Staff_and_Service_Account_Register.csv"), "r", encoding="utf-8") as f:
        reference_data["accounts"] = list(csv.DictReader(f))

    # E06 HelpDesk Tickets
    with open(os.path.join(RAW_DATA_DIR, "E06_HelpDesk_Tickets.csv"), "r", encoding="utf-8") as f:
        reference_data["tickets"] = list(csv.DictReader(f))

    # E10 Communications
    with open(os.path.join(RAW_DATA_DIR, "E10_Vendor_And_Internal_Communications.json"), "r", encoding="utf-8") as f:
        reference_data["communications"] = json.load(f).get("communications", [])

    ref_json_path = os.path.join(PROCESSED_DATA_DIR, "reference_data.json")
    with open(ref_json_path, "w", encoding="utf-8") as f:
        json.dump(reference_data, f, indent=2)

    print(f"[+] Normalization complete: {len(normalized_events)} unified events recorded.")
    print(f"[+] Output stored in: {norm_csv_path}")
    print(f"[+] Reference data cataloged in: {ref_json_path}\n")
    return normalized_events

if __name__ == "__main__":
    normalize_all_events()
