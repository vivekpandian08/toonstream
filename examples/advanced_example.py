"""
Advanced example demonstrating toonstream advanced features.
Shows error handling, edge cases, and performance considerations.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import toonstream
from toonstream import ToonEncodeError, ToonDecodeError


def example_error_handling():
    """Demonstrate error handling."""
    print("1. Error Handling")
    print("-" * 60)
    
    # Example: Encoding unsupported type
    print("Attempting to encode unsupported type...")
    try:
        class CustomClass:
            pass
        toonstream.encode(CustomClass())
    except ToonEncodeError as e:
        print(f"✓ Caught ToonEncodeError: {e}")
    print()
    
    # Example: Encoding NaN
    print("Attempting to encode NaN...")
    try:
        toonstream.encode(float('nan'))
    except ToonEncodeError as e:
        print(f"✓ Caught ToonEncodeError: {e}")
    print()
    
    # Example: Decoding invalid TOON
    print("Attempting to decode invalid TOON...")
    try:
        toonstream.decode("{invalid: data}")
    except ToonDecodeError as e:
        print(f"✓ Caught ToonDecodeError: {e}")
    print()
    
    # Example: Decoding unterminated string
    print("Attempting to decode unterminated string...")
    try:
        toonstream.decode('"unterminated string')
    except ToonDecodeError as e:
        print(f"✓ Caught ToonDecodeError: {e}")
    print()


def example_edge_cases():
    """Demonstrate edge cases."""
    print("2. Edge Cases")
    print("-" * 60)
    
    # Empty collections
    edge_cases = {
        "empty_object": {},
        "empty_array": [],
        "empty_string": "",
        "zero": 0,
        "false": False,
        "null": None
    }
    
    print("Testing edge cases:")
    for key, value in edge_cases.items():
        toon = toonstream.encode(value, indent=0)
        decoded = toonstream.decode(toon)
        match = "✓" if value == decoded or (value is None and decoded is None) else "✗"
        print(f"  {match} {key}: {repr(value)} → {toon} → {repr(decoded)}")
    print()
    
    # Special keys (note: newlines in keys are not supported by design)
    special_keys = {
        "key with spaces": "value",
        'key"with"quotes': "value",
        "key_with_unicode_😀": "value"
    }
    
    print("Testing special keys:")
    toon = toonstream.encode(special_keys, indent=0)
    decoded = toonstream.decode(toon)
    print(f"  ✓ All special keys preserved: {special_keys == decoded}")
    print()


def example_json_compatibility():
    """Demonstrate JSON compatibility."""
    print("3. JSON Compatibility")
    print("-" * 60)
    
    # Complex data structure
    data = {
        "users": [
            {
                "id": 1,
                "name": "Alice",
                "email": "alice@example.com",
                "active": True,
                "balance": 1234.56,
                "tags": ["premium", "verified"]
            },
            {
                "id": 2,
                "name": "Bob",
                "email": "bob@example.com",
                "active": False,
                "balance": 0.0,
                "tags": []
            }
        ],
        "metadata": {
            "total_users": 2,
            "generated_at": "2025-11-25T12:00:00Z",
            "version": "1.0.0"
        }
    }
    
    # Convert to JSON
    json_str = json.dumps(data, indent=2)
    print("Original JSON:")
    print(json_str)
    print()
    
    # Convert JSON to Python to TOON
    json_data = json.loads(json_str)
    toon_str = toonstream.encode(json_data, indent=2)
    print("TOON format:")
    print(toon_str)
    print()
    
    # Convert TOON back to Python to JSON
    toon_data = toonstream.decode(toon_str)
    json_str_back = json.dumps(toon_data, indent=2)
    
    # Verify round-trip
    original = json.loads(json_str)
    final = json.loads(json_str_back)
    print(f"✓ JSON → TOON → JSON round-trip successful: {original == final}")
    print()


def example_formatting_options():
    """Demonstrate formatting options."""
    print("4. Formatting Options")
    print("-" * 60)
    
    data = {
        "zebra": 1,
        "apple": 2,
        "mango": 3,
        "banana": 4
    }
    
    # Compact format
    compact = toonstream.encode(data, indent=0)
    print("Compact format (indent=0):")
    print(compact)
    print()
    
    # Pretty format with 2-space indent
    pretty2 = toonstream.encode(data, indent=2)
    print("Pretty format (indent=2):")
    print(pretty2)
    print()
    
    # Pretty format with 4-space indent
    pretty4 = toonstream.encode(data, indent=4)
    print("Pretty format (indent=4):")
    print(pretty4)
    print()
    
    # Sorted keys
    sorted_keys = toonstream.encode(data, indent=2, sort_keys=True)
    print("Sorted keys:")
    print(sorted_keys)
    print()


def example_nested_structures():
    """Demonstrate deeply nested structures."""
    print("5. Deeply Nested Structures")
    print("-" * 60)
    
    # Create deeply nested structure
    nested = {
        "level1": {
            "level2": {
                "level3": {
                    "level4": {
                        "level5": {
                            "data": "Deep value",
                            "array": [1, [2, [3, [4, [5]]]]]
                        }
                    }
                }
            }
        }
    }
    
    print("Original nested structure:")
    print(json.dumps(nested, indent=2))
    print()
    
    toon = toonstream.encode(nested, indent=2)
    print("TOON format:")
    print(toon)
    print()
    
    decoded = toonstream.decode(toon)
    print(f"✓ Lossless conversion: {nested == decoded}")
    print()


def example_whitespace_handling():
    """Demonstrate whitespace handling in decoder."""
    print("6. Whitespace Handling")
    print("-" * 60)
    
    # Various whitespace formats
    test_cases = [
        ('{"key":"value"}', "No whitespace"),
        ('{ "key" : "value" }', "Spaces around braces"),
        ('{\n  "key": "value"\n}', "Newlines and indentation"),
        ('{\t"key"\t:\t"value"\t}', "Tabs"),
        ('[1,2,3]', "Compact array"),
        ('[ 1 , 2 , 3 ]', "Spaced array"),
    ]
    
    print("Testing whitespace variations:")
    for toon_str, description in test_cases:
        try:
            result = toonstream.decode(toon_str)
            print(f"  ✓ {description}")
        except Exception as e:
            print(f"  ✗ {description}: {e}")
    print()


def main():
    print("=" * 60)
    print("TOONSTREAM - Advanced Example")
    print("=" * 60)
    print()
    
    example_error_handling()
    example_edge_cases()
    example_json_compatibility()
    example_formatting_options()
    example_nested_structures()
    example_whitespace_handling()
    
    print("=" * 60)
    print("All advanced examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
