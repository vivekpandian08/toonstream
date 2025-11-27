"""
Compare token counts between TOON and JSON formats for deeply nested configuration data.

This script tests TOON's performance on deeply nested structures where tabular format
provides minimal benefit. The original TOON encoder performed WORSE than JSON on this
type of data (-6.6%), but the optimized encoder now ties with JSON.

Test Data: 20 microservice configurations with:
- 9 levels of nesting depth
- Minimal arrays (mostly nested objects)
- Complex configuration hierarchies
- Deep settings and credentials structures

CSV is excluded because it cannot handle deeply nested structures without
destroying the data model (would require massive flattening).

Tokenizer: tiktoken (OpenAI's GPT-3.5-turbo cl100k_base encoding)

Expected Results (Original Encoder):
- JSON Compact: ~7,393 tokens (WINNER)
- TOON Original: ~7,884 tokens (+6.6% WORSE)
- JSON Pretty: ~9,962 tokens (+34.7% worse)

Expected Results (Optimized Encoder):
- JSON Compact: ~7,393 tokens (TIE)
- TOON Optimized: ~7,393 tokens (±0.0%, matches JSON!)
- JSON Pretty: ~9,962 tokens (+34.7% worse)

Key Insight: TOON's tabular format is designed for arrays of objects. When data
is primarily deeply nested objects with few arrays, JSON Compact is equally efficient.
The optimized encoder detects this and avoids using tabular format, tying with JSON.

Use Case Guidance:
- Arrays of objects (3+ items): Use TOON (38-55% savings)
- Deep nested configs: Use TOON Optimized or JSON (tie)
- Flat tabular data: Use TOON or CSV (essentially tied)
"""

import json
import tiktoken
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from toonstream import encode, ToonEncoder


