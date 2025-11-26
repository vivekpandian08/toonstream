"""
Setup script for toonlib package.

Installation:
    pip install -e .  # Development install
    pip install .     # Regular install
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="toonlib",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Token Oriented Object Notation - Efficient data serialization for LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/toonlib",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies for core functionality
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
        "test": [
            "tiktoken>=0.5.0",  # For token comparison tests
        ],
    },
    entry_points={
        "console_scripts": [
            # Add CLI tools here if needed
        ],
    },
    keywords="toon json serialization tokens llm optimization csv tabular",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/toonlib/issues",
        "Source": "https://github.com/yourusername/toonlib",
        "Documentation": "https://github.com/yourusername/toonlib#readme",
    },
)
