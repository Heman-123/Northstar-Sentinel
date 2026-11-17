#!/usr/bin/env python3
"""
Northstar Sentinel - Safe Local Demonstration Mock API Server with LIVE ATTACK TRACKING
Tracks live incoming attacks in real-time, logs security telemetry, enforces Zero-Trust PEP,
and exposes a /api/live-threats telemetry feed for SOC dashboards.
Binds strictly to 127.0.0.1:8765.
"""

import sys
import os
import time
import json
import argparse
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Import Zero-Trust Defense PEP
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from gateway_defense import ZeroTrustPolicyEnforcementPoint

PORT = 8765
HOST = "127.0.0.1"

# Shared in-memory and disk telemetry buffer
LIVE_TELEMETRY = []
TELEMETRY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    "data", "processed", "live_telemetry.json"
)

# Synthetic test database
SYNTHETIC_LEARNERS = [
    {"id": f"L-{i:04d}", "name": f"Synthetic Learner {i}", "course": "Cyber Defense 101", "status": "ACTIVE"}
    for i in range(1, 2301)
]

def record_telemetry(entry: dict):
    now = datetime.now()
    entry["logged_at"] = now.strftime("%H:%M:%S") + " IST"
    entry["epoch"] = time.time()
    LIVE_TELEMETRY.insert(0, entry)
    if len(LIVE_TELEMETRY) > 100:
        LIVE_TELEMETRY.pop()
    
    os.makedirs(os.path.dirname(TELEMETRY_FILE), exist_ok=True)
    try:
        with open(TELEMETRY_FILE, "w", encoding="utf-8") as f:
            json.dump(LIVE_TELEMETRY, f, indent=2)
    except Exception:
        pass

