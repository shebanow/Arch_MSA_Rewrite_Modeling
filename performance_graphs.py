import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

def calculate_usable_fraction(usage_time_ns: int, total_rows: int = 1024, 
                            write_time_per_row_ns: int = 1, settling_time_us: int = 1) -> float:
    """
    Calculate the fraction of rows that are usable (not settling) for a given usage time.
    
    Args:
        usage_time_ns: Time in nanoseconds when we want to use the rows
        total_rows: Total number of rows (default 1024)
        write_time_per_row_ns: Time to write one row in nanoseconds (default 1)
        settling_time_us: Settling time in microseconds (default 1)
    
    Returns:
        Fraction of rows that are usable (0.0 to 1.0)
    """
    settling_time_ns = settling_time_us * 1000  # Convert microseconds to nanoseconds
    
    # Calculate how many rows have been written by the usage time
    rows_written = min(usage_time_ns // write_time_per_row_ns, total_rows)
    
    if rows_written == 0:
        return 1.0  # All rows are usable if none have been written
    
    # Calculate how many rows are still settling
    # A row is settling if it was written within the last settling_time_ns
    settling_cutoff_time = usage_time_ns - settling_time_ns
    rows_settling = 0
    
    if settling_cutoff_time > 0:
        # Calculate how many rows were written after the settling cutoff
        rows_written_after_cutoff = max(0, rows_written - (settling_cutoff_time // write_time_per_row_ns))
        rows_settling = min(rows_written_after_cutoff, rows_written)
    
    # Usable rows = total rows - rows that are settling
    usable_rows = total_rows - rows_settling
    return usable_rows / total_rows

def calculate_settled_rows_over_time(usage_time_ns: int = 2048, total_rows: int = 1024,
                                   write_time_per_row_ns: int = 1, settling_time_us: int = 1) -> List[Tuple[int, int]]:
    """
    Calculate the number of settled rows over time for a given usage time.
    
    Args:
        usage_time_ns: Total usage time in nanoseconds (default 2048)
        total_rows: Total number of rows (default 1024)
        write_time_per_row_ns: Time to write one row in nanoseconds (default 1)
        settling_time_us: Settling time in microseconds (default 1)
    
    Returns:
        List of (time_ns, settled_rows) tuples
    """
    settling_time_ns = settling_time_us * 1000
    time_points = []
    settled_counts = []
    
    # Start with all rows settled at time 0
    time_points.append(0)
    settled_counts.append(total_rows)
    
    # Simulate each time step
    for time_ns in range(1, usage_time_ns + 1):
        # Calculate how many rows have been written by this time
        rows_written = min(time_ns // write_time_per_row_ns, total_rows)
        
        # Calculate how many rows are settled
        # A row is settled if it was written more than settling_time_ns ago
        settled_cutoff_time = time_ns - settling_time_ns
        
        if settled_cutoff_time <= 0:
            # No rows have settled yet, all original rows are still settled
            settled_rows = total_rows
        else:
            # Calculate how many rows were written before the settling cutoff
            rows_settled = max(0, min(rows_written, settled_cutoff_time // write_time_per_row_ns))
            settled_rows = total_rows - rows_written + rows_settled
        
        time_points.append(time_ns)
        settled_counts.append(settled_rows)
    
    return list(zip(time_points, settled_counts))

def generate_graph_1():
    """Generate Graph #1: Usable fraction vs usage time"""
    print("Generating Graph #1: Usable fraction vs usage time")
    
    # Create usage time range (0 to 3000 ns to see the full pattern)
    usage_times = np.arange(0, 3001, 10)  # Every 10 ns for smooth curve
    usable_fractions = []
    
    for time_ns in usage_times:
        fraction = calculate_usable_fraction(time_ns)
        usable_fractions.append(fraction)
    
    plt.figure(figsize=(12, 8))
    plt.plot(usage_times, usable_fractions, 'b-', linewidth=2)
    plt.xlabel('Usage Time (nanoseconds)', fontsize=12)
    plt.ylabel('Fraction of Rows Usable', fontsize=12)
    plt.title('Graph #1: Usable Fraction vs Usage Time\n(1024 rows, 1ns write time, 1μs settling time)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 3000)
    plt.ylim(0, 1.05)
    
    # Add some key points
    key_times = [0, 1000, 1024, 2000, 2024]
    for time in key_times:
        if time <= 3000:
            fraction = calculate_usable_fraction(time)
            plt.plot(time, fraction, 'ro', markersize=8)
            plt.annotate(f'({time}ns, {fraction:.3f})', 
                        xy=(time, fraction), xytext=(10, 10),
                        textcoords='offset points', fontsize=10,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('graph1_usable_fraction.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_graph_2():
    """Generate Graph #2: Settled rows vs time for 2048ns usage time"""
    print("Generating Graph #2: Settled rows vs time (2048ns usage)")
    
    # Calculate settled rows over time
    time_series = calculate_settled_rows_over_time(usage_time_ns=2048)
    times, settled_counts = zip(*time_series)
    
    plt.figure(figsize=(12, 8))
    plt.plot(times, settled_counts, 'g-', linewidth=2)
    plt.xlabel('Time (nanoseconds)', fontsize=12)
    plt.ylabel('Number of Settled Rows', fontsize=12)
    plt.title('Graph #2: Settled Rows vs Time\n(2048ns usage time, 1024 rows, 1ns write time, 1μs settling time)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 2048)
    plt.ylim(0, 1025)
    
    # Add key points and annotations
    key_times = [0, 1000, 1024, 1500, 2000, 2048]
    for time in key_times:
        if time <= 2048:
            # Find the corresponding settled count
            idx = min(time, len(settled_counts) - 1)
            settled = settled_counts[idx]
            plt.plot(time, settled, 'ro', markersize=8)
            plt.annotate(f'({time}ns, {settled})', 
                        xy=(time, settled), xytext=(10, 10),
                        textcoords='offset points', fontsize=10,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # Add horizontal line for total rows
    plt.axhline(y=1024, color='r', linestyle='--', alpha=0.7, label='Total Rows (1024)')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('graph2_settled_rows.png', dpi=300, bbox_inches='tight')
    plt.show()

def print_analysis():
    """Print detailed analysis of the system"""
    print("\n" + "="*60)
    print("PERFORMANCE ANALYSIS")
    print("="*60)
    
    print(f"System Parameters:")
    print(f"  - Total rows: 1024")
    print(f"  - Write time per row: 1 ns")
    print(f"  - Settling time: 1 μs (1000 ns)")
    print(f"  - Time to write all rows: 1024 ns")
    
    print(f"\nKey Time Points Analysis:")
    
    # Time 0: Before any writing
    fraction_0 = calculate_usable_fraction(0)
    print(f"  Time 0ns: {fraction_0:.3f} usable ({fraction_0*1024:.0f} rows)")
    
    # Time 1000ns: During writing
    fraction_1000 = calculate_usable_fraction(1000)
    print(f"  Time 1000ns: {fraction_1000:.3f} usable ({fraction_1000*1024:.0f} rows)")
    
    # Time 1024ns: Just finished writing
    fraction_1024 = calculate_usable_fraction(1024)
    print(f"  Time 1024ns: {fraction_1024:.3f} usable ({fraction_1024*1024:.0f} rows)")
    
    # Time 2024ns: All rows settled
    fraction_2024 = calculate_usable_fraction(2024)
    print(f"  Time 2024ns: {fraction_2024:.3f} usable ({fraction_2024*1024:.0f} rows)")
    
    # Time 2048ns: Usage time for Graph 2
    fraction_2048 = calculate_usable_fraction(2048)
    print(f"  Time 2048ns: {fraction_2048:.3f} usable ({fraction_2048*1024:.0f} rows)")
    
    print(f"\nGraph 2 Analysis (2048ns usage time):")
    time_series = calculate_settled_rows_over_time(2048)
    start_settled = time_series[0][1]
    end_settled = time_series[-1][1]
    print(f"  Start (0ns): {start_settled} settled rows")
    print(f"  End (2048ns): {end_settled} settled rows")
    print(f"  Net change: {end_settled - start_settled} rows")

if __name__ == "__main__":
    # Set up matplotlib for better plots
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10
    
    # Generate both graphs
    generate_graph_1()
    generate_graph_2()
    
    # Print detailed analysis
    print_analysis()
    
    print("\nGraphs saved as:")
    print("  - graph1_usable_fraction.png")
    print("  - graph2_settled_rows.png")