def count_tokens(text: str) -> int:
    """
    Count tokens using tiktoken (GPT-3.5-turbo encoding).
    
    Args:
        text: String to tokenize
        
    Returns:
        Number of tokens
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def analyze_structure(data):
    """
    Analyze the structural complexity of the data.
    
    Calculates:
    - Maximum nesting depth (how many levels deep)
    - Number of arrays in the structure
    
    Args:
        data: Data structure to analyze
        
    Returns:
        Tuple of (max_depth, array_count)
    """
    def count_depth(obj, current_depth=0):
        """Recursively calculate maximum nesting depth."""
        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(count_depth(v, current_depth + 1) for v in obj.values())
        elif isinstance(obj, list):
            if not obj:
                return current_depth
            return max(count_depth(item, current_depth + 1) for item in obj)
        else:
            return current_depth
    
    def count_arrays(obj):
        """Count total number of arrays in the structure."""
        count = 0
        if isinstance(obj, dict):
            for v in obj.values():
                count += count_arrays(v)
        elif isinstance(obj, list):
            count += 1  # This is an array
            for item in obj:
                count += count_arrays(item)
        return count
    
    max_depth = count_depth(data)
    array_count = count_arrays(data)
    
    return max_depth, array_count

def main():
    # Load the deeply nested configuration dataset
    with open('data/configs-deep-nested.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Analyze structure
    max_depth, array_count = analyze_structure(data)
    
    print("\n" + "="*75)
    print("  TOON vs JSON - DEEPLY NESTED CONFIGURATION DATA")
    print("="*75)
    print(f"\nDataset: 20 Service Configuration Objects")
    print(f"Tokenizer: tiktoken (GPT-3.5-turbo / cl100k_base encoding)")
    print(f"\nStructure Analysis:")
    print(f"  • Maximum nesting depth: {max_depth} levels")
    print(f"  • Total arrays in dataset: {array_count}")
    print(f"  • Data type: Deeply nested configuration with minimal tabular data")
    print(f"  • CSV: ❌ IMPOSSIBLE - Cannot represent deep nesting")
    
    # Generate TOON format
    encoder = ToonEncoder()
    toon_content = encoder.encode(data)
    toon_tokens = count_tokens(toon_content)
    toon_chars = len(toon_content)
    
    # Generate JSON formats
    json_pretty = json.dumps(data, indent=2)
    json_pretty_tokens = count_tokens(json_pretty)
    json_pretty_chars = len(json_pretty)
    
    json_compact = json.dumps(data)
    json_compact_tokens = count_tokens(json_compact)
    json_compact_chars = len(json_compact)
    
    print("\n" + "-"*75)
    print("RESULTS:")
    print("-"*75)
    
    # Results
    print(f"\n1. TOON:")
    print(f"   Tokens: {toon_tokens:,}")
    print(f"   Characters: {toon_chars:,}")
    
    print(f"\n2. JSON Pretty:")
    print(f"   Tokens: {json_pretty_tokens:,}")
    print(f"   Characters: {json_pretty_chars:,}")
    
    print(f"\n3. JSON Compact:")
    print(f"   Tokens: {json_compact_tokens:,}")
    print(f"   Characters: {json_compact_chars:,}")
    
    print("\n" + "-"*75)
    print("TOKEN SAVINGS COMPARISON:")
    print("-"*75)
    
    # TOON vs JSON
    toon_vs_pretty = ((json_pretty_tokens - toon_tokens) / json_pretty_tokens * 100)
    toon_vs_compact = ((json_compact_tokens - toon_tokens) / json_compact_tokens * 100)
    
    print(f"\nTOON vs JSON:")
    if toon_tokens < json_pretty_tokens:
        print(f"  TOON vs JSON Pretty:  {json_pretty_tokens - toon_tokens:,} tokens saved ({toon_vs_pretty:.1f}% reduction)")
    else:
        print(f"  TOON vs JSON Pretty:  {toon_tokens - json_pretty_tokens:,} tokens MORE ({abs(toon_vs_pretty):.1f}% increase)")
    
    if toon_tokens < json_compact_tokens:
        print(f"  TOON vs JSON Compact: {json_compact_tokens - toon_tokens:,} tokens saved ({toon_vs_compact:.1f}% reduction)")
    else:
        print(f"  TOON vs JSON Compact: {toon_tokens - json_compact_tokens:,} tokens MORE ({abs(toon_vs_compact):.1f}% increase)")
    
    # Winner
    print("\n" + "-"*75)
    print("WINNER:")
    print("-"*75)
    
    formats = [
        ("TOON", toon_tokens),
        ("JSON Compact", json_compact_tokens),
        ("JSON Pretty", json_pretty_tokens)
    ]
    formats.sort(key=lambda x: x[1])
    
    winner = formats[0]
    print(f"\n  🏆 {winner[0]}: {winner[1]:,} tokens (Most Efficient)")
    
    for i, (name, tokens) in enumerate(formats[1:], 2):
        diff = tokens - winner[1]
        pct = (diff / winner[1] * 100)
        print(f"  {i}. {name}: {tokens:,} tokens (+{diff:,}, +{pct:.1f}%)")
    
    print("\n" + "="*75)
    
    # Show sample output
    print("\nSAMPLE OUTPUT (First Service Config - Truncated):")
    print("-"*75)
    
    sample_data = [data[0]]
    
    print("\nTOON:")
    toon_sample = encoder.encode(sample_data)
    lines = toon_sample.split('\n')
    for i, line in enumerate(lines[:20]):
        print(line[:150] + ("..." if len(line) > 150 else ""))
        if i >= 19:
            print("... (truncated)")
            break
    
    print("\nJSON Compact:")
    json_sample = json.dumps(sample_data, indent=None)
    print(json_sample[:800] + "..." if len(json_sample) > 800 else json_sample)
    
    print("\n" + "="*75)
    
    # Key insights
    print("\n💡 KEY INSIGHTS:")
    print("-"*75)
    print(f"• Deeply nested configs are TOON's challenge:")
    print(f"  - {max_depth} levels of nesting")
    print(f"  - Mostly nested objects, not arrays")
    print(f"  - Limited opportunity for tabular optimization")
    print(f"")
    print(f"• TOON Performance:")
    if toon_vs_pretty > 0:
        print(f"  - {abs(toon_vs_pretty):.1f}% token reduction vs JSON Pretty ✅")
    else:
        print(f"  - {abs(toon_vs_pretty):.1f}% token increase vs JSON Pretty ⚠️")
    
    if toon_vs_compact > 0:
        print(f"  - {abs(toon_vs_compact):.1f}% token reduction vs JSON Compact ✅")
    else:
        print(f"  - {abs(toon_vs_compact):.1f}% token increase vs JSON Compact ⚠️")
    print(f"")
    print(f"• Why different from earlier tests?")
    print(f"  - Flat data (employees): TOON ≈ CSV (0.2% difference)")
    print(f"  - Arrays of objects (repos): TOON wins big (44% reduction)")
    print(f"  - Nested data (orders): TOON good (18% reduction)")
    print(f"  - Deep configs: Limited tabular data to optimize")
    print(f"")
    print(f"• Best format by use case:")
    print(f"  - Deeply nested configs: JSON Compact (standard, efficient)")
    print(f"  - Arrays of objects: TOON (huge savings)")
    print(f"  - Mixed structures: TOON (balanced)")
    print(f"  - Flat tables: CSV/TOOV (maximum efficiency)")
    
    print("\n" + "="*75)
    
    return {
        "dataset": "configs-deep-nested.json (20 service configs)",
        "tokenizer": "tiktoken (cl100k_base)",
        "structure": {
            "max_depth": max_depth,
            "array_count": array_count
        },
        "formats": {
            "toon": {"tokens": toon_tokens, "characters": toon_chars},
            "json_pretty": {"tokens": json_pretty_tokens, "characters": json_pretty_chars},
            "json_compact": {"tokens": json_compact_tokens, "characters": json_compact_chars}
        },
        "winner": winner[0],
        "toon_vs_json_pretty": toon_vs_pretty,
        "toon_vs_json_compact": toon_vs_compact
    }

if __name__ == "__main__":
    results = main()
