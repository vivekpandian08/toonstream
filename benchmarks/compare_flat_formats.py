"""
Compare token counts between CSV, TOON, and JSON formats for flat tabular data.

This script demonstrates TOON's performance on flat, tabular data (like database tables)
where CSV is traditionally the most efficient format. The results show that TOON
achieves near-parity with CSV in token efficiency.

Test Data: 50 employee records with uniform fields
Tokenizer: tiktoken (OpenAI's GPT-3.5-turbo cl100k_base encoding)

Expected Results:
- CSV: ~1,729 tokens (baseline for flat data)
- TOON: ~1,733 tokens (+0.2%, essentially tied)
- JSON Compact: ~2,614 tokens (+51%)
- JSON Pretty: ~4,614 tokens (+167%)

Key Insight: For flat tabular data, TOON matches CSV efficiency while
maintaining the structure and readability advantages of object notation.
"""

import json
import csv
import io
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import tiktoken
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


def json_to_csv(data: list) -> str:
    """
    Convert JSON array of objects to CSV string.
    
    Assumes all objects have the same fields (homogeneous structure).
    
    Args:
        data: List of dictionaries
        
    Returns:
        CSV-formatted string with header row
    """
    if not data:
        return ""
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()

def main():
    # Load the flat dataset
    with open('data/employees-flat.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("\n" + "="*70)
    print("  CSV vs TOON vs JSON - TOKEN COMPARISON (Flat Tabular Data)")
    print("="*70)
    print(f"\nDataset: 50 Employee Records")
    print(f"Tokenizer: tiktoken (GPT-3.5-turbo / cl100k_base encoding)")
    
    # Generate CSV format
    csv_content = json_to_csv(data)
    csv_tokens = count_tokens(csv_content)
    csv_chars = len(csv_content)
    
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
    
    print("\n" + "-"*70)
    print("RESULTS:")
    print("-"*70)
    
    # CSV Results
    print(f"\n1. CSV Format:")
    print(f"   Tokens: {csv_tokens:,}")
    print(f"   Characters: {csv_chars:,}")
    
    # TOON Results
    print(f"\n2. TOON Format:")
    print(f"   Tokens: {toon_tokens:,}")
    print(f"   Characters: {toon_chars:,}")
    
    # JSON Pretty Results
    print(f"\n3. JSON (Pretty):")
    print(f"   Tokens: {json_pretty_tokens:,}")
    print(f"   Characters: {json_pretty_chars:,}")
    
    # JSON Compact Results
    print(f"\n4. JSON (Compact):")
    print(f"   Tokens: {json_compact_tokens:,}")
    print(f"   Characters: {json_compact_chars:,}")
    
    print("\n" + "-"*70)
    print("TOKEN SAVINGS COMPARISON:")
    print("-"*70)
    
    # CSV vs others
    print(f"\nCSV as baseline:")
    toon_vs_csv = ((csv_tokens - toon_tokens) / csv_tokens * 100)
    json_pretty_vs_csv = ((csv_tokens - json_pretty_tokens) / csv_tokens * 100)
    json_compact_vs_csv = ((csv_tokens - json_compact_tokens) / csv_tokens * 100)
    
    print(f"  TOON vs CSV:         {toon_tokens - csv_tokens:+,} tokens ({toon_vs_csv:+.1f}%)")
    print(f"  JSON Pretty vs CSV:  {json_pretty_tokens - csv_tokens:+,} tokens ({json_pretty_vs_csv:+.1f}%)")
    print(f"  JSON Compact vs CSV: {json_compact_tokens - csv_tokens:+,} tokens ({json_compact_vs_csv:+.1f}%)")
    
    # TOON vs JSON
    print(f"\nTOON vs JSON:")
    toon_vs_pretty = ((json_pretty_tokens - toon_tokens) / json_pretty_tokens * 100)
    toon_vs_compact = ((json_compact_tokens - toon_tokens) / json_compact_tokens * 100)
    
    print(f"  TOON vs JSON Pretty:  {json_pretty_tokens - toon_tokens:,} tokens saved ({toon_vs_pretty:.1f}% reduction)")
    print(f"  TOON vs JSON Compact: {json_compact_tokens - toon_tokens:,} tokens saved ({toon_vs_compact:.1f}% reduction)")
    
    # Best format
    print("\n" + "-"*70)
    print("WINNER:")
    print("-"*70)
    
    formats = [
        ("CSV", csv_tokens),
        ("TOON", toon_tokens),
        ("JSON Pretty", json_pretty_tokens),
        ("JSON Compact", json_compact_tokens)
    ]
    formats.sort(key=lambda x: x[1])
    
    winner = formats[0]
    print(f"\n  🏆 {winner[0]}: {winner[1]:,} tokens (Most Efficient)")
    
    for i, (name, tokens) in enumerate(formats[1:], 2):
        diff = tokens - winner[1]
        pct = (diff / winner[1] * 100)
        print(f"  {i}. {name}: {tokens:,} tokens (+{diff:,}, +{pct:.1f}%)")
    
    print("\n" + "="*70)
    
    # Show sample output for each format
    print("\nSAMPLE OUTPUT (First 3 records):")
    print("-"*70)
    
    sample_data = data[:3]
    
    print("\nCSV:")
    print(json_to_csv(sample_data)[:500] + "..." if len(json_to_csv(sample_data)) > 500 else json_to_csv(sample_data))
    
    print("\nTOON:")
    toon_sample = encoder.encode(sample_data)
    print(toon_sample[:500] + "..." if len(toon_sample) > 500 else toon_sample)
    
    print("\nJSON (Compact):")
    json_sample = json.dumps(sample_data)
    print(json_sample[:500] + "..." if len(json_sample) > 500 else json_sample)
    
    print("\n" + "="*70)
    
    # Save detailed results
    results = {
        "dataset": "employees-flat.json (50 records)",
        "tokenizer": "tiktoken (cl100k_base)",
        "formats": {
            "csv": {"tokens": csv_tokens, "characters": csv_chars},
            "toon": {"tokens": toon_tokens, "characters": toon_chars},
            "json_pretty": {"tokens": json_pretty_tokens, "characters": json_pretty_chars},
            "json_compact": {"tokens": json_compact_tokens, "characters": json_compact_chars}
        },
        "comparisons": {
            "toon_vs_csv_tokens": toon_tokens - csv_tokens,
            "toon_vs_csv_percent": toon_vs_csv,
            "toon_vs_json_pretty_tokens": json_pretty_tokens - toon_tokens,
            "toon_vs_json_pretty_percent": toon_vs_pretty,
            "toon_vs_json_compact_tokens": json_compact_tokens - toon_tokens,
            "toon_vs_json_compact_percent": toon_vs_compact
        },
        "winner": winner[0]
    }
    
    return results

if __name__ == "__main__":
    results = main()
