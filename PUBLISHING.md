# Publishing ToonLib to PyPI

Complete guide to make ToonLib installable via `pip install toonlib`

---

## Prerequisites

1. **PyPI Account**
   - Create account at https://pypi.org/account/register/
   - Verify your email
   - Enable 2FA (recommended)

2. **Test PyPI Account (Optional)**
   - Create account at https://test.pypi.org/account/register/
   - Use for testing before real upload

3. **Install Build Tools**
   ```bash
   pip install build twine
   ```

---

## Step 1: Update Package Metadata

Edit `setup.py` and update:

```python
setup(
    name="toonlib",
    version="1.0.0",  # Increment for new releases
    author="Your Name",  # ← Change this
    author_email="your.email@example.com",  # ← Change this
    url="https://github.com/yourusername/toonlib",  # ← Change this
    # ... rest of config
)
```

---

## Step 2: Build Distribution Files

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build distribution packages
python -m build
```

This creates:
- `dist/toonlib-1.0.0.tar.gz` (source distribution)
- `dist/toonlib-1.0.0-py3-none-any.whl` (wheel distribution)

---

## Step 3: Test Upload (Optional but Recommended)

Upload to Test PyPI first:

```bash
python -m twine upload --repository testpypi dist/*
```

Enter credentials when prompted.

Test installation:

```bash
pip install --index-url https://test.pypi.org/simple/ toonlib
```

Verify it works:

```python
from toonlib import encode, decode
data = {"test": [1, 2, 3]}
toon = encode(data)
print(decode(toon))
```

---

## Step 4: Upload to Real PyPI

```bash
python -m twine upload dist/*
```

Enter your PyPI credentials when prompted.

**Done!** Your package is now live at https://pypi.org/project/toonlib/

---

## Step 5: Users Can Install

Anyone can now install:

```bash
pip install toonlib
```

---

## Using API Tokens (Recommended)

Instead of username/password, use API tokens for security.

1. **Generate Token**
   - Go to https://pypi.org/manage/account/token/
   - Create new token with scope "Entire account"
   - Copy token (starts with `pypi-`)

2. **Configure `.pypirc`**

   Windows: `%USERPROFILE%\.pypirc`
   Linux/Mac: `~/.pypirc`

   ```ini
   [pypi]
   username = __token__
   password = pypi-your-token-here

   [testpypi]
   username = __token__
   password = pypi-your-test-token-here
   ```

3. **Upload with Token**
   ```bash
   python -m twine upload dist/*
   # No prompt - uses token from .pypirc
   ```

---

## Version Updates

For new releases:

1. **Update version in setup.py**
   ```python
   version="1.0.1",  # Increment
   ```

2. **Update version in toonlib/__init__.py**
   ```python
   __version__ = "1.0.1"
   ```

3. **Rebuild and upload**
   ```bash
   rm -rf dist/ build/ *.egg-info
   python -m build
   python -m twine upload dist/*
   ```

---

## Troubleshooting

**Error: "File already exists"**
- Can't re-upload same version
- Increment version number and rebuild

**Error: "Invalid credentials"**
- Check username/password
- Use API token instead
- Verify 2FA is enabled

**Error: "Package name already taken"**
- Choose different name
- Update `name=` in setup.py

**Import error after install**
- Check package structure
- Verify `__init__.py` exports are correct

---

## GitHub Actions (CI/CD)

Automate publishing with GitHub Actions:

`.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Add PyPI token to GitHub secrets as `PYPI_API_TOKEN`.

---

## Quick Reference

```bash
# Install tools
pip install build twine

# Build package
python -m build

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Users install
pip install toonlib
```

---

## Resources

- PyPI: https://pypi.org
- Test PyPI: https://test.pypi.org
- Packaging Guide: https://packaging.python.org/
- Twine Docs: https://twine.readthedocs.io/
