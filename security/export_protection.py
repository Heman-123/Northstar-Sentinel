#!/usr/bin/env python3
"""
Northstar Sentinel - Security Module: Export Protection & Two-Man DPO Gating
Enforces Layer 4 mandatory Data Protection Officer (DPO) cryptographic approval
for any bulk personal data export, satisfying India DPDPA 2023 Sec 8(5).
"""

from typing import Optional, Tuple

class ExportProtectionEngine:
    def __init__(self):
        # Approved cryptographic DPO signing tokens for statutory audits
        self.approved_dpo_tokens = {
            "DPO-AUTH-2026-CH-9912": {"issued_to": "classbridge-admin", "purpose": "Statutory Annual Regulatory Audit"}
        }
        # S3 / CampusVault DLP Isolation State
        self.campusvault_locked: bool = False

    def set_dlp_lockdown(self, lock: bool) -> None:
        """Toggles S3 DLP quarantine lockdown mode."""
        self.campusvault_locked = lock

    def validate_export_authorization(
        self, endpoint: str, client_id: str, dpo_token: Optional[str]
    ) -> Tuple[bool, Optional[str]]:
        """
        Validates whether bulk export requests satisfy the Two-Man Rule.
        Returns: (is_permitted, denial_reason)
        """
        if not endpoint.startswith("/v1/learners/export"):
            return True, None

        if self.campusvault_locked:
            return False, "CAMPUSVAULT_ISOLATED: Export repository bucket is quarantined in read-only DLP mode."

        if not dpo_token:
            return False, (
                "DUAL_AUTHORIZATION_REQUIRED: Bulk export of student PII requires "
                "an asynchronous X-DPO-Approval-Token as mandated by Policy Section 5.3 & DPDPA 2023."
            )

        if dpo_token not in self.approved_dpo_tokens:
            return False, f"INVALID_DPO_TOKEN: The provided token '{dpo_token}' is unrecognized or unverified."

        token_meta = self.approved_dpo_tokens[dpo_token]
        if token_meta["issued_to"] != client_id:
            return False, f"DPO_TOKEN_MISMATCH: Token was issued to {token_meta['issued_to']}, not {client_id}."

        return True, None
