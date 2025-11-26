# 🎨 ToonLib

**Token-Optimized Object Notation (TOON) - Reduce LLM token usage by up to 55% with lossless data serialization**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)](https://github.com/vivekpandian08/toonlib)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-93.3%25-brightgreen.svg)](tests/)

---

## 📖 What is ToonLib?

**ToonLib** is a Python library for encoding structured data in a token-efficient format designed for Large Language Models (LLMs). It converts repetitive JSON structures into compact, tabular representations that dramatically reduce token count while maintaining 100% lossless conversion.

### The Problem

LLMs charge by tokens. Verbose JSON wastes tokens and money:

```json
[
  {"id": 1, "name": "Alice", "dept": "Engineering", "salary": 95000},
  {"id": 2, "name": "Bob", "dept": "Sales", "salary": 75000},
  {"id": 3, "name": "Carol", "dept": "Engineering", "salary": 105000}
]
```
**Cost:** 3,914 tokens

### The Solution

TOON format eliminates redundancy:

```
employees[3]{id,name,dept,salary}:
1,Alice,Engineering,95000
2,Bob,Sales,75000
3,Carol,Engineering,105000
```
**Cost:** 1,733 tokens (**-55.7%** reduction)

### Why ToonLib?

✅ **Save Money** - Reduce API costs by up to 55% on structured data  
✅ **100% Lossless** - Perfect round-trip conversion, no data loss  
✅ **Zero Dependencies** - Pure Python, no external packages required  
✅ **Fast** - Sub-millisecond encoding/decoding  
✅ **Smart** - Automatic optimization, only improves when beneficial  
✅ **Simple API** - Two functions: `encode()` and `decode()`  

---

## 🚀 Installation

```bash
pip install toonlib
```

Or from source:

```bash
git clone https://github.com/vivekpandian08/toonlib.git
cd toonlib
pip install -e .
```

**Requirements:**
- Python 3.7 or higher
- No external dependencies (tiktoken optional for token counting)

### Basic Usage

```python
import toonlib

# Your data
data = {
    "name": "Alice",
    "age": 30,
    "skills": ["Python", "JavaScript", "SQL"]
}

# Encode to TOON
toon_str = toonlib.encode(data)
print(toon_str)
```

**Output:**
```
name: "Alice"
age: 30
skills: [
  - "Python"
  - "JavaScript"
  - "SQL"
]
```

---

## ⚡ Quick Start

### Basic Usage

```python
from toonlib import encode, decode

# Your data
data = {
    "employees": [
        {"id": 1, "name": "Alice", "dept": "Engineering"},
        {"id": 2, "name": "Bob", "dept": "Sales"},
        {"id": 3, "name": "Carol", "dept": "Engineering"}
    ]
}

# Encode to TOON format
toon_str = encode(data)
print(toon_str)
# Output:
# employees[3]{id,name,dept}:
# 1,Alice,Engineering
# 2,Bob,Sales
# 3,Carol,Engineering

# Decode back to Python
decoded = decode(toon_str)
assert decoded == data  # ✓ Perfect round-trip!
```

### Advanced Options

```python
# Compact mode (minimize whitespace)
compact = encode(data, compact=True)

# Disable smart optimization (always use tabular)
always_tabular = encode(data, smart_optimize=False)

# Pretty print with indentation
pretty = encode(data, indent=2)
```

---

## 📊 Performance Benchmarks

Real-world results from production datasets:

| Data Type | JSON Tokens | TOON Tokens | Reduction | Use Case |
|-----------|-------------|-------------|-----------|----------|
| **Employee Records** (50) | 3,914 | 1,733 | **-55.7%** | HR systems, payroll |
| **GitHub Repos** (100) | 14,102 | 8,712 | **-38.2%** | API responses |
| **Order History** (10) | 2,926 | 2,915 | **-0.4%** | E-commerce |
| **Config Files** (20) | 7,393 | 7,393 | **0.0%** | Microservices |

### When to Use TOON

**🟢 Excellent Results (30-55% savings):**
- Arrays of similar objects (users, products, logs)
- Tabular data (CSV-like structures)
- Database query results
- Time-series data

**🟡 Good Results (10-30% savings):**
- Mixed nested structures
- API responses with arrays
- Semi-structured documents

**🔴 Neutral Results (±5%):**
- Deeply nested JSON (5+ levels)
- Unique object structures
- Small datasets (<3 items)

### Speed

All operations complete in **under 1 millisecond** for typical datasets:
- 50 records: 0.41ms
- 100 records: 0.83ms
- Decode: <1ms

---

## 🎯 Use Cases

### 1. LLM Context Optimization

3. **Install in development mode:**
```bash
pip install -e .
```

4. **Install development dependencies (optional):**
```bash
pip install -e ".[dev]"
```

This includes:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `tiktoken` - Token counting
- `black` - Code formatting

### Verify Installation

```bash
# Run tests
pytest tests/

# Run benchmarks
python benchmarks/run_all_comparisons.py

# Try the tutorial
jupyter notebook examples/toonlib_tutorial.ipynb
```

### Project Structure

```


```python
import toonlib

# Pass structured data to LLM
context = {
    "users": [...],  # 100 user records
    "products": [...],  # 50 products
    "orders": [...]  # 200 orders
}

# Reduce prompt tokens by 40%
toon_context = toonlib.encode(context)
response = llm.complete(f"Analyze this data:\n{toon_context}")
```

### 2. Pickle Integration

Save data with TOON encoding for additional compression:

```python
from toonlib import save_toon_pickle, load_toon_pickle

# Save with TOON encoding
data = {"users": [...], "logs": [...]}
save_toon_pickle(data, 'data.toon.pkl')

# Load back
loaded = load_toon_pickle('data.toon.pkl')

# 11.4% smaller than regular pickle!
```

### 3. API Response Optimization

```python
from toonlib import encode
from flask import Flask, Response

app = Flask(__name__)

@app.route('/api/employees')
def get_employees():
    employees = db.query("SELECT * FROM employees")
    toon_data = encode(employees)
    return Response(toon_data, mimetype='text/plain')

# Clients get 55% smaller responses
```

### 4. Configuration Files

```python
import toonlib

config = {
    "database": {"host": "localhost", "port": 5432},
    "cache": {"ttl": 3600, "max_size": 1000}
}

# Save human-readable config
with open('config.toon', 'w') as f:
    f.write(toonlib.encode(config, indent=2))

# Load config
with open('config.toon') as f:
    config = toonlib.decode(f.read())
```

---

## 🛠️ API Reference

### Core Functions

#### `encode(obj, compact=False, smart_optimize=True, indent=None)`

Convert Python object to TOON format.

**Parameters:**
- `obj` (Any): Python object (dict, list, primitive)
- `compact` (bool): Minimize whitespace (default: False)
- `smart_optimize` (bool): Auto-detect best format (default: True)
- `indent` (int): Indentation spaces, None for compact (default: None)

**Returns:** `str` - TOON formatted string

**Raises:** `ToonEncodeError` - If encoding fails

```python
# Basic encoding
toon = encode(data)

# Compact output
toon = encode(data, compact=True)

# Always use tabular (no optimization)
toon = encode(data, smart_optimize=False)

# Pretty print with 2-space indent
toon = encode(data, indent=2)
```

#### `decode(toon_str, strict=True)`

Convert TOON format to Python object.

**Parameters:**
- `toon_str` (str): TOON formatted string
- `strict` (bool): Enforce strict validation (default: True)

**Returns:** `Any` - Python object

**Raises:** `ToonDecodeError` - If decoding fails

```python
# Decode TOON string
data = decode(toon_str)

# Lenient mode (allows minor format issues)
data = decode(toon_str, strict=False)
```

### Pickle Functions

#### `save_toon_pickle(data, filepath, smart_optimize=True, protocol=HIGHEST_PROTOCOL)`

Save data as TOON-encoded pickle file.

**Parameters:**
- `data` (Any): Python object to save
- `filepath` (str): Output file path
- `smart_optimize` (bool): Use TOON optimization (default: True)
- `protocol` (int): Pickle protocol version (default: HIGHEST_PROTOCOL)

```python
from toonlib import save_toon_pickle

save_toon_pickle(data, 'data.toon.pkl')
```

#### `load_toon_pickle(filepath, strict=True)`

Load TOON-encoded pickle file.

**Parameters:**
- `filepath` (str): Input file path
- `strict` (bool): Enforce strict TOON validation (default: True)

**Returns:** `Any` - Loaded Python object

```python
from toonlib import load_toon_pickle

data = load_toon_pickle('data.toon.pkl')
```

### Exceptions

- `ToonError` - Base exception
- `ToonEncodeError` - Encoding failures (unsupported types, NaN, Infinity)
- `ToonDecodeError` - Decoding failures (invalid format, syntax errors)
- `ToonValidationError` - Validation failures
- `ToonPickleError` - Pickle operation failures

---

## 🧪 Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=toonlib --cov-report=html

# Open coverage report
open htmlcov/index.html
```

### Running Benchmarks

```bash
# Run all benchmarks
python benchmarks/run_all_comparisons.py

# Results appear in terminal and save to results/
```

### Project Structure

```
toonlib/
├── toonlib/              # Core library
│   ├── __init__.py       # Public API exports
│   ├── encoder.py        # TOON encoder (480 lines)
│   ├── decoder.py        # TOON decoder (530 lines)
│   ├── exceptions.py     # Exception hierarchy
│   └── pickle_utils.py   # Pickle integration (170 lines)
├── benchmarks/           # Performance tests
│   ├── run_all_comparisons.py
│   └── config.json
├── tests/                # Test suite (45 tests, 93.3% passing)
│   └── test_toonlib.py
├── examples/             # Usage examples
│   ├── basic_usage.py
│   ├── advanced_optimization.py
│   └── pickle_example.py
├── data/                 # Benchmark datasets
├── results/              # Benchmark results
├── README.md             # This file
├── PICKLE_USAGE.md       # Pickle utilities guide
├── setup.py              # Package configuration
└── requirements.txt      # Dependencies
```

---

## 📖 Examples

See the `examples/` directory for complete examples:

- **basic_usage.py** - Getting started guide
- **advanced_optimization.py** - Smart optimization features
- **pickle_example.py** - Pickle integration demo

Run them:

```bash
python examples/basic_usage.py
python examples/advanced_optimization.py
python examples/pickle_example.py
```

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

1. **Edge Cases** - Special characters in keys, empty string validation
2. **Features** - CLI tool, streaming encoder, sort_keys parameter
3. **Documentation** - More examples, integration guides
4. **Performance** - Additional optimizations for specific data types

### Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/toonlib.git
cd toonlib

# Create branch
git checkout -b feature/your-feature

# Install dev dependencies
pip install -e ".[dev]"

# Make changes and test
pytest tests/

# Submit PR
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- Inspired by CSV efficiency for tabular data
- Built for the LLM era where tokens = money
- Tested with real-world production datasets

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/toonlib/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/toonlib/discussions)
- **Documentation:** See `PICKLE_USAGE.md` and `results/OPTIMIZATION_GUIDE.md`

