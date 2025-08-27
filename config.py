"""
Configuration file for Row Performance Analyzer

This file contains different system configurations and scenarios for analysis.
"""

# Default system configuration
DEFAULT_CONFIG = {
    'total_rows': 1024,
    'write_time_per_row_ns': 1,
    'settling_time_us': 1,
    'usage_time_ns': 2048
}

# High-performance memory system
HIGH_PERF_CONFIG = {
    'total_rows': 2048,
    'write_time_per_row_ns': 0.5,
    'settling_time_us': 0.5,
    'usage_time_ns': 4096
}

# Low-power memory system
LOW_POWER_CONFIG = {
    'total_rows': 512,
    'write_time_per_row_ns': 2,
    'settling_time_us': 2,
    'usage_time_ns': 1024
}

# Extreme settling time scenario
LONG_SETTLING_CONFIG = {
    'total_rows': 1024,
    'write_time_per_row_ns': 1,
    'settling_time_us': 5,
    'usage_time_ns': 5000
}

# Fast write, slow settling scenario
FAST_WRITE_SLOW_SETTLING_CONFIG = {
    'total_rows': 1024,
    'write_time_per_row_ns': 0.1,
    'settling_time_us': 10,
    'usage_time_ns': 3000
}

# All available configurations
CONFIGURATIONS = {
    'default': DEFAULT_CONFIG,
    'high_perf': HIGH_PERF_CONFIG,
    'low_power': LOW_POWER_CONFIG,
    'long_settling': LONG_SETTLING_CONFIG,
    'fast_write_slow_settling': FAST_WRITE_SLOW_SETTLING_CONFIG
}

def get_config(config_name='default'):
    """Get a configuration by name."""
    return CONFIGURATIONS.get(config_name, DEFAULT_CONFIG).copy()

def list_configurations():
    """List all available configurations."""
    return list(CONFIGURATIONS.keys())

def print_config_summary():
    """Print a summary of all configurations."""
    print("Available System Configurations:")
    print("=" * 50)
    
    for name, config in CONFIGURATIONS.items():
        print(f"\n{name.upper()}:")
        print(f"  Total rows: {config['total_rows']}")
        print(f"  Write time: {config['write_time_per_row_ns']} ns/row")
        print(f"  Settling time: {config['settling_time_us']} μs")
        print(f"  Usage time: {config['usage_time_ns']} ns")
        
        # Calculate some key metrics
        write_duration = config['total_rows'] * config['write_time_per_row_ns']
        settling_duration = config['settling_time_us'] * 1000
        total_settling_time = write_duration + settling_duration
        
        print(f"  Write duration: {write_duration} ns")
        print(f"  Total settling time: {total_settling_time} ns")
        print(f"  Efficiency: {config['usage_time_ns'] / total_settling_time:.2f}x")
