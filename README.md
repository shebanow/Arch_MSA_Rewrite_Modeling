# Row Performance Analyzer

A comprehensive Python package for analyzing row usage patterns with settling time constraints in memory systems and architectures.

## 🚀 Features

- **Performance Analysis**: Calculate usable row fractions over time
- **Settling Time Modeling**: Model row settling behavior after writes
- **Multiple Configurations**: Pre-defined system configurations for different scenarios
- **Visualization**: Generate performance graphs and charts
- **Command Line Interface**: Easy-to-use CLI for quick analysis
- **Extensible**: Modular design for custom analysis scenarios

## 📋 Problem Description

The system has the following characteristics:
- **1024 total rows** that can be written to
- **1 nanosecond per row** write time
- **1 microsecond settling time** after writing a row before it can be used
- **Sequential writing** starting from row 0
- **All 1024 rows must be written** once writing begins

## 🏗️ Project Structure

```
Arch_MSA_Rewrite_Modeling/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   └── row_performance_analyzer.py  # Core analysis functions
├── tests/                       # Unit tests
│   ├── __init__.py
│   └── test_analyzer.py
├── examples/                    # Usage examples
│   └── basic_usage.py
├── docs/                        # Documentation
├── data/                        # Data files
├── main.py                      # Command line interface
├── config.py                    # System configurations
├── setup.py                     # Package setup
├── Makefile                     # Development tasks
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip

### Quick Start
```bash
# Clone the repository
git clone https://github.com/shebanow/Arch_MSA_Rewrite_Modeling.git
cd Arch_MSA_Rewrite_Modeling

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Development Installation
```bash
# Install with development dependencies
pip install -e ".[dev]"
```

## 📖 Usage

### Command Line Interface

```bash
# Show help
python main.py --help

# Generate both performance graphs
python main.py --generate-graphs

# Analyze usage at specific time
python main.py --analyze-time 1500

# Show settled rows over time
python main.py --settled-rows 2048

# Run complete analysis
python main.py --full-analysis

# Use custom parameters
python main.py --total-rows 2048 --write-time 0.5 --settling-time 2
```

### Python API

```python
from src.row_performance_analyzer import calculate_usable_fraction, generate_graph_1

# Calculate usable fraction at 1024ns
fraction = calculate_usable_fraction(1024)
print(f"Usable fraction: {fraction:.3f}")

# Generate performance graph
generate_graph_1()
```

### Examples

```bash
# Run the basic usage example
python examples/basic_usage.py

# Run tests
python -m pytest tests/

# Show configuration summary
python -c "import config; config.print_config_summary()"
```

## 📊 Generated Graphs

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

## ⚙️ System Configurations

The package includes several pre-defined system configurations:

- **default**: Standard 1024-row system with 1ns write time and 1μs settling time
- **high_perf**: High-performance 2048-row system with faster write and settling times
- **low_power**: Low-power 512-row system with slower write and settling times
- **long_settling**: System with extended 5μs settling time
- **fast_write_slow_settling**: System with fast writes but slow settling

## 🧪 Testing

```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage

# Run linting
make lint

# Format code
make format
```

## 🛠️ Development

### Available Make Targets

```bash
make help              # Show all available targets
make install           # Install in development mode
make install-dev       # Install with development dependencies
make test              # Run unit tests
make test-coverage     # Run tests with coverage
make clean             # Clean up generated files
make run-example       # Run the basic usage example
make generate-graphs   # Generate performance graphs
make lint              # Run linting checks
make format            # Format code with black
make quick-analysis    # Run quick analysis
make ci                # Run CI workflow (install, test, lint)
make dev               # Full development workflow
```

### Adding New Features

1. Add new functions to `src/row_performance_analyzer.py`
2. Add tests in `tests/test_analyzer.py`
3. Update `src/__init__.py` to export new functions
4. Add examples in `examples/`
5. Update documentation

## 📈 Analysis Results

The analysis shows that:
- The system has a critical period around 1024ns when most rows are settling
- By 2024ns, all rows have settled and are usable again
- The net change in settled rows over 2048ns is 0 (starts and ends with all rows settled)
- Different system configurations show varying performance characteristics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏢 Organization

This project is part of the Neurophos organization and focuses on architectural modeling and performance analysis for memory systems.

## 📞 Support

For questions and support, please open an issue on GitHub or contact the development team.
