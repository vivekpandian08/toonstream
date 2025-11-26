# Examples

Tutorials and example code for using toonlib.

## Files

- `toonlib_tutorial.ipynb` - Interactive Jupyter notebook with comprehensive examples

## Tutorial Contents

The notebook covers:

1. **Installation** - Setting up toonlib
2. **Basic Usage** - Simple encoding and decoding
3. **Smart Optimization** - Automatic tabular format for arrays
4. **Data Types** - All supported Python types
5. **Real-world Examples** - Practical use cases
6. **Performance** - Compression benchmarks
7. **Best Practices** - When to use TOON

## Running the Tutorial

### Jupyter Notebook
```bash
jupyter notebook examples/toonlib_tutorial.ipynb
```

### VS Code
1. Open `toonlib_tutorial.ipynb` in VS Code
2. Select Python kernel
3. Run cells interactively

## Quick Examples

### Basic Encoding
```python
import toonlib

data = {"name": "John", "age": 30}
toon_str = toonlib.encode(data)
```

### Smart Optimization
```python
employees = [
    {"id": 1, "name": "Alice", "salary": 50000},
    {"id": 2, "name": "Bob", "salary": 60000}
]
toon_str = toonlib.encode(employees, smart_optimize=True)
```

### Decoding
```python
data = toonlib.decode(toon_str)
```

## Use Cases

- **API responses** - Reduce payload size
- **Data storage** - Compress JSON files
- **Log files** - Structured logging with less space
- **Configuration** - Readable config files
- **Data exchange** - Efficient data transfer
