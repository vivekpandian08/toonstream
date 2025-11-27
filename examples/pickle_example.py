"""
Example demonstrating pickle utilities for TOON format.

This script shows how to save and load data using TOON pickle format,
and compares file sizes between TOON pickle and regular pickle.
"""

import os
import toonstream
from toonstream import save_toon_pickle, load_toon_pickle, save_pickle, load_pickle

# Sample data - typical use case with arrays of objects
sample_data = {
    "employees": [
        {"id": 1, "name": "Alice Johnson", "department": "Engineering", "salary": 95000, "active": True},
        {"id": 2, "name": "Bob Smith", "department": "Sales", "salary": 75000, "active": True},
        {"id": 3, "name": "Carol Williams", "department": "Engineering", "salary": 105000, "active": True},
        {"id": 4, "name": "David Brown", "department": "Marketing", "salary": 82000, "active": False},
        {"id": 5, "name": "Eve Davis", "department": "Sales", "salary": 87000, "active": True},
    ],
    "metadata": {
        "company": "TechCorp",
        "year": 2025,
        "total_employees": 5
    }
}

print("=" * 60)
print("TOON Pickle Utilities - Example")
print("=" * 60)

# 1. Save data using TOON pickle
print("\n1. Saving data with TOON pickle...")
save_toon_pickle(sample_data, "output/employees.toon.pkl")
print("   ✓ Saved to: output/employees.toon.pkl")

# 2. Save data using regular pickle (for comparison)
print("\n2. Saving data with regular pickle...")
save_pickle(sample_data, "output/employees.pkl")
print("   ✓ Saved to: output/employees.pkl")

# 3. Compare file sizes
toon_size = os.path.getsize("output/employees.toon.pkl")
regular_size = os.path.getsize("output/employees.pkl")
savings = (1 - toon_size / regular_size) * 100

print("\n3. File size comparison:")
print(f"   TOON pickle:    {toon_size:,} bytes")
print(f"   Regular pickle: {regular_size:,} bytes")
print(f"   Savings:        {savings:.1f}%")

# 4. Load data back from TOON pickle
print("\n4. Loading data from TOON pickle...")
loaded_data = load_toon_pickle("output/employees.toon.pkl")
print("   ✓ Data loaded successfully")

# 5. Verify data integrity
print("\n5. Verifying data integrity...")
if loaded_data == sample_data:
    print("   ✓ Data matches original (lossless conversion)")
else:
    print("   ✗ Data mismatch!")

# 6. Display loaded data sample
print("\n6. Sample of loaded data:")
print(f"   Company: {loaded_data['metadata']['company']}")
print(f"   Employees: {len(loaded_data['employees'])}")
print(f"   First employee: {loaded_data['employees'][0]['name']}")

# 7. Show TOON format preview
print("\n7. TOON format preview:")
toon_str = toonstream.encode(sample_data)
lines = toon_str.split('\n')
print("   " + "\n   ".join(lines[:5]))
if len(lines) > 5:
    print(f"   ... ({len(lines) - 5} more lines)")

print("\n" + "=" * 60)
print("✓ Example completed successfully!")
print("=" * 60)

# Cleanup
print("\nFiles created:")
print("  - output/employees.toon.pkl")
print("  - output/employees.pkl")
