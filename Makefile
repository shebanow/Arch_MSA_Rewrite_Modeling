# Makefile for Row Performance Analyzer

.PHONY: help install test clean run-example generate-graphs lint format docs

# Default target
help:
	@echo "Available targets:"
	@echo "  install        - Install the package in development mode"
	@echo "  test           - Run unit tests"
	@echo "  clean          - Clean up generated files"
	@echo "  run-example    - Run the basic usage example"
	@echo "  generate-graphs - Generate performance graphs"
	@echo "  lint           - Run linting checks"
	@echo "  format         - Format code with black"
	@echo "  docs           - Generate documentation"

# Install the package in development mode
install:
	pip install -e .

# Install development dependencies
install-dev:
	pip install -e ".[dev]"

# Run unit tests
test:
	python -m pytest tests/ -v

# Run tests with coverage
test-coverage:
	python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# Clean up generated files
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Run the basic usage example
run-example:
	python examples/basic_usage.py

# Generate performance graphs
generate-graphs:
	python main.py --generate-graphs

# Run full analysis
full-analysis:
	python main.py --full-analysis

# Run linting checks
lint:
	flake8 src/ tests/ examples/ main.py config.py
	mypy src/ main.py config.py

# Format code with black
format:
	black src/ tests/ examples/ main.py config.py

# Generate documentation
docs:
	@echo "Documentation generation not yet implemented"
	@echo "See README.md for current documentation"

# Show configuration summary
config-summary:
	python -c "import config; config.print_config_summary()"

# Run quick analysis
quick-analysis:
	python main.py --analyze-time 1024
	python main.py --settled-rows 2048

# Install and run tests
ci: install-dev test lint

# Development workflow
dev: install-dev format lint test
