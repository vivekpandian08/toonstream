# Toonstream Core Library

Core implementation of the TOON format encoder and decoder.

## Files

- `__init__.py` - Package initialization and public API
- `encoder.py` - TOON format encoder with smart optimization
- `decoder.py` - TOON format decoder
- `exceptions.py` - Custom exception classes

## Architecture

### Encoder (`encoder.py`)

The encoder converts Python objects to TOON format:

**Key Features:**
- Recursive encoding of nested structures
- Smart optimization for arrays of objects
- Tabular format for homogeneous arrays (MIN_ARRAY_SIZE_FOR_TABULAR=3)
- Handles all Python data types

**Smart Optimization:**
- Detects arrays of similar objects
- Converts to tabular format (header + data rows)
- Reduces redundancy by 30-50%
- Configurable via `smart_optimize` parameter

### Decoder (`decoder.py`)

The decoder parses TOON format back to Python objects:

**Key Features:**
- Line-by-line parsing
- Indentation-aware structure parsing
- Tabular array reconstruction
- Type preservation (str, int, float, bool, None)

**Parsing Rules:**
- Lines with `:` are key-value pairs
- Lines with `-` are list items
- Quoted values are strings
- Numeric values are int/float
- `true`/`false` are booleans
- `null` is None

### Exceptions (`exceptions.py`)

Custom exception hierarchy:
- `ToonStreamError` - Base exception
- `EncodingError` - Encoding failures
- `DecodingError` - Decoding failures

## Public API

```python
import toonstream

# Encode
toon_str = toonstream.encode(data, smart_optimize=True)

# Decode
data = toonstream.decode(toon_str)
```

## Configuration

### Encoder Parameters

```python
MIN_ARRAY_SIZE_FOR_TABULAR = 3
MAX_FIELD_HETEROGENEITY = 0.3
```

- `MIN_ARRAY_SIZE_FOR_TABULAR`: Minimum array length for tabular optimization
- `MAX_FIELD_HETEROGENEITY`: Maximum field variance (0.3 = 30% different fields allowed)

### Encoder Options

```python
encode(data, smart_optimize=True)
```

- `smart_optimize=True`: Enable automatic tabular optimization
- `smart_optimize=False`: Use standard TOON format

## Data Type Support

| Python Type | TOON Representation | Example |
|-------------|-------------------|---------|
| str | Quoted | `"text"` |
| int | Numeric | `42` |
| float | Numeric | `3.14` |
| bool | Keyword | `true`, `false` |
| None | Keyword | `null` |
| list | Dash items | `- item` |
| dict | Key-value | `key: value` |

## Performance

**Encoding Speed:**
- Simple objects: <1ms
- Large arrays (1000 items): 10-50ms
- Deep nesting (10 levels): 5-20ms

**Decoding Speed:**
- Small TOON: <1ms
- Large TOON (10KB): 10-30ms
- Complex structures: 20-50ms

## Development

### Adding Features

1. Add implementation to `encoder.py` or `decoder.py`
2. Export in `__init__.py` if public API
3. Add tests to `tests/`
4. Update documentation
5. Run test suite

### Code Style

- PEP 8 compliant
- Type hints for all functions
- Comprehensive docstrings
- Comments for complex logic

### Extending

To add custom encoding for new types:
1. Add type check in `_encode_value()`
2. Add serialization logic
3. Add corresponding decoder logic
4. Add tests for round-trip
