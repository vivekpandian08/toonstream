# Results

Benchmark results and performance comparisons.

## Files

- `comparison_results_*.json` - JSON format results from benchmark runs
- `comparison_results_*.md` - Human-readable markdown reports

## Format

Each result file contains:
- **Dataset name** and description
- **Size comparison** (characters and tokens)
- **Compression ratio** for each format
- **Relative performance** percentages

## Reading Results

Results show token count comparisons:
```
Format: toon
  Characters: 12,345 (45.2% of JSON compact)
  Tokens: 3,456 (38.7% of JSON compact)
```

Negative percentages = smaller/better
Positive percentages = larger/worse

## Typical Results

| Data Type | TOON vs JSON Compact |
|-----------|---------------------|
| Flat data (employees) | **-55% tokens** |
| Arrays (repos) | **-38% tokens** |
| Nested (orders) | **-15% tokens** |
| Deep nested | **~0% tokens** |

## Regenerating Results

```bash
python benchmarks/run_all_comparisons.py
```

New results are timestamped automatically.
