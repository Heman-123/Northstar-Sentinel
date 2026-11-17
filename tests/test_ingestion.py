#!/usr/bin/env python3
"""
Northstar Sentinel - Stage 1 Unit Tests: Ingestion & Cryptographic Chain of Custody
Verifies SHA-256 evidence integrity, file discovery, and manifest generation.
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

import importlib
stage1 = importlib.import_module("01_verify_ingest")

class TestEvidenceIngestion(unittest.TestCase):
    def test_verify_all_twelve_artifacts(self):
        """Ensure all 12 evidentiary artifacts (E01-E12) are present and verified."""
        manifest = stage1.verify_and_ingest()
        self.assertEqual(len(manifest), 12, "Must verify exactly 12 evidence artifacts.")
        
        for item in manifest:
            self.assertEqual(item["status"], "VERIFIED_INTEGRITY")
            self.assertEqual(len(item["sha256"]), 64)
            size = item.get("size_bytes", item.get("file_size_bytes", 0))
            self.assertTrue(size > 0)

    def test_manifest_file_persisted(self):
        """Verify the evidence_hashes.csv manifest file is created on disk."""
        manifest_path = os.path.join(PROJECT_ROOT, "data", "processed", "evidence_hashes.csv")
        self.assertTrue(os.path.exists(manifest_path))

if __name__ == "__main__":
    unittest.main()
