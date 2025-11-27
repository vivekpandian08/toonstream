# Data

Sample datasets for testing and benchmarking.

## Purpose

This folder contains various data structures used for:
- Performance benchmarking
- Format comparison
- Testing edge cases
- Example demonstrations

## Data Types

### Flat Data
Simple records with basic fields:
- Employee records
- User profiles
- Product listings

### Nested Structures
Multi-level hierarchies:
- Orders with items
- Organizations with departments
- Configuration files

### Arrays of Objects
Homogeneous collections (TOON's strength):
- Repository listings
- Transaction logs
- Sensor readings

### Deep Nesting
Complex hierarchical data:
- Configuration trees
- API responses
- Document structures

## Usage

Data files are used by:
- `benchmarks/run_all_comparisons.py` - Performance testing
- `examples/toonstream_tutorial.ipynb` - Tutorial demonstrations
- `tests/` - Integration tests

## File Formats

- `.json` - Standard JSON format
- `.toon` - TOON format (generated)
- `.py` - Python data generators

## Generating Data

Most data is generated programmatically:
```python
# See benchmarks/run_all_comparisons.py
# Data is created inline for each test
```

## Benchmark Datasets

Current datasets used in benchmarks:

1. **flat_data** - 50 employee records
2. **arrays_of_objects** - 100 GitHub repositories
3. **nested_structures** - 10 orders with items
4. **deep_nested** - 20 configuration objects

Each dataset tests different TOON optimization scenarios.