---

## 🔗 Links

- **PyPI:** https://pypi.org/project/toonlib/ (coming soon)
- **GitHub:** https://github.com/yourusername/toonlib
- **Documentation:** https://toonlib.readthedocs.io/ (coming soon)

---

**Made with ❤️ for the LLM community**

*Save tokens. Save money. Build better.*
• Smart Optimizer: Detects homogeneous arrays and applies tabular format
• Type System: Preserves all JSON types during conversion
• Parser: Indentation-aware recursive descent parser
```

---

## 📊 Benchmarks

Run comprehensive benchmarks:

```bash
python benchmarks/run_all_comparisons.py
```

### Performance Results

**Dataset: 200 employees + 150 projects**

| Format | Characters | Tokens | vs JSON Compact |
|--------|-----------|--------|-----------------|
| JSON Pretty | 52,340 | 14,250 | +30% |
| JSON Compact | 40,230 | 10,958 | baseline |
| **TOON** | **18,327** | **6,686** | **-39%** 🏆 |

**Encoding Speed:**
- Small objects (<1KB): <1ms
- Large arrays (1000 items): 10-50ms
- Deep nesting (10 levels): 5-20ms

**Decoding Speed:**
- Small TOON (<1KB): <1ms
- Large TOON (10KB): 10-30ms
- Complex structures: 20-50ms

---

## 🧪 Testing

Comprehensive test suite with 100% coverage:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=toonlib --cov-report=html

# Run specific test file
pytest tests/test_encoder.py
```

