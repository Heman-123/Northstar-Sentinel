#!/usr/bin/env python3
"""
Northstar Sentinel - Zero-Trust API Policy Enforcement Point (PEP)
Provides enterprise defensive controls:
  1. Automated Dynamic IP Blacklisting & Threat Shunning (Adaptive Auto-Ban)
  2. Source IP CIDR Whitelisting & Geo/Perimeter Pinning
  3. Granular Least-Privilege OAuth2 Scope Enforcement
  4. Leaky-Bucket Rate Limiting (Scraping & DoS Throttling)
  5. Asynchronous Two-Man Rule Approval for Bulk PII Exports
"""

import time
import ipaddress
from typing import Dict, List, Tuple, Optional

class ZeroTrustPolicyEnforcementPoint:
    def __init__(self):
        # 1. Approved CIDRs for vendor integrations & admin consoles
        self.approved_cidrs = {
            "rollcall-prod": [ipaddress.ip_network("10.10.4.0/24")],
            "backend-worker": [ipaddress.ip_network("10.10.2.0/24")],
            "staff-vpn": [ipaddress.ip_network("198.51.100.0/24")],
            "classbridge-admin": [ipaddress.ip_network("198.51.100.0/24")]
        }

        # 2. Principle of Least Privilege (PoLP) Scope Catalog
        self.authorized_scopes = {
            "rollcall-prod": ["attendance:read", "attendance:sync"],
            "razorpay-prod": ["payments:read", "payments:write"],
            "classbridge-admin": ["*"]
        }

        # 3. Dynamic IP Threat Shunning & Quarantine (Auto-Ban Register)
        # Structure: { ip_str: ban_expiration_epoch }
        self.dynamic_blacklisted_ips: Dict[str, float] = {}
        # Violation history tracking: { ip_str: [list of violation timestamps] }
        self.ip_violation_counters: Dict[str, List[float]] = {}
        self.max_violations_before_ban = 2
        self.default_ban_duration_seconds = 3600 # 1 hour ban

        # 4. Rate Limiting State (Token Bucket)
        self.rate_limits: Dict[str, List[float]] = {}
        self.max_requests_per_window = 10
        self.window_seconds = 60

        # 5. Dual-Authorization Approval Register for Bulk Exports
        self.approved_export_tokens = set()

    def is_ip_banned(self, source_ip_str: str) -> Tuple[bool, str]:
        """Layer 0: Checks if IP is currently under active quarantine/auto-ban."""
        now = time.time()
        if source_ip_str in self.dynamic_blacklisted_ips:
            ban_expiry = self.dynamic_blacklisted_ips[source_ip_str]
            if now < ban_expiry:
                remaining = int(ban_expiry - now)
                return True, f"DYNAMICALLY_QUARANTINED: IP {source_ip_str} is AUTO-BANNED due to suspicious activity ({remaining}s remaining)"
            else:
                # Ban expired
                del self.dynamic_blacklisted_ips[source_ip_str]
        return False, "IP_NOT_BANNED"

    def record_suspicious_offense(self, source_ip_str: str, reason: str) -> bool:
        """Records an offense against an IP and auto-bans if threshold is exceeded."""
        now = time.time()
        violations = self.ip_violation_counters.get(source_ip_str, [])
        # Keep violations within last 10 minutes
        violations = [t for t in violations if now - t < 600]
        violations.append(now)
        self.ip_violation_counters[source_ip_str] = violations

        # Auto-ban trigger on repeated or critical violations
        if len(violations) >= self.max_violations_before_ban or "CRITICAL" in reason:
            self.dynamic_blacklisted_ips[source_ip_str] = now + self.default_ban_duration_seconds
            return True # Triggered new ban
        return False

    def validate_source_ip(self, client_id: str, source_ip_str: str) -> Tuple[bool, str]:
        """Enforces IP whitelisting per integration client ID."""
        try:
            client_ip = ipaddress.ip_address(source_ip_str)
        except ValueError:
            self.record_suspicious_offense(source_ip_str, "CRITICAL: Malformed IP attempt")
            return False, f"MALFORMED_IP: {source_ip_str}"

        allowed_networks = self.approved_cidrs.get(client_id, [])
        if not allowed_networks:
            self.record_suspicious_offense(source_ip_str, "Unregistered client attempt")
            return False, f"NO_WHITELIST_CONFIGURED_FOR_CLIENT: {client_id}"

        for net in allowed_networks:
            if client_ip in net:
                return True, "IP_AUTHORIZED"

        # Offense recorded for unauthorized IP attempt
        self.record_suspicious_offense(source_ip_str, f"Unauthorized source IP attempt for {client_id}")
        return False, f"UNAUTHORIZED_SOURCE_IP: {source_ip_str} not permitted for client {client_id}"

    def validate_least_privilege_scope(self, client_id: str, requested_endpoint: str, source_ip: str) -> Tuple[bool, str]:
        """Verifies that requested action is within client's authorized scopes."""
        allowed_scopes = self.authorized_scopes.get(client_id, [])
        if "*" in allowed_scopes:
            return True, "SUPERUSER_SCOPE_ALLOWED"

        endpoint_scope_map = {
            "/v1/attendance": "attendance:read",
            "/v1/attendance/sync": "attendance:sync",
            "/v1/attendance/all": "attendance:read",
            "/v1/learners/search": "learner:search",
            "/v1/learners/export": "learner:export",
            "/v1/courses": "course:read"
        }

        required_scope = endpoint_scope_map.get(requested_endpoint)
        if not required_scope:
            self.record_suspicious_offense(source_ip, f"Probing unknown endpoint {requested_endpoint}")
            return False, f"UNKNOWN_ENDPOINT: {requested_endpoint}"

        if required_scope in allowed_scopes:
            return True, f"SCOPE_AUTHORIZED: {required_scope}"

        # Unauthorized scope escalation attempt recorded as offense
        self.record_suspicious_offense(source_ip, f"Scope escalation attempt on {requested_endpoint}")
        return False, f"PRIVILEGE_CREEP_BLOCKED: Client '{client_id}' lacks required scope '{required_scope}'"

    def enforce_rate_limiting(self, client_id: str, source_ip: str) -> Tuple[bool, str]:
        """Leaky-bucket rate limiter to prevent automated scraping and portal DoS."""
        now = time.time()
        timestamps = self.rate_limits.get(client_id, [])
        timestamps = [t for t in timestamps if now - t < self.window_seconds]
        
        if len(timestamps) >= self.max_requests_per_window:
            self.rate_limits[client_id] = timestamps
            self.record_suspicious_offense(source_ip, "Burst rate limit breach")
            return False, f"RATE_LIMIT_EXCEEDED: Maximum {self.max_requests_per_window} requests per {self.window_seconds}s"

        timestamps.append(now)
        self.rate_limits[client_id] = timestamps
        return True, "RATE_LIMIT_OK"

    def verify_bulk_export_authorization(self, requested_endpoint: str, dpo_approval_token: Optional[str], source_ip: str) -> Tuple[bool, str]:
        """Enforces dual-key authorization (Two-Man Rule) for bulk PII exports."""
        if requested_endpoint != "/v1/learners/export":
            return True, "NOT_AN_EXPORT_ENDPOINT"

        if not dpo_approval_token:
            self.record_suspicious_offense(source_ip, "Attempted bulk PII export without DPO token")
            return False, "DUAL_AUTHORIZATION_REQUIRED: Missing X-DPO-Approval-Token for bulk learner PII export"

        if dpo_approval_token not in self.approved_export_tokens:
            self.record_suspicious_offense(source_ip, "CRITICAL: Forged or invalid DPO approval token")
            return False, "INVALID_EXPORT_TOKEN: Provided DPO approval token is invalid, expired, or unverified"

        return True, "EXPORT_OPERATION_LEGITIMATELY_AUTHORIZED"

    def inspect_request(self, client_id: str, source_ip: str, endpoint: str, dpo_token: Optional[str] = None) -> Dict:
        """Comprehensive Zero-Trust Security Policy Evaluation Pipeline."""
        # Layer 0: Check if IP is Auto-Banned / Shunning active
        banned, ban_reason = self.is_ip_banned(source_ip)
        if banned:
            return {
                "decision": "DENY",
                "status_code": 403,
                "reason": ban_reason,
                "security_layer": "ADAPTIVE_THREAT_AUTO_SHUNNING"
            }

        # Layer 1: Source IP CIDR Whitelist Check
        ip_ok, ip_msg = self.validate_source_ip(client_id, source_ip)
        if not ip_ok:
            return {
                "decision": "DENY",
                "status_code": 403,
                "reason": ip_msg,
                "security_layer": "PERIMETER_IP_FILTER"
            }

        # Layer 2: Least-Privilege Scope Gate
        scope_ok, scope_msg = self.validate_least_privilege_scope(client_id, endpoint, source_ip)
        if not scope_ok:
            return {
                "decision": "DENY",
                "status_code": 403,
                "reason": scope_msg,
                "security_layer": "LEAST_PRIVILEGE_SCOPE_GATE"
            }

        # Layer 3: Rate Limiting & Throttler
        rate_ok, rate_msg = self.enforce_rate_limiting(client_id, source_ip)
        if not rate_ok:
            return {
                "decision": "DENY",
                "status_code": 429,
                "reason": rate_msg,
                "security_layer": "RATE_LIMITING_THROTTLER"
            }

        # Layer 4: Dual-Key Export Authorization (Two-Man Rule)
        export_ok, export_msg = self.verify_bulk_export_authorization(endpoint, dpo_token, source_ip)
        if not export_ok:
            return {
                "decision": "DENY",
                "status_code": 403,
                "reason": export_msg,
                "security_layer": "TWO_MAN_EXPORT_GATE"
            }

        return {
            "decision": "ALLOW",
            "status_code": 200,
            "reason": "ALL_ZERO_TRUST_CHECKS_PASSED",
            "security_layer": "PERMITTED"
        }

if __name__ == "__main__":
    pep = ZeroTrustPolicyEnforcementPoint()
    print("[*] Testing Zero-Trust Policy Enforcement Point with Dynamic Auto-Ban...")

    # First attempt from external IP
    res1 = pep.inspect_request("rollcall-prod", "203.0.113.77", "/v1/attendance/sync")
    print(f"Request 1 (External IP): {res1['decision']} ({res1['status_code']}) - {res1['reason']}")

    # Second attempt from external IP (triggers auto-ban threshold)
    res2 = pep.inspect_request("rollcall-prod", "203.0.113.77", "/v1/attendance/sync")
    print(f"Request 2 (External IP): {res2['decision']} ({res2['status_code']}) - {res2['reason']}")

    # Third attempt from external IP (now directly dropped by Adaptive Threat Auto-Shunning)
    res3 = pep.inspect_request("rollcall-prod", "203.0.113.77", "/v1/attendance/sync")
    print(f"Request 3 (After Auto-Ban): {res3['decision']} ({res3['status_code']}) - {res3['reason']}")
