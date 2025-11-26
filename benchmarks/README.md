# TOON Benchmarks

This directory contains benchmark scripts and configuration for testing TOON format performance.

## Quick Start

Run all benchmarks:
```bash
python benchmarks/run_all_comparisons.py
```

Run specific dataset:
```bash
python benchmarks/run_all_comparisons.py --dataset flat_data
```

## Files

### Main Benchmark Suite
- **`run_all_comparisons.py`** - Unified benchmark script (recommended)
  - Runs all comparisons from a single script
  - Configurable via config.json
  - Generates comprehensive reports

### Configuration
- **`config.json`** - Benchmark configuration
  - Dataset paths and descriptions
  - Formats to test
  - Optimization thresholds
  - Output settings

### Individual Comparison Scripts (Legacy)
These are the original standalone comparison scripts, now consolidated into `run_all_comparisons.py`:

- **`compare_flat_formats.py`** - CSV vs TOON vs JSON (flat tabular data)
- **`compare_nested_formats.py`** - Complex nested structures comparison
- **`compare_deep_nested.py`** - Deeply nested configuration comparison
- **`test_optimization.py`** - Original vs Optimized encoder comparison

## Configuration

Edit `config.json` to customize:

```json
{
  "benchmark_settings": {
    "tokenizer": {
      "model": "gpt-3.5-turbo",
      "encoding": "cl100k_base"
    },
    "datasets": {
      "flat_data": {
        "file": "data/employees-flat.json",
        "formats_to_test": ["csv", "toon", "json_compact"]
      }
    },
    "optimization_thresholds": {
      "min_array_size_for_tabular": 3,
      "max_field_heterogeneity": 0.3,
      "max_nesting_depth_for_tabular": 3
    }
  }
}
```

## Benchmark Results

### Flat Tabular Data (50 employees)
- **CSV**: 1,729 tokens (winner)
- **TOON**: 1,733 tokens (+0.2%)
- **JSON Compact**: 2,614 tokens (+51.3%)

### Arrays of Objects (100 repos)
- **TOON**: 2,915 tokens (winner, -38.2% vs JSON)
- **JSON Compact**: 4,715 tokens

### Nested Structures (10 orders)
- **TOON**: 2,915 tokens (winner)
- **JSON Compact**: 2,926 tokens (+0.4%)

### Deep Nested Configs (20 services)
- **TOON Optimized**: 7,393 tokens (tie)
- **JSON Compact**: 7,393 tokens (tie)
- **TOON Original**: 7,884 tokens (+6.6% worse)

## Optimization Guide

The optimized encoder uses smart detection:

1. **Minimum Array Size** (3+ items)
   - Small arrays use JSON inline
   - Header overhead only justified for 3+ items

2. **Homogeneity Check** (>70% common fields)
   - Skip tabular if objects are too different
   - Avoids sparse tables with many empty cells

3. **Nesting Depth Limit** (≤3 levels)
   - Deep configs stay as JSON
   - Nested values become JSON anyway

## Key Insights

✅ **Use TOON for:**
- Arrays of 3+ objects with shared structure
- Flat tabular data (matches CSV efficiency)
- Mixed nested structures with arrays

⚠️ **Use JSON Compact for:**
- Deep nested configs (TOON Optimized ties)
- Small arrays (1-2 items)
- Highly heterogeneous objects

📊 **Overall Performance:**
- Arrays: 38-55% token savings
- Flat data: ±1% (essentially ties CSV)
- Deep configs: ±0% (ties with optimization)
- Processing: 1.62x faster average (optimized)
