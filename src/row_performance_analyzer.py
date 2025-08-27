import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

class RowState:
    """Represents the state of a single row with color and usable time."""
    
    def __init__(self):
        """Constructor sets initial color to green and usable time to t=0 (already settled)."""
        self._color = 0  # 0 = green, 1 = blue
        self._usable_time = 0  # Time in nanoseconds when row becomes usable
    
    def get_color(self) -> int:
        """Get the current color of the row."""
        return self._color
    
    def set_color(self, color: int):
        """Set the color of the row."""
        self._color = color
    
    def get_usable_time(self) -> int:
        """Get the usable time of the row."""
        return self._usable_time
    
    def set_usable_time(self, usable_time: int):
        """Set the usable time of the row."""
        self._usable_time = usable_time
    
    def write_row(self, current_time_ns: int):
        """Write the row at current time. Flips color and sets usable time to current_time + 1μs."""
        self._color = 1 - self._color  # Flip color
        self._usable_time = current_time_ns + 1000  # Add 1μs (1000ns) settling time

def calculate_usable_fraction(usage_time_us: int, total_rows: int = 1024, 
                            write_time_per_row_us: int = 1, settling_time_us: int = 1) -> float:
    """
    Calculate the fraction of rows that are usable (not settling) for a given usage time.
    
    Args:
        usage_time_us: Time in microseconds when we want to use the rows
        total_rows: Total number of rows (default 1024)
        write_time_per_row_us: Time to write one row in microseconds (default 1)
        settling_time_us: Settling time in microseconds (default 1)
    
    Returns:
        Fraction of rows that are usable (0.0 to 1.0)
    """
    # Calculate how many rows have been written by the usage time
    rows_written = min(usage_time_us // write_time_per_row_us, total_rows)
    
    if rows_written == 0:
        return 1.0  # All rows are usable if none have been written
    
    # Calculate how many rows are still settling
    # A row is settling if it was written within the last settling_time_us
    settling_cutoff_time = usage_time_us - settling_time_us
    rows_settling = 0
    
    if settling_cutoff_time > 0:
        # Calculate how many rows are still settling
        rows_written_before_cutoff = min(rows_written, settling_cutoff_time // write_time_per_row_us)
        rows_settling = rows_written - rows_written_before_cutoff
    else:
        # All written rows are still settling
        rows_settling = rows_written
    
    # Usable rows = total rows - rows that are settling
    usable_rows = total_rows - rows_settling
    return usable_rows / total_rows

def calculate_row_states_over_time(usage_time_ns: int = 8000, total_rows: int = 1024) -> List[Tuple[int, int, int, int]]:
    """
    Calculate the row states over time using the RowState class approach.
    
    Args:
        usage_time_ns: Total usage time in nanoseconds (default 8000 ns)
        total_rows: Total number of rows (default 1024)
    
    Returns:
        List of (time_ns, settled_green_rows, settled_blue_rows, unsettled_rows) tuples
    """
    time_points = []
    settled_green_counts = []
    settled_blue_counts = []
    unsettled_counts = []
    
    # Create 1024 instances of RowState in an array
    row_states = [RowState() for _ in range(total_rows)]
    
    # State machine variables
    master_color = 0  # Start with green
    change_in_progress = False
    current_row_index = 0
    
    # Define color change start times
    green_to_blue_start = 10    # Start Green -> Blue at t=10ns
    blue_to_green_start = 4000  # Start Blue -> Green at t=4000ns
    
    # Start with all rows settled at time 0
    time_points.append(0)
    settled_green_counts.append(total_rows)
    settled_blue_counts.append(0)
    unsettled_counts.append(0)
    
    # Simulate each time step (1 ns intervals)
    for time_ns in range(1, usage_time_ns + 1):
        # State machine for color change
        if not change_in_progress:
            # Check if it's time to start a color change
            if time_ns == green_to_blue_start or time_ns == blue_to_green_start:
                change_in_progress = True
                current_row_index = 0
        
        # Write the current row if we're in progress
        if change_in_progress and current_row_index < total_rows:
            row_states[current_row_index].write_row(time_ns)
            current_row_index += 1
        
        # Check if we've written all rows
        if current_row_index >= total_rows and change_in_progress:
            # Go back to idle
            change_in_progress = False
            # Flip the master color
            master_color = 1 - master_color
        
        # Count different row states: iterate through all 1024 row states
        settled_green_rows = 0
        settled_blue_rows = 0
        unsettled_rows = 0
        
        for row_state in row_states:
            color = row_state.get_color()
            usable_time = row_state.get_usable_time()
            
            if usable_time > time_ns:
                # Unsettled: written but not yet settled
                unsettled_rows += 1
            elif color == 0:  # Green
                # Settled green
                settled_green_rows += 1
            else:  # color == 1, Blue
                # Settled blue
                settled_blue_rows += 1
        
        time_points.append(time_ns)
        settled_green_counts.append(settled_green_rows)
        settled_blue_counts.append(settled_blue_rows)
        unsettled_counts.append(unsettled_rows)
    
    return list(zip(time_points, settled_green_counts, settled_blue_counts, unsettled_counts))

def calculate_trapezoid_width(N: int, total_rows: int = 1024) -> int:
    """
    Calculate the trapezoid width for N usage instances.
    
    The trapezoid represents the time needed to compute all {U1, ..., UN} x {R0, ..., R1023} combinations
    during color transitions.
    
    Args:
        N: Number of usage instances
        total_rows: Total number of rows (default 1024)
    
    Returns:
        Width of the trapezoid in nanoseconds
    """
    if N <= total_rows:
        # For N <= 1024, we need two ramps (2048 cycles)
        # Each ramp takes 1024 cycles (1ns per row)
        ramp_width = total_rows  # 1024ns
        return 2 * ramp_width  # 2048ns
    else:
        # For N > 1024, we have a flat top in addition to the ramps
        # The flat top duration is (N - total_rows) cycles
        ramp_width = total_rows  # 1024ns
        flat_top_width = N - total_rows
        return 2 * ramp_width + flat_top_width

def generate_graph_1():
    """Generate Graph #1: Average computations per clock vs number of usage instances"""
    print("Generating Graph 1: Average vector dot products per clock vs vector sequence length")
    
    # Create N range from 0 to 25000 in increments of 250
    N_values = np.arange(0, 25001, 250)
    avg_computations_per_clock = []
    
    for N in N_values:
        if N == 0:
            avg_computations_per_clock.append(0)
        else:
            width = calculate_trapezoid_width(N)
            # Total computations = N * 1024 (N usage instances × 1024 rows)
            total_computations = N * 1024
            avg_per_clock = total_computations / width
            avg_computations_per_clock.append(avg_per_clock)
    
    plt.figure(figsize=(12, 8))
    plt.plot(N_values, avg_computations_per_clock, 'b-', linewidth=2)
    plt.xlabel('Vector Sequence Length (N)', fontsize=12)
    plt.ylabel('Average Vector Dot Products per Clock Cycle', fontsize=12)
    plt.title('Average Vector Dot Products per Clock vs. Vector Sequence Length\n(1024 rows, 1ns write time, 1μs settling time)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 25000)
    plt.ylim(0, 1024)
    
    # Add key points and annotations
    key_N_values = [0, 1024, 2048, 5000, 10000, 25000]
    for N in key_N_values:
        if N <= 25000 and N > 0:
            width = calculate_trapezoid_width(N)
            total_computations = N * 1024
            avg_per_clock = total_computations / width
            plt.plot(N, avg_per_clock, 'ro', markersize=8)
            plt.annotate(f'(N={N}, {avg_per_clock:.1f} dot products/clock)', 
                        xy=(N, avg_per_clock), xytext=(10, -20),
                        textcoords='offset points', fontsize=10,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # Add horizontal line for asymptotic limit (1024 vector dot products/clock)
    plt.axhline(y=1024, color='r', linestyle='--', alpha=0.7, 
                label='Asymptotic Limit: 1024 vector dot products/clock')
    
    # Add vertical line at N=1024
    plt.axvline(x=1024, color='g', linestyle='--', alpha=0.7, 
                label='N=1024 (all rows)')
    
    plt.legend()
    plt.tight_layout()
    plt.savefig('graph1_usable_fraction.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_graph_2():
    """Generate Graph 2: Row states area chart for 8000ns MSA Clock Cycle"""
    print("Generating Graph 2: Row states area chart (8000ns MSA Clock Cycle)")
    
    # Calculate row states over time
    time_series = calculate_row_states_over_time(usage_time_ns=8000)  # 8000ns
    times, settled_green_counts, settled_blue_counts, unsettled_counts = zip(*time_series)
    
    plt.figure(figsize=(12, 8))
    
    # Create stacked area chart
    plt.fill_between(times, 0, settled_green_counts, color='green', alpha=0.7, label='Settled Green Rows')
    plt.fill_between(times, settled_green_counts, [g + b for g, b in zip(settled_green_counts, settled_blue_counts)], 
                     color='blue', alpha=0.7, label='Settled Blue Rows')
    plt.fill_between(times, [g + b for g, b in zip(settled_green_counts, settled_blue_counts)], 
                     [1024] * len(times), color='red', alpha=0.7, label='Unsettled Rows')
    
    plt.xlabel('Time (nanoseconds)', fontsize=12)
    plt.ylabel('Row Count', fontsize=12)
    plt.title('Row State vs. Time\n(8000ns MSA Clock Cycles, 1024 rows, 1ns write time, 1μs settling time)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 8000)
    plt.ylim(0, 1025)
    
    # Add key points and annotations
    key_times_ns = [0, 10, 1000, 1034, 4000, 5000, 5024, 8000]
    for time_ns in key_times_ns:
        if time_ns <= 8000:
            # Find the corresponding counts
            idx = min(time_ns, len(settled_green_counts) - 1)
            settled_green = settled_green_counts[idx]
            settled_blue = settled_blue_counts[idx]
            unsettled = unsettled_counts[idx]
            
            # Plot point at the top of the stack
            plt.plot(time_ns, 1024, 'ko', markersize=8)
            plt.annotate(f'({time_ns}ns)\nG:{settled_green} B:{settled_blue} U:{unsettled}', 
                        xy=(time_ns, 1024), xytext=(10, -20),
                        textcoords='offset points', fontsize=8,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    # Add horizontal line for total rows
    plt.axhline(y=1024, color='black', linestyle='--', alpha=0.7, label='Total Rows (1024)')
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
    
    # Get the time series data
    time_series = calculate_row_states_over_time(8000)  # 8000ns
    time_dict = {}
    for time_ns, settled_green, settled_blue, unsettled in time_series:
        time_dict[time_ns] = (settled_green, settled_blue, unsettled)
    
    # Time 0: Before any writing
    settled_green_0, settled_blue_0, unsettled_0 = time_dict[0]
    print(f"  Time 0ns: {settled_green_0} settled green, {settled_blue_0} settled blue, {unsettled_0} unsettled")
    
    # Time 10ns: Start of Green -> Blue transition
    settled_green_10, settled_blue_10, unsettled_10 = time_dict[10]  # 10ns
    print(f"  Time 10ns: {settled_green_10} settled green, {settled_blue_10} settled blue, {unsettled_10} unsettled")
    
    # Time 1034ns: End of Green -> Blue transition (10 + 1024)
    settled_green_1034, settled_blue_1034, unsettled_1034 = time_dict[1034]  # 1034ns
    print(f"  Time 1034ns: {settled_green_1034} settled green, {settled_blue_1034} settled blue, {unsettled_1034} unsettled")
    
    # Time 4000ns: Start of Blue -> Green transition
    settled_green_4000, settled_blue_4000, unsettled_4000 = time_dict[4000]  # 4000ns
    print(f"  Time 4000ns: {settled_green_4000} settled green, {settled_blue_4000} settled blue, {unsettled_4000} unsettled")
    
    # Time 5024ns: End of Blue -> Green transition (4000 + 1024)
    settled_green_5024, settled_blue_5024, unsettled_5024 = time_dict[5024]  # 5024ns
    print(f"  Time 5024ns: {settled_green_5024} settled green, {settled_blue_5024} settled blue, {unsettled_5024} unsettled")
    
    # Time 8000ns: End of simulation
    settled_green_8000, settled_blue_8000, unsettled_8000 = time_dict[8000]  # 8000ns
    print(f"  Time 8000ns: {settled_green_8000} settled green, {settled_blue_8000} settled blue, {unsettled_8000} unsettled")
    
    print(f"\nGraph 2 Analysis (8000ns MSA Clock Cycle):")
    start_green, start_blue, start_unsettled = time_series[0][1:]
    end_green, end_blue, end_unsettled = time_series[-1][1:]
    print(f"  Start (0ns): {start_green} settled green, {start_blue} settled blue, {start_unsettled} unsettled")
    print(f"  End (8000ns): {end_green} settled green, {end_blue} settled blue, {end_unsettled} unsettled")
    print(f"  Net change in settled green: {end_green - start_green} rows")
    
    print(f"\nPerformance Analysis:")
    print(f"  Efficiency (N=1024): {(1024 * 1024) / calculate_trapezoid_width(1024):.1f} vector dot products/clock")
    print(f"  Efficiency (N=2048): {(2048 * 1024) / calculate_trapezoid_width(2048):.1f} vector dot products/clock")
    print(f"  Efficiency (N=5000): {(5000 * 1024) / calculate_trapezoid_width(5000):.1f} vector dot products/clock")
    print(f"  Efficiency (N=10000): {(10000 * 1024) / calculate_trapezoid_width(10000):.1f} vector dot products/clock")
    print(f"  Efficiency (N=25000): {(25000 * 1024) / calculate_trapezoid_width(25000):.1f} vector dot products/clock")
    print(f"  Asymptotic limit: 1024.0 vector dot products/clock")
    print(f"  Trapezoid width (N=1024): {calculate_trapezoid_width(1024)}ns")
    print(f"  Trapezoid width (N=25000): {calculate_trapezoid_width(25000)}ns")

if __name__ == "__main__":
    # Set up matplotlib for better plots
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10
    
    # Generate both graphs
    generate_graph_1()
    generate_graph_2()  # Commented out temporarily
    
    # Print detailed analysis
    print_analysis()
    
    print("\nGraphs saved as:")
    print("  - graph1_usable_fraction.png")
    print("  - graph2_settled_rows.png")
