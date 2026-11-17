#!/usr/bin/env python3
"""
Northstar Sentinel - Stage 3 Unit Tests: Multi-Source Correlation Engine
Verifies that cross-source correlations link authentication, gateway, storage,
and network feeds while preserving explicit relationship type labels.
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

import importlib
stage3 = importlib.import_module("03_correlate")

class TestCorrelation(unittest.TestCase):
    def test_correlation_rules_coverage(self):
        """Verify all critical correlations (COR-01 through COR-09) are formed."""
        correlations = stage3.run_correlation()
        self.assertGreaterEqual(len(correlations), 8)
        
        cor_ids = [c["correlation_id"] for c in correlations]
        self.assertIn("COR-01", cor_ids)
        self.assertIn("COR-02", cor_ids)
        self.assertIn("COR-03", cor_ids)
        self.assertIn("COR-04", cor_ids)
        self.assertIn("COR-05", cor_ids)
        self.assertIn("COR-06", cor_ids)
        self.assertIn("COR-07", cor_ids)
        self.assertIn("COR-08", cor_ids)
        self.assertIn("COR-09", cor_ids)

    def test_relationship_labels(self):
        """Verify strict DFIR relationship types: DIRECT_EVIDENCE, CORRELATED_INFERENCE, UNPROVEN_HYPOTHESIS."""
        correlations = stage3.run_correlation()
        types = {c["relationship_type"] for c in correlations}
        self.assertIn("DIRECT_EVIDENCE", types)
        self.assertIn("CORRELATED_INFERENCE", types)
        self.assertIn("UNPROVEN_HYPOTHESIS", types)

    def test_correlation_csv_outputs(self):
        """Verify correlated_events.csv, incident_timeline.csv, and correlation_report.json exist."""
        stage3.run_correlation()
        c_csv = os.path.join(PROJECT_ROOT, "data", "processed", "correlated_events.csv")
        t_csv = os.path.join(PROJECT_ROOT, "data", "processed", "incident_timeline.csv")
        r_json = os.path.join(PROJECT_ROOT, "data", "processed", "correlation_report.json")
        self.assertTrue(os.path.exists(c_csv))
        self.assertTrue(os.path.exists(t_csv))
        self.assertTrue(os.path.exists(r_json))

if __name__ == "__main__":
    unittest.main()
