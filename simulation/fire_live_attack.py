#!/usr/bin/env python3
"""
Northstar Sentinel - Live Threat Generator & Attack Simulator
Fires real live HTTP attack payloads against the Sentinel PEP Proxy (http://127.0.0.1:8765)
to demonstrate real-time interception, tracking, and automated auto-banning.
"""

import sys
import time
import urllib.request
import urllib.error
import json

TARGET_URL = "http://127.0.0.1:8765"

def send_payload(name, method, endpoint, headers, expected_to_fail=True):
    print(f"\n[*] DISPATCHING: {name}")
    print(f"    -> {method} {TARGET_URL}{endpoint}")
    print(f"    -> Source IP: {headers.get('X-Forwarded-For')} | Client: {headers.get('X-Client-ID')}")

    req = urllib.request.Request(
        f"{TARGET_URL}{endpoint}",
        headers=headers,
        method=method
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read().decode('utf-8')
            print(f"    [+] RESPONSE: HTTP {resp.status} - ALLOWED")
            print(f"        Payload: {data[:120]}...")
    except urllib.error.HTTPError as e:
        data = e.read().decode('utf-8')
        print(f"    [!] INTERCEPTED: HTTP {e.code} - BLOCKED BY SENTINEL PEP")
        print(f"        Reason: {data}")
    except Exception as e:
        print(f"    [-] Connection Failed: {e}")
        print("        Ensure 'simulation/mock_api_server.py' is running on port 8765!")

def main():
    print("=" * 70)
    print(" NORTHSTAR SENTINEL - LIVE ATTACK DISPATCHER & STRIKE HARNESS")
    print(" Target: http://127.0.0.1:8765")
    print("=" * 70)

    # Attack 1: External IP Token Replay
    send_payload(
        name="ATTACK 1: External IP Token Replay (Case NS-26-014 Scenario)",
        method="GET",
        endpoint="/v1/attendance/sync",
        headers={
            "X-Client-ID": "rollcall-prod",
            "X-Forwarded-For": "203.0.113.77", # Unauthorized external IP
            "Authorization": "Bearer demo-rollcall-token"
        }
    )
    time.sleep(1)

    # Attack 2: Out-of-Scope Bulk Learner Export
    send_payload(
        name="ATTACK 2: Privilege Creep (RollCall calling Bulk Learner Export)",
        method="POST",
        endpoint="/v1/learners/export",
        headers={
            "X-Client-ID": "rollcall-prod",
            "X-Forwarded-For": "10.10.4.12",
            "Authorization": "Bearer demo-rollcall-token"
        }
    )
    time.sleep(1)

    # Attack 3: Repeat Attacker triggering Auto-Ban
    print("\n[*] ATTACK 3: Repeat Offenses triggering Sentinel Dynamic Auto-Ban...")
    for i in range(1, 4):
        send_payload(
            name=f"ATTACK 3.{i}: Unauthorized Probe from Suspicious IP",
            method="GET",
            endpoint="/v1/attendance/sync",
            headers={
                "X-Client-ID": "rollcall-prod",
                "X-Forwarded-For": "198.51.100.99",
                "Authorization": "Bearer demo-rollcall-token"
            }
        )
        time.sleep(0.5)

    # Normal Operation
    send_payload(
        name="BENCHMARK: Legitimate Scheduled Attendance Sync",
        method="GET",
        endpoint="/v1/attendance/sync",
        headers={
            "X-Client-ID": "rollcall-prod",
            "X-Forwarded-For": "10.10.4.12",
            "Authorization": "Bearer demo-rollcall-token"
        }
    )

    print("\n" + "=" * 70)
    print(" All live attack simulations dispatched.")
    print(" Check your dashboard or http://127.0.0.1:8765/api/live-threats for live telemetry!")
    print("=" * 70)

if __name__ == "__main__":
    main()
