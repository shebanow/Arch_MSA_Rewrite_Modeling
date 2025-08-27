"""
Row Performance Analyzer Package

A comprehensive tool for analyzing row usage patterns with settling time constraints
in memory systems and architectures.
"""

__version__ = "1.0.0"
__author__ = "Neurophos"
__description__ = "Performance analysis and modeling for row usage patterns with settling time constraints"

from .row_performance_analyzer import (
    calculate_usable_fraction,
    calculate_settled_rows_over_time,
    generate_graph_1,
    generate_graph_2,
    print_analysis
)

__all__ = [
    'calculate_usable_fraction',
    'calculate_settled_rows_over_time', 
    'generate_graph_1',
    'generate_graph_2',
    'print_analysis'
]
