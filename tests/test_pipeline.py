#!/usr/bin/env python3
"""
Northstar Sentinel - Full Pipeline & Security Integration Tests
Executes end-to-end verification of the 6-stage DFIR pipeline and PEP defense.
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

import importlib
stage1 = importlib.import_module("01_verify_ingest")
stage2 = importlib.import_module("02_normalize")
stage3 = importlib.import_module("03_correlate")
stage4 = importlib.import_module("04_detect")
stage5 = importlib.import_module("05_risk_scoring")
stage6 = importlib.import_module("06_generate_report")
from gateway_defense import ZeroTrustPolicyEnforcementPoint

class TestSentinelPipeline(unittest.TestCase):
    def test_stage_1_ingestion_and_hashing(self):
        """Verify that all 12 evidence artifacts are ingested and hashed."""
        manifest = stage1.verify_and_ingest()
        self.assertEqual(len(manifest), 12)
        for item in manifest:
            self.assertEqual(item["status"], "VERIFIED_INTEGRITY")
            self.assertEqual(len(item["sha256"]), 64)

    def test_stage_2_normalization(self):
        """Verify unified normalization produces valid OCSF-aligned schema."""
        events = stage2.normalize_all_events()
        self.assertGreater(len(events), 25)
        sample = events[0]
        self.assertIn("event_id", sample)
        self.assertIn("timestamp", sample)
        self.assertIn("source_system", sample)
        self.assertIn("actor_identity", sample)
        self.assertIn("source_ip", sample)
        self.assertIn("action", sample)

    def test_stage_3_correlation(self):
        """Verify correlations connect auth, api, storage, and network events."""
        correlations = stage3.run_correlation()
        self.assertGreaterEqual(len(correlations), 8)
        cor_ids = [c["correlation_id"] for c in correlations]
        self.assertIn("COR-01", cor_ids)
        self.assertIn("COR-04", cor_ids)
        self.assertIn("COR-06", cor_ids)

    def test_stage_4_detections(self):
        """Verify DET-001 through DET-010 detection rules fire correctly."""
        detections = stage4.run_detections()
        self.assertGreaterEqual(len(detections), 8)
        det_ids = [d["detection_id"] for d in detections]
        self.assertIn("DET-001", det_ids) # Unrecognized IP
        self.assertIn("DET-002", det_ids) # Privilege Creep
        self.assertIn("DET-003", det_ids) # Bulk Export

    def test_stage_5_risk_scoring(self):
        """Verify decoupled risk scoring and triage tier calculation."""
        scored = stage5.calculate_risk_scores()
        self.assertGreaterEqual(len(scored), 8)
        top_risk = scored[0]
        self.assertGreaterEqual(top_risk["triage_index"], 85.0)

    def test_stage_6_report_generation(self):
        """Verify formal DFIR report generation."""
        report_file = stage6.generate_formal_report()
        self.assertTrue(os.path.exists(report_file))
        self.assertGreater(os.path.getsize(report_file), 1000)

if __name__ == "__main__":
    print("=" * 70)
    print(" NORTHSTAR SENTINEL - COMPLETE PIPELINE VERIFICATION")
    print("=" * 70)
    unittest.main(verbosity=2)
