#!/usr/bin/env python3
"""
Northstar Sentinel - Verification Test Harness
Runs 11 automated test cases against the Zero-Trust Policy Enforcement Point (PEP).
Verifies:
  - Source IP whitelisting
  - Dynamic Adaptive IP Auto-Banning / Threat Shunning
  - Granular least-privilege scoping
  - Rate limiting
  - Two-Man Rule bulk PII export authorization
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from gateway_defense import ZeroTrustPolicyEnforcementPoint

class TestHardenedAPISecurity(unittest.TestCase):
    def setUp(self):
        self.pep = ZeroTrustPolicyEnforcementPoint()

    def test_01_legitimate_attendance_sync_allowed(self):
        """Test 1: Authorized RollCall connector from approved internal subnet."""
        res = self.pep.inspect_request(
            client_id="rollcall-prod",
            source_ip="10.10.4.12",
            endpoint="/v1/attendance/sync"
        )
        self.assertEqual(res["decision"], "ALLOW")
        self.assertEqual(res["status_code"], 200)

    def test_02_learner_search_denied_for_rollcall_scope(self):
        """Test 2: RollCall attempting learner search violates Least Privilege."""
        res = self.pep.inspect_request(
            client_id="rollcall-prod",
            source_ip="10.10.4.12",
            endpoint="/v1/learners/search"
        )
        self.assertEqual(res["decision"], "DENY")
        self.assertEqual(res["status_code"], 403)
        self.assertIn("PRIVILEGE_CREEP_BLOCKED", res["reason"])

    def test_03_bulk_learner_export_denied_for_rollcall(self):
        """Test 3: RollCall attempting mass learner export blocked by scope gate."""
        res = self.pep.inspect_request(
            client_id="rollcall-prod",
            source_ip="10.10.4.12",
            endpoint="/v1/learners/export"
        )
        self.assertEqual(res["decision"], "DENY")
        self.assertEqual(res["status_code"], 403)

    def test_04_unapproved_external_source_ip_denied(self):
        """Test 4: Request from external IP 203.0.113.77 blocked by IP whitelist."""
        res = self.pep.inspect_request(
            client_id="rollcall-prod",
            source_ip="203.0.113.77",
            endpoint="/v1/attendance/sync"
        )
        self.assertEqual(res["decision"], "DENY")
        self.assertEqual(res["status_code"], 403)
        self.assertIn("UNAUTHORIZED_SOURCE_IP", res["reason"])

    def test_05_spoofed_or_bogus_ip_string(self):
        """Test 5: Malformed IP strings are rejected cleanly."""
        res = self.pep.inspect_request(
            client_id="rollcall-prod",
            source_ip="999.999.999.999",
            endpoint="/v1/attendance/sync"
        )
        self.assertEqual(res["decision"], "DENY")
        self.assertEqual(res["status_code"], 403)

    def test_06_rate_limiting_enforcement(self):
        """Test 6: Exceeding 10 requests per minute triggers 429 rate limit."""
        client = "rollcall-prod"
        # Fire 10 allowed requests
        for _ in range(10):
            res = self.pep.inspect_request(client, "10.10.4.12", "/v1/attendance/sync")
            self.assertEqual(res["decision"], "ALLOW")
            
        # 11th request must trigger rate limit
        res_limit = self.pep.inspect_request(client, "10.10.4.12", "/v1/attendance/sync")
        self.assertEqual(res_limit["decision"], "DENY")
        self.assertEqual(res_limit["status_code"], 429)
        self.assertIn("RATE_LIMIT_EXCEEDED", res_limit["reason"])

    def test_07_course_catalog_access_denied_without_scope(self):
        """Test 7: Client without course:read cannot enumerate courses."""
        res = self.pep.inspect_request(
            client_id="rollcall-prod",
            source_ip="10.10.4.12",
            endpoint="/v1/courses"
        )
        self.assertEqual(res["decision"], "DENY")
        self.assertEqual(res["status_code"], 403)

    def test_08_bulk_export_requires_dual_authorization_token(self):
        """Test 8: Export without DPO approval token fails."""
        res = self.pep.inspect_request(
            client_id="classbridge-admin",
            source_ip="198.51.100.21",
            endpoint="/v1/learners/export",
            dpo_token=None
        )
        self.assertEqual(res["decision"], "DENY")
        self.assertEqual(res["status_code"], 403)
        self.assertIn("DUAL_AUTHORIZATION_REQUIRED", res["reason"])

    def test_09_bulk_export_permitted_with_valid_dpo_token(self):
        """Test 9: Admin with valid cryptographic DPO token is authorized."""
        self.pep.approved_export_tokens.add("DPO-AUTH-SEC-2026-TOKEN-99")
        res = self.pep.inspect_request(
            client_id="classbridge-admin",
            source_ip="198.51.100.21",
            endpoint="/v1/learners/export",
            dpo_token="DPO-AUTH-SEC-2026-TOKEN-99"
        )
        self.assertEqual(res["decision"], "ALLOW")
        self.assertEqual(res["status_code"], 200)

    def test_10_unknown_client_rejected(self):
        """Test 10: Unregistered client identity rejected by perimeter filter."""
        res = self.pep.inspect_request(
            client_id="hacker-bot-client",
            source_ip="10.10.4.12",
            endpoint="/v1/attendance"
        )
        self.assertEqual(res["decision"], "DENY")
        self.assertEqual(res["status_code"], 403)

    def test_11_suspicious_repeat_attacker_triggers_dynamic_auto_ban(self):
        """Test 11: Suspicious attacker attempting repeat probes triggers Adaptive Auto-Ban."""
        attacker_ip = "198.51.100.99"
        # First offense: unwhitelisted IP attempt
        res1 = self.pep.inspect_request("rollcall-prod", attacker_ip, "/v1/attendance/sync")
        self.assertEqual(res1["status_code"], 403)
        self.assertEqual(res1["security_layer"], "PERIMETER_IP_FILTER")

        # Second offense: repeat attempt (crosses threshold >= 2)
        res2 = self.pep.inspect_request("rollcall-prod", attacker_ip, "/v1/attendance/sync")
        self.assertEqual(res2["status_code"], 403)

        # Third attempt: Now blocked at Layer 0 (ADAPTIVE_THREAT_AUTO_SHUNNING)
        res3 = self.pep.inspect_request("rollcall-prod", attacker_ip, "/v1/attendance/sync")
        self.assertEqual(res3["status_code"], 403)
        self.assertEqual(res3["security_layer"], "ADAPTIVE_THREAT_AUTO_SHUNNING")
        self.assertIn("AUTO-BANNED", res3["reason"])

if __name__ == "__main__":
    print("=" * 70)
    print(" NORTHSTAR SENTINEL - DEFENSIVE TEST SUITE EXECUTION")
    print("=" * 70)
    unittest.main(verbosity=2)