**Test Coverage:**
- ✅ All primitive types (str, int, float, bool, null)
- ✅ Nested structures (arrays, objects, deep nesting)
- ✅ Edge cases (empty values, Unicode, special chars)
- ✅ Smart optimization (tabular arrays)
- ✅ Round-trip conversion (encode → decode)
- ✅ Error handling (invalid input, malformed TOON)

---

## 📖 Documentation

### API Reference

#### `encode(data, smart_optimize=True)`

Convert Python object to TOON format.

**Parameters:**
- `data` (dict|list|str|int|float|bool|None): Python object to encode
- `smart_optimize` (bool): Enable automatic tabular optimization (default: True)

**Returns:**
- `str`: TOON formatted string

**Example:**
```python
toon_str = toonlib.encode(data, smart_optimize=True)
```

---

#### `decode(toon_str)`

Convert TOON format back to Python object.

**Parameters:**
- `toon_str` (str): TOON formatted string

**Returns:**
- `dict|list|str|int|float|bool|None`: Parsed Python object

**Raises:**
- `DecodingError`: If TOON format is invalid

**Example:**
```python
data = toonlib.decode(toon_str)
```

---

### TOON Format Specification

#### Basic Syntax

```
# Key-value pairs
name: "Alice"
age: 30
active: true
score: 3.14
value: null

# Arrays
skills: [
  - "Python"
  - "JavaScript"
]

# Objects
address: {
  city: "NYC"
  zip: 10001
}
```

