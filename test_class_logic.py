#!/usr/bin/env python3

from src.row_performance_analyzer import RowState

def test_class_logic():
    """Test the class-based logic step by step"""
    total_rows = 1024
    
    print("Testing class-based logic:")
    print("Time | Master Color | Change Progress | Current Row | Usable Rows | Row 0 State | Row 1 State")
    print("-" * 90)
    
    # Create 1024 instances of RowState in an array
    row_states = [RowState() for _ in range(total_rows)]
    
    # State machine variables
    master_color = 0  # Start with black
    change_in_progress = False
    current_row_index = 0
    
    # Test around critical points - run full simulation
    test_times = [0, 1, 2, 1000, 1000000, 1024000, 1025000, 2048000]
    
    # Run full simulation up to max test time
    max_time = max(test_times)
    
    for time_ns in range(max_time + 1):
        # State machine for color change
        if not change_in_progress:
            # Start a new color change
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
            # Reset for next cycle
            current_row_index = 0
        
        # Only print at test times
        if time_ns in test_times:
            # Count usable rows: iterate through all 1024 row states
            usable_rows = 0
            for row_state in row_states:
                if (row_state.get_color() == master_color and 
                    row_state.get_usable_time() <= time_ns):
                    usable_rows += 1
            
            # Show states of first two rows for debugging
            row0_state = f"({row_states[0].get_color()},{row_states[0].get_usable_time()})" if time_ns < 10000 else "N/A"
            row1_state = f"({row_states[1].get_color()},{row_states[1].get_usable_time()})" if time_ns < 10000 else "N/A"
            
            print(f"{time_ns:8d} | {master_color:11d} | {str(change_in_progress):14s} | {current_row_index:11d} | {usable_rows:11d} | {row0_state:11s} | {row1_state:11s}")

if __name__ == "__main__":
    test_class_logic()
