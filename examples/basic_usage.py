#!/usr/bin/env python3
"""
Basic Usage Example for Row Performance Analyzer

This example demonstrates how to use the core functions of the analyzer.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from row_performance_analyzer import (
    calculate_usable_fraction,
    calculate_settled_rows_over_time,
    generate_graph_1,
    generate_graph_2
)

def main():
    print("Row Performance Analyzer - Basic Usage Example")
    print("=" * 50)
    
    # Example 1: Calculate usable fraction at different times
    print("\n1. Usable Fraction Analysis:")
    print("-" * 30)
    
    times = [0, 500, 1000, 1024, 1500, 2024, 2048]
    
    for time_ns in times:
        fraction = calculate_usable_fraction(time_ns)
        usable_rows = int(fraction * 1024)
        print(f"Time {time_ns:4d}ns: {fraction:.3f} usable ({usable_rows:4d} rows)")
    
    # Example 2: Analyze settled rows over time
    print("\n2. Settled Rows Analysis (first 10 time points):")
    print("-" * 50)
    
    time_series = calculate_settled_rows_over_time(100)
    print("Time(ns) | Settled Rows")
    print("---------|-------------")
    
    for time, settled in time_series[:10]:
        print(f"{time:8d} | {settled:11d}")
    
    # Example 3: Generate graphs
    print("\n3. Generating Performance Graphs...")
    print("-" * 35)
    
    try:
        generate_graph_1()
        generate_graph_2()
        print("✓ Graphs generated successfully!")
        print("  - graph1_usable_fraction.png")
        print("  - graph2_settled_rows.png")
    except Exception as e:
        print(f"✗ Error generating graphs: {e}")
    
    # Example 4: Performance comparison
    print("\n4. Performance Comparison:")
    print("-" * 25)
    
    # Compare different settling times
    settling_times = [0.5, 1.0, 2.0, 5.0]
    
    print("Settling Time | Usable Fraction at 1024ns")
    print("(μs)         | (fraction)")
    print("-------------|---------------------------")
    
    for settling_time in settling_times:
        fraction = calculate_usable_fraction(1024, settling_time_us=settling_time)
        print(f"{settling_time:11.1f} | {fraction:25.3f}")
    
    print("\nExample completed successfully!")

if __name__ == "__main__":
    main()
