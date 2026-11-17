#!/usr/bin/env python3
"""
Northstar Sentinel - Security Module: Source Restriction & CIDR Pinning
Enforces Layer 1 IP whitelisting per integration registration and provides
dynamic adaptive IP shunning (auto-ban) for threat containment.
"""

import ipaddress
import time
from typing import Dict, List, Optional, Tuple

class SourceRestrictionEngine:
    def __init__(self):
        # Whitelisted CIDRs per client identity
        self.approved_cidrs: Dict[str, List[ipaddress.IPv4Network]] = {
            "rollcall-prod": [ipaddress.ip_network("10.10.4.0/24")],
            "classbridge-admin": [ipaddress.ip_network("198.51.100.0/24")],
            "staff-vpn": [ipaddress.ip_network("198.51.100.0/24")],
            "backend-worker": [ipaddress.ip_network("10.10.2.0/24")]
        }
        # In-memory dynamic shunned IPs: {ip_str: ban_expiration_timestamp}
        self.shunned_ips: Dict[str, float] = {}

    def shun_ip(self, ip_str: str, duration_seconds: int = 3600) -> None:
        """Dynamically add an IP to the active quarantine shun list."""
        self.shunned_ips[ip_str] = time.time() + duration_seconds

    def is_ip_shunned(self, ip_str: str) -> bool:
        """Check if an IP is actively quarantined."""
        if ip_str in self.shunned_ips:
            if time.time() < self.shunned_ips[ip_str]:
                return True
            else:
                del self.shunned_ips[ip_str]
        return False

    def validate_source_ip(self, client_id: str, ip_str: str) -> Tuple[bool, Optional[str]]:
        """
        Validates source IP against client's approved CIDR range and active shun list.
        Returns: (is_permitted, denial_reason)
        """
        # 1. Check if IP is under active quarantine
        if self.is_ip_shunned(ip_str):
            return False, f"SOURCE_IP_ACTIVELY_QUARANTINED: {ip_str} is shunned by adaptive defense."

        # 2. Parse IP
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError:
            return False, f"INVALID_IP_FORMAT: '{ip_str}' is not a valid IPv4/IPv6 address."

        # 3. Check approved CIDRs
        if client_id not in self.approved_cidrs:
            return False, f"NO_WHITELIST_CONFIGURED_FOR_CLIENT: {client_id}"

        matched = any(ip_obj in network for network in self.approved_cidrs[client_id])
        if not matched:
            # Auto-shun rogue external IPs attempting vendor impersonation
            self.shun_ip(ip_str, 3600)
            return False, (
                f"UNAPPROVED_SOURCE_IP_DENIED: {ip_str} violates approved CIDRs for {client_id}. "
                f"IP has been added to 1-hour quarantine."
            )

        return True, None
