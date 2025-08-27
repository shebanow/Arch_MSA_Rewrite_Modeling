"""
Unit tests for Row Performance Analyzer

Tests the core functions for calculating usable fractions and settled rows.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from row_performance_analyzer import (
    calculate_usable_fraction,
    calculate_settled_rows_over_time
)

class TestRowPerformanceAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Set up test parameters."""
        self.total_rows = 1024
        self.write_time = 1
        self.settling_time = 1
    
    def test_calculate_usable_fraction_time_zero(self):
        """Test usable fraction at time 0."""
        fraction = calculate_usable_fraction(0, self.total_rows, self.write_time, self.settling_time)
        self.assertEqual(fraction, 1.0)
    
    def test_calculate_usable_fraction_before_writing(self):
        """Test usable fraction before any writing occurs."""
        fraction = calculate_usable_fraction(500, self.total_rows, self.write_time, self.settling_time)
        self.assertEqual(fraction, 1.0)
    
    def test_calculate_usable_fraction_during_writing(self):
        """Test usable fraction during writing process."""
        # At time 1000ns, 1000 rows have been written, but 1000-1000=0 are settling
        fraction = calculate_usable_fraction(1000, self.total_rows, self.write_time, self.settling_time)
        self.assertEqual(fraction, 1.0)
    
    def test_calculate_usable_fraction_after_writing(self):
        """Test usable fraction after writing completes."""
        # At time 1024ns, all 1024 rows have been written
        # Settling cutoff is 1024-1000=24ns, so 24 rows are settled
        fraction = calculate_usable_fraction(1024, self.total_rows, self.write_time, self.settling_time)
        expected_usable = 24  # Only the first 24 rows have settled
        expected_fraction = expected_usable / self.total_rows
        self.assertAlmostEqual(fraction, expected_fraction, places=3)
    
    def test_calculate_usable_fraction_all_settled(self):
        """Test usable fraction when all rows have settled."""
        # At time 2024ns, all rows should have settled
        fraction = calculate_usable_fraction(2024, self.total_rows, self.write_time, self.settling_time)
        self.assertEqual(fraction, 1.0)
    
    def test_calculate_settled_rows_initial_state(self):
        """Test settled rows at time 0."""
        time_series = calculate_settled_rows_over_time(100, self.total_rows, self.write_time, self.settling_time)
        initial_settled = time_series[0][1]
        self.assertEqual(initial_settled, self.total_rows)
    
    def test_calculate_settled_rows_during_writing(self):
        """Test settled rows during writing process."""
        time_series = calculate_settled_rows_over_time(1000, self.total_rows, self.write_time, self.settling_time)
        # At time 1000ns, 1000 rows have been written
        # Settling cutoff is 1000-1000=0ns, so no rows have settled yet
        settled_at_1000 = time_series[1000][1]
        self.assertEqual(settled_at_1000, 0)
    
    def test_calculate_settled_rows_after_settling(self):
        """Test settled rows after settling period."""
        time_series = calculate_settled_rows_over_time(2024, self.total_rows, self.write_time, self.settling_time)
        # At time 2024ns, all rows should have settled
        settled_at_2024 = time_series[2024][1]
        self.assertEqual(settled_at_2024, self.total_rows)
    
    def test_edge_case_zero_rows(self):
        """Test edge case with zero total rows."""
        fraction = calculate_usable_fraction(1000, 0, self.write_time, self.settling_time)
        self.assertEqual(fraction, 1.0)  # Should handle gracefully
    
    def test_edge_case_zero_settling_time(self):
        """Test edge case with zero settling time."""
        fraction = calculate_usable_fraction(1024, self.total_rows, self.write_time, 0)
        self.assertEqual(fraction, 1.0)  # All rows should be usable immediately
    
    def test_different_configurations(self):
        """Test with different system configurations."""
        # Test with different total rows
        fraction = calculate_usable_fraction(100, 512, self.write_time, self.settling_time)
        self.assertEqual(fraction, 1.0)
        
        # Test with different write time
        fraction = calculate_usable_fraction(200, self.total_rows, 2, self.settling_time)
        self.assertEqual(fraction, 1.0)

if __name__ == '__main__':
    unittest.main()
