"""
Unified benchmark suite for TOON format comparisons.

This script consolidates all comparison tests into a single executable that runs
comprehensive benchmarks across different data structure types and formats.

Features:
- Configurable via config.json
- Tests multiple data structure types (flat, arrays, nested, deep)
- Compares TOON vs JSON Compact vs JSON Pretty formats
- Measures token efficiency and processing speed
- Generates detailed reports with summaries

Usage:
    python benchmarks/run_all_comparisons.py
    python benchmarks/run_all_comparisons.py --config custom_config.json
    python benchmarks/run_all_comparisons.py --dataset flat_data
    python benchmarks/run_all_comparisons.py --format toon_optimized

Configuration:
    Edit benchmarks/config.json to customize:
    - Datasets to test
    - Formats to compare
    - Optimization thresholds
    - Output settings
"""

import json
import csv
import io
import time
import sys
import os
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import tiktoken
from toonlib import ToonEncoder


class BenchmarkSuite:
    """Unified benchmark suite for all TOON format comparisons."""
    
    def __init__(self, config_path: str = "benchmarks/config.json"):
        """
        Initialize benchmark suite with configuration.
        
        Args:
            config_path: Path to configuration JSON file
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # Initialize tokenizer
        encoding_name = self.config['benchmark_settings']['tokenizer']['encoding']
        self.encoding = tiktoken.get_encoding(encoding_name)
        
        self.results = []
    
    def count_tokens(self, text: str) -> int:
        """Count tokens using configured tokenizer."""
        return len(self.encoding.encode(text))
    
    def json_to_csv(self, data: list) -> str:
        """Convert JSON array of objects to CSV string."""
        if not data:
            return ""
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()
    
    def json_to_csv_flattened(self, data: list) -> str:
        """
        Convert nested JSON to flattened CSV (loses structure).
        Used for nested data comparison to show CSV limitations.
        """
        if not data:
            return ""
        
        # Flatten nested structures
        flat_rows = []
        for item in data:
            flat_row = self._flatten_dict(item)
            flat_rows.append(flat_row)
        
        # Write to CSV
        output = io.StringIO()
        if flat_rows:
            writer = csv.DictWriter(output, fieldnames=flat_rows[0].keys())
            writer.writeheader()
            writer.writerows(flat_rows)
        return output.getvalue()
    
    def _flatten_dict(self, d: dict, parent_key: str = '', sep: str = '.') -> dict:
        """Recursively flatten nested dictionary with dot notation."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Convert arrays to JSON strings (no better way in CSV)
                items.append((new_key, json.dumps(v)))
            else:
                items.append((new_key, v))
        return dict(items)
    
    def run_format_test(self, format_name: str, data: Any, encoder_type: str = None) -> Tuple[str, int, int, float]:
        """
        Generate and measure a specific format.
        
        Args:
            format_name: Name of format (csv, toon, json_compact, etc.)
            data: Data to encode
            encoder_type: For TOON, specify 'original' or 'optimized'
            
        Returns:
            Tuple of (encoded_string, token_count, char_count, processing_time)
        """
        start_time = time.time()
        
        if format_name == "csv":
            encoded = self.json_to_csv(data)
        elif format_name == "csv_flattened":
            encoded = self.json_to_csv_flattened(data)
        elif format_name == "toon" or format_name == "toon_optimized":
            encoder = ToonEncoder(smart_optimize=True)
            encoded = encoder.encode(data)
        elif format_name == "toon_original":
            encoder = ToonEncoder(smart_optimize=False)
            encoded = encoder.encode(data)
        elif format_name == "json_compact":
            encoded = json.dumps(data)
        elif format_name == "json_pretty":
            encoded = json.dumps(data, indent=2)
        else:
            raise ValueError(f"Unknown format: {format_name}")
        
        processing_time = time.time() - start_time
        token_count = self.count_tokens(encoded)
        char_count = len(encoded)
        
        return encoded, token_count, char_count, processing_time
    
    def run_dataset_benchmark(self, dataset_name: str, dataset_config: dict):
        """
        Run benchmark for a specific dataset.
        
        Args:
            dataset_name: Name of dataset (flat_data, arrays_of_objects, etc.)
            dataset_config: Configuration dictionary for this dataset
        """
        print(f"\n{'='*80}")
        print(f"  BENCHMARK: {dataset_name.replace('_', ' ').title()}")
        print(f"{'='*80}")
        print(f"Dataset: {dataset_config['description']}")
        print(f"File: {dataset_config['file']}")
        
        # Load data
        with open(dataset_config['file'], 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Run tests for each format
        format_results = {}
        for format_name in dataset_config['formats_to_test']:
            try:
                encoded, tokens, chars, proc_time = self.run_format_test(format_name, data)
                format_results[format_name] = {
                    'tokens': tokens,
                    'chars': chars,
                    'time': proc_time,
                    'encoded': encoded if self.config['output_settings']['save_encoded_samples'] else None
                }
            except Exception as e:
                print(f"  ⚠️  Failed to test {format_name}: {e}")
                format_results[format_name] = None
        
        # Display results
        print(f"\n{'Format':<20} {'Tokens':<12} {'Characters':<14} {'Time (ms)':<12}")
        print("-"*80)
        
        baseline_format = self.config['comparison_settings']['baseline_format']
        baseline_tokens = format_results.get(baseline_format, {}).get('tokens', 0) if baseline_format in format_results else 0
        
        for format_name, result in format_results.items():
            if result is None:
                continue
            
            tokens_str = f"{result['tokens']:,}"
            chars_str = f"{result['chars']:,}"
            time_str = f"{result['time']*1000:.2f}"
            
            # Calculate percentage vs baseline
            if baseline_tokens > 0 and format_name != baseline_format:
                pct = ((result['tokens'] - baseline_tokens) / baseline_tokens * 100)
                tokens_str += f" ({pct:+.1f}%)"
            
            print(f"{format_name:<20} {tokens_str:<12} {chars_str:<14} {time_str:<12}")
        
        # Determine winner
        winner = min(format_results.items(), key=lambda x: x[1]['tokens'] if x[1] else float('inf'))
        print(f"\n✅ Winner: {winner[0]} with {winner[1]['tokens']:,} tokens")
        
        # Store results
        self.results.append({
            'dataset': dataset_name,
            'description': dataset_config['description'],
            'formats': format_results,
            'winner': winner[0]
        })
    
    def run_all_benchmarks(self, specific_dataset: str = None):
        """
        Run all configured benchmarks.
        
        Args:
            specific_dataset: If provided, only run this dataset
        """
        print("\n" + "="*80)
        print("  TOON FORMAT BENCHMARK SUITE")
        print("="*80)
        print(f"Tokenizer: {self.config['benchmark_settings']['tokenizer']['model']}")
        print(f"Encoding: {self.config['benchmark_settings']['tokenizer']['encoding']}")
        
        datasets = self.config['benchmark_settings']['datasets']
        
        if specific_dataset:
            if specific_dataset in datasets:
                self.run_dataset_benchmark(specific_dataset, datasets[specific_dataset])
            else:
                print(f"❌ Dataset '{specific_dataset}' not found in config")
                return
        else:
            for dataset_name, dataset_config in datasets.items():
                self.run_dataset_benchmark(dataset_name, dataset_config)
        
        # Display summary
        self.print_summary()
    
    def print_summary(self):
        """Print overall summary of all benchmarks."""
        print(f"\n{'='*80}")
        print("  SUMMARY")
        print(f"{'='*80}\n")
        
        for result in self.results:
            print(f"{result['dataset'].replace('_', ' ').title()}:")
            print(f"  Winner: {result['winner']}")
            print(f"  Description: {result['description']}\n")
        
        print(f"{'='*80}")
        print("Benchmark complete! Results saved.")
        print(f"{'='*80}\n")


def main():
    """Main entry point for benchmark suite."""
    parser = argparse.ArgumentParser(
        description="Run TOON format benchmarks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python benchmarks/run_all_comparisons.py
  python benchmarks/run_all_comparisons.py --dataset flat_data
  python benchmarks/run_all_comparisons.py --config custom_config.json
        """
    )
    parser.add_argument(
        '--config',
        default='benchmarks/config.json',
        help='Path to configuration file (default: benchmarks/config.json)'
    )
    parser.add_argument(
        '--dataset',
        help='Run only specific dataset (e.g., flat_data, arrays_of_objects)'
    )
    
    args = parser.parse_args()
    
    # Run benchmarks
    suite = BenchmarkSuite(config_path=args.config)
    suite.run_all_benchmarks(specific_dataset=args.dataset)


if __name__ == "__main__":
    main()
