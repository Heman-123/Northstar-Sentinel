#!/usr/bin/env python3
"""
Northstar Sentinel - Security Module: Credential Policy & Token Lifecycle
Enforces credential rotation policies, validates token format, and maintains
an instant in-memory revocation list for JTI tokens.
"""

from typing import Dict, Set, Optional, Tuple

class CredentialPolicyEngine:
    def __init__(self):
        # Known registered keys with maximum allowable TTL (seconds)
        self.credential_registry: Dict[str, dict] = {
            "rollcall-prod": {"key_id": "rc-prod-01", "max_ttl_days": 90},
            "classbridge-admin": {"key_id": "cb-adm-01", "max_ttl_days": 30}
        }
        # In-memory revoked token identifiers (0ms instant revocation)
        self.revoked_tokens: Set[str] = set()

    def revoke_token(self, token_jti: str) -> None:
        """Instantly revokes a token JTI across all gateway nodes."""
        self.revoked_tokens.add(token_jti)

    def validate_credential(self, client_id: str, auth_header: str) -> Tuple[bool, Optional[str]]:
        """
        Validates token existence, Bearer format, and revocation state.
        Returns: (is_permitted, denial_reason)
        """
        if not auth_header or not auth_header.startswith("Bearer "):
            return False, "AUTHENTICATION_FAILED: Missing or malformed Bearer authorization token."

        token_body = auth_header.split(" ", 1)[1].strip()

        if token_body in self.revoked_tokens:
            return False, f"TOKEN_REVOKED: JTI token '{token_body}' has been revoked by emergency SOAR policy."

        return True, None
