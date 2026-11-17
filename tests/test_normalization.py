#!/usr/bin/env python3
"""
Northstar Sentinel - Stage 2 Unit Tests: Normalization Engine
Verifies conversion of heterogeneous logs into a unified OCSF-aligned schema.
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

import importlib
stage2 = importlib.import_module("02_normalize")

class TestNormalization(unittest.TestCase):
    def test_ocsf_schema_fields(self):
        """Verify unified normalization produces valid OCSF-aligned schema."""
        events = stage2.normalize_all_events()
        self.assertGreater(len(events), 25, "Expected at least 25 normalized events.")
        
        required_fields = ["event_id", "timestamp", "source_system", "actor_identity", "source_ip", "action"]
        for field in required_fields:
            self.assertIn(field, events[0], f"Missing required OCSF field: {field}")

    def test_normalization_outputs_exist(self):
        """Verify normalized_events.csv and reference_data.json exist."""
        stage2.normalize_all_events()
        norm_csv = os.path.join(PROJECT_ROOT, "data", "processed", "normalized_events.csv")
        ref_json = os.path.join(PROJECT_ROOT, "data", "processed", "reference_data.json")
        self.assertTrue(os.path.exists(norm_csv))
        self.assertTrue(os.path.exists(ref_json))

if __name__ == "__main__":
    unittest.main()