def make_handler(mode: str):
    pep = ZeroTrustPolicyEnforcementPoint()
    
    class MockAPIHandler(BaseHTTPRequestHandler):
        def _send_response_json(self, status_code: int, data: dict):
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.send_header("X-Security-Mode", mode.upper())
            self.send_header("X-Sentinel-PEP", "Active" if mode == "hardened" else "Bypassed")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()

        def do_GET(self):
            parsed_url = urllib.parse.urlparse(self.path)
            endpoint = parsed_url.path

            # Serve SOC Dashboard directly on browser load
            if endpoint in ["/", "/index.html", "/dashboard.html"]:
                root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                dash_path = os.path.join(root_dir, "dashboard.html")
                if os.path.exists(dash_path):
                    with open(dash_path, "rb") as f:
                        html_content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("Content-Length", str(len(html_content)))
                    self.end_headers()
                    self.wfile.write(html_content)
                    return

            # Expose live telemetry endpoint for the SOC dashboard
            if endpoint == "/api/live-threats":
                self._send_response_json(200, {
                    "server_mode": mode,
                    "total_intercepted": len(LIVE_TELEMETRY),
                    "events": LIVE_TELEMETRY
                })
                return

            client_id = self.headers.get("X-Client-ID", "anonymous")
            source_ip = self.headers.get("X-Forwarded-For", self.client_address[0])
            auth_token = self.headers.get("Authorization", "")
            dpo_token = self.headers.get("X-DPO-Approval-Token")

            # 1. Authentication Check
            if not auth_token.startswith("Bearer demo-"):
                record_telemetry({
                    "action": f"GET {endpoint}",
                    "client_id": client_id,
                    "source_ip": source_ip,
                    "decision": "BLOCKED",
                    "status_code": 401,
                    "threat_type": "UNAUTHENTICATED_ACCESS_ATTEMPT",
                    "security_layer": "AUTHENTICATION_GATE",
                    "reason": "Missing or invalid Bearer token"
                })
                self._send_response_json(401, {"error": "UNAUTHORIZED", "message": "Missing or invalid bearer token"})
                return

            # 2. Hardened Mode Defense Evaluation
            if mode == "hardened":
                evaluation = pep.inspect_request(client_id, source_ip, endpoint, dpo_token)
                if evaluation["decision"] != "ALLOW":
                    record_telemetry({
                        "action": f"GET {endpoint}",
                        "client_id": client_id,
                        "source_ip": source_ip,
                        "decision": "BLOCKED",
                        "status_code": evaluation["status_code"],
                        "threat_type": evaluation["security_layer"],
                        "security_layer": evaluation["security_layer"],
                        "reason": evaluation["reason"]
                    })
                    print(f" [!] LIVE ATTACK INTERCEPTED: {endpoint} from {source_ip} -> {evaluation['security_layer']}")
                    self._send_response_json(evaluation["status_code"], {
                        "status": "DENIED",
                        "error": evaluation["security_layer"],
                        "details": evaluation["reason"]
                    })
                    return

            # If Vulnerable mode or Authorized
            record_telemetry({
                "action": f"GET {endpoint}",
                "client_id": client_id,
                "source_ip": source_ip,
                "decision": "PERMITTED",
                "status_code": 200,
                "threat_type": "LEGITIMATE_OR_UNCHECKED" if mode == "hardened" else "VULNERABILITY_EXPOSED",
                "security_layer": "ALLOW_GATE",
                "reason": "Request allowed"
            })

            if endpoint in ["/v1/attendance", "/v1/attendance/sync", "/v1/attendance/all"]:
                self._send_response_json(200, {
                    "status": "SUCCESS",
                    "operation": "attendance_sync",
                    "records_synced": 120,
                    "mode": mode
                })
            elif endpoint == "/v1/learners/search":
                self._send_response_json(200, {
                    "status": "SUCCESS",
                    "total_learners": len(SYNTHETIC_LEARNERS),
                    "sample": SYNTHETIC_LEARNERS[:5],
                    "warning": "VULNERABILITY_EXPOSED: Bulk PII scraped without authorization" if mode == "vulnerable" else "Hardened"
                })
            elif endpoint == "/v1/courses":
                self._send_response_json(200, {"status": "SUCCESS", "courses_count": 42})
            else:
                self._send_response_json(404, {"error": "NOT_FOUND", "endpoint": endpoint})

        def do_POST(self):
            parsed_url = urllib.parse.urlparse(self.path)
            endpoint = parsed_url.path
            client_id = self.headers.get("X-Client-ID", "anonymous")
            source_ip = self.headers.get("X-Forwarded-For", self.client_address[0])
            auth_token = self.headers.get("Authorization", "")
            dpo_token = self.headers.get("X-DPO-Approval-Token")

            if not auth_token.startswith("Bearer demo-"):
                record_telemetry({
                    "action": f"POST {endpoint}",
                    "client_id": client_id,
                    "source_ip": source_ip,
                    "decision": "BLOCKED",
                    "status_code": 401,
                    "threat_type": "UNAUTHENTICATED_ACCESS_ATTEMPT",
                    "security_layer": "AUTHENTICATION_GATE",
                    "reason": "Missing or invalid bearer token"
                })
                self._send_response_json(401, {"error": "UNAUTHORIZED"})
                return

            if mode == "hardened":
                evaluation = pep.inspect_request(client_id, source_ip, endpoint, dpo_token)
                if evaluation["decision"] != "ALLOW":
                    record_telemetry({
                        "action": f"POST {endpoint}",
                        "client_id": client_id,
                        "source_ip": source_ip,
                        "decision": "BLOCKED",
                        "status_code": evaluation["status_code"],
                        "threat_type": evaluation["security_layer"],
                        "security_layer": evaluation["security_layer"],
                        "reason": evaluation["reason"]
                    })
                    print(f" [!] LIVE ATTACK INTERCEPTED: POST {endpoint} from {source_ip} -> {evaluation['security_layer']}")
                    self._send_response_json(evaluation["status_code"], {
                        "status": "DENIED",
                        "error": evaluation["security_layer"],
                        "details": evaluation["reason"]
                    })
                    return

            record_telemetry({
                "action": f"POST {endpoint}",
                "client_id": client_id,
                "source_ip": source_ip,
                "decision": "PERMITTED",
                "status_code": 200,
                "threat_type": "VULNERABILITY_EXPOSED" if mode == "vulnerable" else "LEGITIMATE_OPERATION",
                "security_layer": "ALLOW_GATE",
                "reason": "Operation allowed"
            })

            if endpoint == "/v1/learners/export":
                self._send_response_json(200, {
                    "status": "SUCCESS",
                    "job_id": "EXP-JOB-20261012-LIVE",
                    "target_bucket": "campusvault-exports",
                    "object_key": "learner-exports/learners-20261012.csv",
                    "records_exported": len(SYNTHETIC_LEARNERS),
                    "mode": mode
                })
            elif endpoint == "/v1/attendance/sync":
                self._send_response_json(200, {"status": "SUCCESS", "records_updated": 120})
            else:
                self._send_response_json(404, {"error": "NOT_FOUND"})

        def log_message(self, format, *args):
            pass

    return MockAPIHandler

def run_server(mode: str):
    handler = make_handler(mode)
    server = HTTPServer((HOST, PORT), handler)
    print("=" * 70)
    print(f" NORTHSTAR SENTINEL - LIVE THREAT MONITORING & PEP PROXY")
    print(f" Status: LISTENING on http://{HOST}:{PORT} (MODE: {mode.upper()})")
    print(f" Live Telemetry API: http://{HOST}:{PORT}/api/live-threats")
    print(f" Press Ctrl+C to terminate.")
    print("=" * 70)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Sentinel Live Monitoring terminated gracefully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Northstar Sentinel Live Threat Demonstration Server")
    parser.add_argument("--mode", choices=["vulnerable", "hardened"], default="hardened", help="Execution mode")
    args = parser.parse_args()
    run_server(args.mode)
