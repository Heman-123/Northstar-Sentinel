#!/usr/bin/env python3
"""
Northstar Sentinel - Security Module: Access Control & Least Privilege
Enforces Layer 2 fine-grained OAuth2 scopes and Layer 3 token-bucket rate limiting.
"""

import time
from typing import Dict, List, Optional, Tuple

class AccessControlEngine:
    def __init__(self):
        # Strict least-privilege scopes per client identity
        self.client_scopes: Dict[str, List[str]] = {
            "rollcall-prod": ["attendance.sync"],
            "classbridge-admin": ["learner.search", "learner.export", "course.read"],
            "staff-vpn": ["attendance.read", "course.read"],
            "backend-worker": ["storage.write"]
        }

        # Rate limiting state: {client_id: [timestamp_list]}
        self.rate_limit_records: Dict[str, List[float]] = {}
        self.max_requests_per_min = 10
        self.window_seconds = 60

    def validate_scope(self, client_id: str, endpoint: str) -> Tuple[bool, Optional[str]]:
        """
        Enforces least-privilege scoping per endpoint.
        Returns: (is_permitted, denial_reason)
        """
        scopes = self.client_scopes.get(client_id, [])

        if endpoint.startswith("/v1/attendance"):
            if "attendance.sync" not in scopes and "attendance.read" not in scopes:
                return False, f"SCOPE_INSUFFICIENT: Endpoint {endpoint} requires attendance.sync or attendance.read"
        elif endpoint.startswith("/v1/learners/search"):
            if "learner.search" not in scopes:
                return False, f"SCOPE_INSUFFICIENT: Endpoint {endpoint} requires learner.search"
        elif endpoint.startswith("/v1/learners/export"):
            if "learner.export" not in scopes:
                return False, f"SCOPE_INSUFFICIENT: Endpoint {endpoint} requires learner.export"
        elif endpoint.startswith("/v1/courses"):
            if "course.read" not in scopes:
                return False, f"SCOPE_INSUFFICIENT: Endpoint {endpoint} requires course.read"
        else:
            return False, f"UNRECOGNIZED_ENDPOINT_ACCESS: {endpoint}"

        return True, None

    def check_rate_limit(self, client_id: str) -> Tuple[bool, Optional[str]]:
        """
        Enforces token-bucket rate limiting (max 10 requests per 60-second window).
        Returns: (is_permitted, denial_reason)
        """
        now = time.time()
        if client_id not in self.rate_limit_records:
            self.rate_limit_records[client_id] = []

        # Prune old timestamps
        self.rate_limit_records[client_id] = [
            t for t in self.rate_limit_records[client_id] if now - t < self.window_seconds
        ]

        if len(self.rate_limit_records[client_id]) >= self.max_requests_per_min:
            return False, f"RATE_LIMIT_EXCEEDED: Maximum {self.max_requests_per_min} requests/minute limit breached."

        self.rate_limit_records[client_id].append(now)
        return True, None
