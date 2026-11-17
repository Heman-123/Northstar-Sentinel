#!/usr/bin/env python3
"""
Northstar Sentinel - Stage 4 Unit Tests: Behavioral Detection Engine
Verifies that rules DET-001 through DET-010 fire reliably and carry valid MITRE ATT&CK references.
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

import importlib
stage4 = importlib.import_module("04_detect")

class TestDetection(unittest.TestCase):
    def test_all_ten_detection_rules_fire(self):
        """Verify DET-001 through DET-010 detection rules fire correctly."""
        detections = stage4.run_detections()
        self.assertEqual(len(detections), 10, "Expected exactly 10 deterministic detections.")
        
        det_ids = [d["detection_id"] for d in detections]
        for i in range(1, 11):
            expected_id = f"DET-{i:03d}"
            self.assertIn(expected_id, det_ids, f"Missing detection rule: {expected_id}")

    def test_mitre_mapping_and_evidence_citations(self):
        """Verify every detection links to a MITRE technique and raw evidence citation."""
        detections = stage4.run_detections()
        for det in detections:
            self.assertTrue(det["mitre_technique"].startswith("T"), f"Invalid MITRE ID in {det['detection_id']}")
            ev_refs = det.get("evidence_references", det.get("evidence_citations", []))
            self.assertTrue(len(ev_refs) > 0, f"Missing evidence in {det['detection_id']}")
            self.assertIn(det["severity"], ["CRITICAL", "HIGH", "MEDIUM"])

if __name__ == "__main__":
    unittest.main()