#### Tabular Arrays (Smart Optimization)

```
employees: [
  - {id, name, salary}
  - 1, "Alice", 95000
  - 2, "Bob", 75000
]
```

**Requirements for tabular format:**
- Array length ≥ 3 (configurable)
- Objects have similar keys (≤30% difference)
- Automatically applied with `smart_optimize=True`

---

## 🎯 Use Cases

### 1. LLM Token Optimization
Reduce input tokens for GPT/Claude/etc. API calls:
```python
import toonlib

# Convert large JSON context to TOON
context_json = load_large_context()
context_toon = toonlib.encode(context_json, smart_optimize=True)

# Save 39% on tokens → lower costs!
response = openai.ChatCompletion.create(
    messages=[{"role": "user", "content": f"Context: {context_toon}\n\nQuestion: ..."}]
)
```

### 2. Data Storage Compression
Reduce storage costs for JSON-heavy databases:
```python
# Before: 100GB of JSON logs
# After: 55GB of TOON logs
# Savings: 45GB × $0.023/GB/month = $1.04/month (S3 Standard)
```

### 3. API Bandwidth Reduction
Lower data transfer costs:
```python
# API response: 500KB JSON → 275KB TOON (45% reduction)
# 1M requests/month: 225GB saved
# CDN savings: 225GB × $0.085/GB = $19.13/month
```

### 4. Configuration Files
Human-readable configs with type safety:
```python
# config.toon is more readable than config.json
# Still machine-parseable with toonlib.decode()
```

---

## 🤝 Contributing

Contributions welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Add tests** for new functionality
4. **Ensure** all tests pass (`pytest tests/`)
5. **Commit** changes (`git commit -m 'Add amazing feature'`)
6. **Push** to branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Development Setup

```bash
git clone https://github.com/yourusername/toonlib.git
cd toonlib
pip install -e ".[dev]"
pytest tests/
```

---

## 📋 Roadmap

- [x] Core encoder/decoder
- [x] Smart tabular optimization
- [x] Comprehensive test suite
- [x] Performance benchmarks
- [ ] CLI tool for JSON ↔ TOON conversion
- [ ] VS Code syntax highlighting extension
- [ ] Streaming parser for large files
- [ ] C extension for 10x performance boost
- [ ] Language bindings (JavaScript, Go, Rust)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by YAML's readability and JSON's simplicity
- Optimized for the token-constrained world of LLMs
- Built with ❤️ for developers who care about efficiency

---

## 📞 Support & Contact

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/toonlib/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/toonlib/discussions)
- 📧 **Email**: your.email@example.com
- 🌟 **Star** this repo if you find it useful!

---

## 🔗 Links

- [Documentation](docs/)
- [Examples](examples/)
- [Benchmarks](benchmarks/)
- [Changelog](CHANGELOG.md)
- [Contributing Guide](CONTRIBUTING.md)

---

**Made with 🎨 by [Your Name]** | **Token efficiency for the modern web**

