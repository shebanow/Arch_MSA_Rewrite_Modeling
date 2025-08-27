# Performance Graphs Generator

This Python script generates performance graphs for analyzing row usage patterns with settling time constraints.

## Problem Description

The system has the following characteristics:
- **1024 total rows** that can be written to
- **1 nanosecond per row** write time
- **1 microsecond settling time** after writing a row before it can be used
- **Sequential writing** starting from row 0
- **All 1024 rows must be written** once writing begins

## Generated Graphs

### Graph #1: Usable Fraction vs Usage Time
Shows the fraction of rows that are usable (not settling) as a function of usage time in nanoseconds.

**Key Insights:**
- At time 0ns: 100% of rows are usable (1024 rows)
- At time 1000ns: 100% of rows are still usable (writing hasn't started yet)
- At time 1024ns: Only 2.3% of rows are usable (24 rows) - this is when writing just finished and most rows are settling
- At time 2024ns: 100% of rows are usable again (all rows have settled)

### Graph #2: Settled Rows vs Time (2048ns Usage)
Shows the number of settled rows over time for a 2048ns usage period, starting with all 1024 rows settled.

**Key Insights:**
- Starts with all 1024 rows settled
- During writing (0-1024ns), settled rows decrease as new rows are written and become unsettled
- After writing completes, rows gradually settle back
- Ends with all 1024 rows settled again

## Installation and Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the script:**
   ```bash
   python performance_graphs.py
   ```

3. **Output:**
   - `graph1_usable_fraction.png` - Usable fraction vs usage time
   - `graph2_settled_rows.png` - Settled rows vs time
   - Console output with detailed analysis

## System Parameters

The script uses these default parameters:
- Total rows: 1024
- Write time per row: 1 ns
- Settling time: 1 μs (1000 ns)
- Usage time for Graph 2: 2048 ns

These can be modified in the script functions if needed.

## Analysis Results

The analysis shows that:
- The system has a critical period around 1024ns when most rows are settling
- By 2024ns, all rows have settled and are usable again
- The net change in settled rows over 2048ns is 0 (starts and ends with all rows settled)
