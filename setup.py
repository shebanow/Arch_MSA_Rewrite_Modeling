"""
Setup script for Row Performance Analyzer

This script allows the project to be installed as a Python package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Row Performance Analyzer - Performance analysis and modeling for row usage patterns with settling time constraints"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ['numpy>=1.20.0', 'matplotlib>=3.3.0']

setup(
    name="row-performance-analyzer",
    version="1.0.0",
    author="Neurophos",
    author_email="",
    description="Performance analysis and modeling for row usage patterns with settling time constraints",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/shebanow/Arch_MSA_Rewrite_Modeling",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "row-analyzer=row_performance_analyzer:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="performance analysis memory architecture settling time row usage",
    project_urls={
        "Bug Reports": "https://github.com/shebanow/Arch_MSA_Rewrite_Modeling/issues",
        "Source": "https://github.com/shebanow/Arch_MSA_Rewrite_Modeling",
        "Documentation": "https://github.com/shebanow/Arch_MSA_Rewrite_Modeling#readme",
    },
)
