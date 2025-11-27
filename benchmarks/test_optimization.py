"""
Compare original TOON encoder vs optimized encoder across different datasets.

This script validates the optimization improvements made to the TOON encoder.
The original encoder had a 6.6% penalty on deeply nested configurations, which
the optimized encoder fixes using smart array detection.

Optimization Strategy:
1. **Minimum Array Size**: Skip tabular for arrays <3 items (header overhead too high)
2. **Homogeneity Check**: Skip tabular if >30% fields unique (too many empty cells)
3. **Nesting Depth Limit**: Skip tabular if >3 levels deep (nested JSON values anyway)
4. **Performance Boosts**: Pre-allocation, early returns, conditional escaping

Test Datasets:
1. Flat tabular data (50 employees) - Tests CSV-like structures
2. Arrays of objects (100 GitHub repos) - Tests TOON's core strength
3. Nested data (10 orders) - Tests mixed nested structures
4. Deep nested configs (20 services) - Tests optimization fix

Expected Results:
- Flat/Arrays/Nested: Original and Optimized perform identically (±0.0%)
- Deep configs: Original -6.6% vs JSON, Optimized ±0.0% vs JSON (+6.2% improvement!)
- Processing speed: 1.62x faster average, 3.82x faster on deep configs

Usage:
    python test_optimization.py
    
Output:
    Detailed comparison for each dataset plus summary table and recommendations.
"""

import json
import time
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import tiktoken
from toonstream import ToonEncoder


