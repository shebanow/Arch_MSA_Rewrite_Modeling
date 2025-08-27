#!/usr/bin/env python3
"""
Main entry point for the Row Performance Analyzer

This script provides a command-line interface for analyzing row usage patterns
with settling time constraints.
"""

import argparse
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from row_performance_analyzer import (
    calculate_usable_fraction,
    calculate_settled_rows_over_time,
    generate_graph_1,
    generate_graph_2,
    print_analysis
)

def main():
    parser = argparse.ArgumentParser(
        description="Row Performance Analyzer - Analyze row usage patterns with settling time constraints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --generate-graphs                    # Generate both graphs
  python main.py --analyze-time 1500                  # Analyze usage at 1500ns
  python main.py --settled-rows 2048                  # Show settled rows over 2048ns
  python main.py --full-analysis                      # Run complete analysis
        """
    )
    
    parser.add_argument(
        '--generate-graphs',
        action='store_true',
        help='Generate both performance graphs'
    )
    
    parser.add_argument(
        '--analyze-time',
        type=int,
        metavar='TIME_NS',
        help='Analyze usable fraction at specific time (nanoseconds)'
    )
    
    parser.add_argument(
        '--settled-rows',
        type=int,
        metavar='TIME_NS',
        help='Show settled rows over time for specified duration (nanoseconds)'
    )
    
    parser.add_argument(
        '--full-analysis',
        action='store_true',
        help='Run complete analysis with all graphs and detailed output'
    )
    
    parser.add_argument(
        '--total-rows',
        type=int,
        default=1024,
        help='Total number of rows (default: 1024)'
    )
    
    parser.add_argument(
        '--write-time',
        type=int,
        default=1,
        help='Write time per row in nanoseconds (default: 1)'
    )
    
    parser.add_argument(
        '--settling-time',
        type=int,
        default=1,
        help='Settling time in microseconds (default: 1)'
    )
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    print("=" * 60)
    print("ROW PERFORMANCE ANALYZER")
    print("=" * 60)
    print(f"Configuration:")
    print(f"  Total rows: {args.total_rows}")
    print(f"  Write time per row: {args.write_time} ns")
    print(f"  Settling time: {args.settling_time} μs")
    print()
    
    if args.analyze_time is not None:
        fraction = calculate_usable_fraction(
            args.analyze_time, 
            args.total_rows, 
            args.write_time, 
            args.settling_time
        )
        usable_rows = int(fraction * args.total_rows)
        print(f"Analysis at {args.analyze_time}ns:")
        print(f"  Usable fraction: {fraction:.3f}")
        print(f"  Usable rows: {usable_rows}/{args.total_rows}")
        print(f"  Settling rows: {args.total_rows - usable_rows}")
    
    if args.settled_rows is not None:
        print(f"\nSettled rows analysis over {args.settled_rows}ns:")
        time_series = calculate_settled_rows_over_time(
            args.settled_rows, 
            args.total_rows, 
            args.write_time, 
            args.settling_time
        )
        print("  Time(ns) | Settled Rows")
        print("  ---------|-------------")
        for time, settled in time_series[::100]:  # Show every 100th point
            print(f"  {time:8d} | {settled:11d}")
    
    if args.generate_graphs:
        print("\nGenerating performance graphs...")
        generate_graph_1()
        generate_graph_2()
        print("Graphs saved as graph1_usable_fraction.png and graph2_settled_rows.png")
    
    if args.full_analysis:
        print("\nRunning full analysis...")
        generate_graph_1()
        generate_graph_2()
        print_analysis()
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
