"""
Northstar Sentinel - Security Package
Comprehensive Zero-Trust Policy Enforcement Architecture:
  - source_restriction: Ingress Subnet Pinning & Dynamic Auto-Shunning
  - access_control: OAuth2 Least Privilege & Rate Limiting
  - credential_policy: Credential Lifecycle & Emergency Revocation
  - export_protection: Two-Man DPO Approval & DLP Bucket Quarantine
"""

from .source_restriction import SourceRestrictionEngine
from .access_control import AccessControlEngine
from .credential_policy import CredentialPolicyEngine
from .export_protection import ExportProtectionEngine

class ModularZeroTrustPEP:
    """
    Unified Policy Enforcement Point (PEP) aggregating all 4 security engines.
    """
    def __init__(self):
        self.source_engine = SourceRestrictionEngine()
        self.access_engine = AccessControlEngine()
        self.cred_engine = CredentialPolicyEngine()
        self.export_engine = ExportProtectionEngine()

    def inspect_request(
        self, client_id: str, source_ip: str, endpoint: str, dpo_token: str = None
    ) -> dict:
        # Layer 1: Source IP / CIDR Pinning
        ip_ok, ip_err = self.source_engine.validate_source_ip(client_id, source_ip)
        if not ip_ok:
            return {
                "decision": "DENY",
                "status_code": 403,
                "security_layer": "PERIMETER_IP_FILTER",
                "reason": ip_err
            }

        # Layer 2: Scope Validation
        scope_ok, scope_err = self.access_engine.validate_scope(client_id, endpoint)
        if not scope_ok:
            return {
                "decision": "DENY",
                "status_code": 403,
                "security_layer": "LEAST_PRIVILEGE_SCOPE_GATE",
                "reason": scope_err
            }

        # Layer 3: Rate Limiting
        rate_ok, rate_err = self.access_engine.check_rate_limit(client_id)
        if not rate_ok:
            return {
                "decision": "DENY",
                "status_code": 429,
                "security_layer": "TOKEN_BUCKET_RATE_LIMITER",
                "reason": rate_err
            }

        # Layer 4: Export Approval Gating
        export_ok, export_err = self.export_engine.validate_export_authorization(endpoint, client_id, dpo_token)
        if not export_ok:
            return {
                "decision": "DENY",
                "status_code": 403,
                "security_layer": "TWO_MAN_EXPORT_GATE",
                "reason": export_err
            }

        return {
            "decision": "ALLOW",
            "status_code": 200,
            "security_layer": "ALL_GATES_PASSED",
            "reason": "Authorized under active Zero-Trust policy."
        }

__all__ = [
    "SourceRestrictionEngine",
    "AccessControlEngine",
    "CredentialPolicyEngine",
    "ExportProtectionEngine",
    "ModularZeroTrustPEP"
]
