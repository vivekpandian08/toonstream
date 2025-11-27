# Tests

Test suite for toonstream library.

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run specific test file
```bash
pytest tests/test_toonstream.py
pytest tests/test_encoder.py
pytest tests/test_decoder.py
pytest tests/test_exceptions.py
```

### Run with coverage
```bash
pytest tests/ --cov=toonstream --cov-report=html
```

## Test Files

- `test_toonstream.py` - Comprehensive unit tests for toonstream
- `test_encoder.py` - Tests for TOON encoding
- `test_decoder.py` - Tests for TOON decoding
- `test_exceptions.py` - Error handling tests
- `test_integration.py` - End-to-end integration tests

## Test Coverage

Tests cover:
- ✓ All Python data types (str, int, float, bool, None, list, dict)
- ✓ Nested structures
- ✓ Edge cases (empty values, special characters)
- ✓ Smart optimization (tabular arrays)
- ✓ Round-trip encoding/decoding
- ✓ Error handling and exceptions
- ✓ Unicode and special characters

## Adding Tests

When adding new features:
1. Add tests to appropriate test file
2. Test both encoding and decoding
3. Test edge cases
4. Ensure round-trip correctness
5. Run full test suite before committing

## Test Results

All tests should pass:
```
===== test session starts =====
collected 45 items

tests/test_toonstream.py ......... [ 26%]
tests/test_encoder.py ............ [ 52%]
tests/test_decoder.py ............ [ 70%]
tests/test_exceptions.py ........ [ 85%]
tests/test_integration.py ...... [100%]

===== 45 passed in 0.5s =====
```