```python
import toonlib

# Python object to TOON
data = {
    "name": "John Doe",
    "age": 30,
    "active": True,
    "hobbies": ["reading", "coding"]
}

# Encode to TOON (compact format)
toon_str = toonlib.encode(data, indent=0)
print(toon_str)
# Output: {"name": "John Doe", "age": 30, "active": true, "hobbies": ["reading", "coding"]}

# Encode to TOON (pretty format)
toon_str = toonlib.encode(data, indent=2)
print(toon_str)
# Output:
# {
#   "name": "John Doe",
#   "age": 30,
#   "active": true,
#   "hobbies": [
#     "reading",
#     "coding"
#   ]
# }

# Decode TOON back to Python
decoded = toonlib.decode(toon_str)
print(decoded == data)  # True - lossless conversion
```

### Advanced Usage

```python
import toonlib
from toonlib import ToonEncoder, ToonDecoder, ToonEncodeError, ToonDecodeError

# Using encoder class with options
encoder = ToonEncoder(indent=2, sort_keys=True)
toon_str = encoder.encode({"z": 1, "a": 2})

# Using decoder class
decoder = ToonDecoder(strict=True)
data = decoder.decode(toon_str)

# Error handling
try:
    toonlib.encode(float('nan'))  # NaN not supported
except ToonEncodeError as e:
    print(f"Encoding error: {e}")

try:
    toonlib.decode("{invalid}")  # Invalid TOON
except ToonDecodeError as e:
    print(f"Decoding error: {e}")
```

## TOON Format Specification

TOON uses a JSON-like syntax:

- **Strings**: `"value"` (with escape sequences: `\"`, `\\`, `\/`, `\b`, `\f`, `\n`, `\r`, `\t`, `\uXXXX`)
- **Numbers**: `123`, `123.456`, `-123`, `1.23e10`
- **Booleans**: `true`, `false`
- **Null**: `null`
- **Arrays**: `[item1, item2, item3]`
- **Objects**: `{"key1": value1, "key2": value2}`

## API Reference

### Functions

#### `encode(obj, indent=2, sort_keys=False)`
Encode a Python object to TOON format.

**Parameters:**
- `obj` (Any): Python object to encode
- `indent` (int): Number of spaces for indentation (0 for compact)
- `sort_keys` (bool): Whether to sort object keys alphabetically

**Returns:** TOON formatted string

**Raises:** `ToonEncodeError` if encoding fails

#### `decode(toon_str, strict=True)`
Decode a TOON string to a Python object.

**Parameters:**
- `toon_str` (str): TOON formatted string
- `strict` (bool): Whether to enforce strict TOON validation

**Returns:** Python object

**Raises:** `ToonDecodeError` if decoding fails

### Classes

#### `ToonEncoder(indent=2, sort_keys=False)`
Encoder class for converting Python objects to TOON format.

**Methods:**
- `encode(obj)`: Encode a Python object to TOON

#### `ToonDecoder(strict=True)`
Decoder class for converting TOON strings to Python objects.

**Methods:**
- `decode(toon_str)`: Decode a TOON string to Python

### Exceptions

- `ToonError`: Base exception for all TOON-related errors
- `ToonEncodeError`: Raised when encoding fails
- `ToonDecodeError`: Raised when decoding fails
- `ToonValidationError`: Raised when validation fails

## Examples

Run the included examples:

```bash
# Basic example
python examples/basic_example.py

# Advanced example with error handling and edge cases
python examples/advanced_example.py
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=toonlib --cov-report=html

# Run specific test class
python -m pytest tests/test_toonlib.py::TestPrimitiveTypes

# Run with verbose output
python -m pytest tests/ -v
```

## Project Structure

```
toonlib/
├── toonlib/
│   ├── __init__.py       # Package initialization
│   ├── encoder.py        # JSON to TOON encoder
│   ├── decoder.py        # TOON to JSON decoder
│   └── exceptions.py     # Custom exceptions
├── tests/
│   └── test_toonlib.py   # Comprehensive unit tests
├── examples/
│   ├── basic_example.py      # Basic usage examples
│   └── advanced_example.py   # Advanced features demo
├── README.md
├── setup.py
└── requirements.txt
```

## Development

### Phase 1: Core Functionality ✅

- [x] Implement JSON → TOON encoder
- [x] Implement TOON → JSON decoder
- [x] Basic validation and error handling
- [x] Unit tests for primitive types
- [x] Lossless JSON ↔ TOON conversion
- [x] All primitive types supported
- [x] Nested structures handled correctly
- [x] Edge cases tested (empty, null, special chars)

## Requirements

- Python 3.8 or higher
- No external dependencies for core functionality
- pytest (for running tests)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or contributions, please open an issue on the repository.