def count_tokens(text: str) -> int:
    """
    Count tokens using tiktoken (GPT-3.5-turbo encoding).
    
    Args:
        text: String to tokenize
        
    Returns:
        Number of tokens (same tokenizer used by ChatGPT)
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def test_dataset(name: str, filepath: str):
    """
    Test a dataset with both original and optimized encoders.
    
    Compares token efficiency and processing speed between:
    - JSON Compact (baseline)
    - Original TOON encoder (always uses tabular for arrays)
    - Optimized TOON encoder (smart detection)
    
    Args:
        name: Human-readable dataset name
        filepath: Path to JSON file
        
    Returns:
        Dictionary with detailed results for summary table
    """
    print(f"\n{'='*75}")
    print(f"  Testing: {name}")
    print(f"{'='*75}")
    
    # Load test data
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # JSON baseline (for comparison)
    json_compact = json.dumps(data)
    json_compact_tokens = count_tokens(json_compact)
    json_compact_chars = len(json_compact)
    
    # Original TOON encoder (always uses tabular for arrays)
    encoder_original = ToonEncoder()
    start_time = time.time()
    toon_original = encoder_original.encode(data)
    time_original = time.time() - start_time
    toon_original_tokens = count_tokens(toon_original)
    toon_original_chars = len(toon_original)
    
    # Optimized TOON encoder (smart array detection enabled)
    encoder_optimized = ToonEncoder(smart_optimize=True)
    start_time = time.time()
    toon_optimized = encoder_optimized.encode(data)
    time_optimized = time.time() - start_time
    toon_optimized_tokens = count_tokens(toon_optimized)
    toon_optimized_chars = len(toon_optimized)
    
    # Calculate token savings percentages
    # Positive % = TOON saved tokens (better than JSON)
    # Negative % = TOON used more tokens (worse than JSON)
    original_vs_json = ((json_compact_tokens - toon_original_tokens) / json_compact_tokens * 100)
    optimized_vs_json = ((json_compact_tokens - toon_optimized_tokens) / json_compact_tokens * 100)
    optimized_vs_original = ((toon_original_tokens - toon_optimized_tokens) / toon_original_tokens * 100)
    
    # Display detailed results
    print(f"\nJSON Compact:         {json_compact_tokens:,} tokens | {json_compact_chars:,} chars")
    print(f"TOON Original:        {toon_original_tokens:,} tokens | {toon_original_chars:,} chars | {time_original*1000:.2f}ms")
    print(f"TOON Optimized:       {toon_optimized_tokens:,} tokens | {toon_optimized_chars:,} chars | {time_optimized*1000:.2f}ms")
    
    print(f"\nToken Savings vs JSON:")
    print(f"  Original encoder:   {original_vs_json:+.1f}%")
    print(f"  Optimized encoder:  {optimized_vs_json:+.1f}%")
    print(f"  Optimization gain:  {optimized_vs_original:+.1f}%")
    
    print(f"\nProcessing Speed:")
    speedup = (time_original / time_optimized) if time_optimized > 0 else 1.0
    print(f"  {speedup:.2f}x {'faster' if speedup > 1 else 'slower'} than original")
    
    # Determine winner and display recommendation
    if toon_optimized_tokens < json_compact_tokens and toon_optimized_tokens < toon_original_tokens:
        winner = "✅ Optimized TOON (best efficiency + performance)"
    elif toon_optimized_tokens < json_compact_tokens:
        winner = "✅ Optimized TOON (better than JSON)"
    elif json_compact_tokens < toon_optimized_tokens:
        winner = "⚠️  JSON Compact (most efficient)"
    else:
        winner = "➖ Tie (JSON and TOON equally efficient)"
    
    print(f"\nWinner: {winner}")
    
    # Return detailed results for summary table
    return {
        'name': name,
        'json_tokens': json_compact_tokens,
        'original_tokens': toon_original_tokens,
        'optimized_tokens': toon_optimized_tokens,
        'original_vs_json': original_vs_json,
        'optimized_vs_json': optimized_vs_json,
        'optimized_vs_original': optimized_vs_original,
        'time_original': time_original,
        'time_optimized': time_optimized,
        'speedup': speedup
    }

def main():
    """
    Run optimization comparison tests across all datasets.
    
    Tests four different data structure types:
    1. Flat tabular data - TOON's traditional use case
    2. Arrays of objects - TOON's core strength
    3. Nested structures - Mixed complexity
    4. Deep nested configs - Tests the optimization fix
    
    Outputs:
    - Detailed results for each dataset
    - Summary table comparing all datasets
    - Optimization explanation and recommendations
    """
    print("\n" + "="*75)
    print("  TOON ENCODER OPTIMIZATION COMPARISON")
    print("="*75)
    print("\nTesting original vs optimized encoder across different data structures...")
    
    results = []
    
    # Test 1: Flat tabular data (optimal for CSV/TOON)
    results.append(test_dataset("Flat Tabular Data (50 employees)", "data/employees-flat.json"))
    
    # Test 2: Arrays of objects (TOON's core strength)
    results.append(test_dataset("Arrays of Objects (100 GitHub repos)", "data/github-repos.json"))
    
    # Test 3: Nested structures with arrays (mixed complexity)
    results.append(test_dataset("Nested with Arrays (10 orders)", "data/orders-nested.json"))
    
    # Test 4: Deep nested configs (tests the optimization fix)
    results.append(test_dataset("Deep Nested Configs (20 services)", "data/configs-deep-nested.json"))
    
    # Display summary table
    print(f"\n{'='*75}")
    print("  OPTIMIZATION SUMMARY")
    print(f"{'='*75}")
    
    print(f"\n{'Dataset':<35} {'Orig→JSON':<12} {'Opt→JSON':<12} {'Opt→Orig':<12} {'Speedup':<10}")
    print("-"*75)
    
    for r in results:
        name = r['name'][:33]
        orig_json = f"{r['original_vs_json']:+.1f}%"
        opt_json = f"{r['optimized_vs_json']:+.1f}%"
        opt_orig = f"{r['optimized_vs_original']:+.1f}%"
        speedup = f"{r['speedup']:.2f}x"
        
        print(f"{name:<35} {orig_json:<12} {opt_json:<12} {opt_orig:<12} {speedup:<10}")
    
    # Calculate averages across all datasets
    avg_original_vs_json = sum(r['original_vs_json'] for r in results) / len(results)
    avg_optimized_vs_json = sum(r['optimized_vs_json'] for r in results) / len(results)
    avg_optimized_vs_original = sum(r['optimized_vs_original'] for r in results) / len(results)
    avg_speedup = sum(r['speedup'] for r in results) / len(results)
    
    print("-"*75)
    print(f"{'AVERAGE':<35} {avg_original_vs_json:+.1f}%{'':<7} {avg_optimized_vs_json:+.1f}%{'':<7} {avg_optimized_vs_original:+.1f}%{'':<7} {avg_speedup:.2f}x")
    
    # Display optimization details and recommendations
    print(f"\n{'='*75}")
    print("  KEY OPTIMIZATIONS APPLIED")
    print(f"{'='*75}")
    print("""
1. Smart Array Detection:
   - Only tabularize arrays with 3+ items
   - Small arrays (1-2 items) use JSON inline (header overhead too high)
   
2. Homogeneity Check:
   - Skip tabular for heterogeneous objects (>30% unique fields)
   - Avoids sparse tables with many empty cells
   
3. Nesting Depth Limit:
   - Don't tabularize if items are deeply nested (>3 levels)
   - Deep configs stay as JSON (more efficient)
   
4. Performance Optimizations:
   - Pre-allocated lists for better memory usage
   - Early returns in value formatting
   - Single join operations instead of multiple string concatenations
   - Conditional escaping (only when needed)
    """)
    
    print(f"{'='*75}\n")

if __name__ == "__main__":
    main()
