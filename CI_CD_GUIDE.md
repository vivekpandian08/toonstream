# ToonStream CI/CD Pipeline Guide

## Overview

The ToonStream project uses GitHub Actions for Continuous Integration/Continuous Deployment (CI/CD). The pipeline automatically:

1. ✅ Runs all tests
2. ✅ Builds distributions (wheel + tarball)
3. ✅ Validates package integrity
4. ✅ Publishes to PyPI
5. ✅ Creates GitHub release
6. ✅ Uploads release assets

## How It Works

The CI/CD pipeline is triggered automatically when you **push a git tag** in the format `v*` (e.g., `v1.0.1`, `v2.0.0`).

### Workflow File

Location: `.github/workflows/publish.yml`

```yaml
on:
  push:
    tags:
      - 'v*'  # Triggers on tags like v1.0.1, v2.0.0, etc.
```

## Step-by-Step Usage

### 1. Make Code Changes

```powershell
# Edit your files, commit changes
git add .
git commit -m "Add new feature or fix"
git push origin main
```

### 2. Update Version Numbers

Update the version in these files:

**pyproject.toml:**
```toml
version = "1.0.2"
```

**setup.py:**
```python
version="1.0.2",
```

**toonstream/__init__.py:**
```python
__version__ = "1.0.2"
```

**README.md:**
```markdown
[![Version](https://img.shields.io/badge/version-1.0.2-brightgreen.svg)]
```

Commit these changes:

```powershell
git add pyproject.toml setup.py toonstream/__init__.py README.md
git commit -m "Bump version to 1.0.2"
git push origin main
```

### 3. Create and Push a Git Tag

Create a tag and push it to GitHub:

```powershell
# Create annotated tag
git tag -a v1.0.2 -m "Release version 1.0.2"

# Push the tag to GitHub
git push origin v1.0.2
```

Or push all tags:

```powershell
git push origin --tags
```

### 4. Monitor CI/CD Pipeline

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. Watch the workflow run in real-time

The pipeline will:
- ✅ Checkout code
- ✅ Set up Python 3.11
- ✅ Install dependencies
- ✅ Run pytest tests
- ✅ Build distributions
- ✅ Validate with twine
- ✅ Upload to PyPI
- ✅ Create GitHub Release
- ✅ Attach wheel and tarball to release

### 5. Verify PyPI Upload

After the workflow completes successfully:

```powershell
# Install the new version
pip install toonstream==1.0.2 --upgrade

# Or install directly from PyPI
pip install --index-url https://pypi.org/project/toonstream/ toonstream
```

## Prerequisites

### 1. PyPI API Token

Your CI/CD pipeline needs a PyPI API token to authenticate and upload packages.

**Generate Token:**
1. Go to https://pypi.org/account/settings/
2. Click "Add API token"
3. Name it "GitHub Actions" (or similar)
4. Copy the token (looks like: `pypi-AgEIcHl...`)

**Add to GitHub Secrets:**
1. Go to your GitHub repository settings
2. Navigate to Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI token
6. Click "Add secret"

The workflow automatically uses this token via:
```yaml
env:
  TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

### 2. GitHub Token

The `GITHUB_TOKEN` is automatically available in GitHub Actions workflows for creating releases. No additional setup needed.

## Complete Workflow Example

```powershell
# 1. Make changes and commit
git add .
git commit -m "Feature: Add new encoder optimization"
git push origin main

# 2. Update versions
# Edit: pyproject.toml, setup.py, toonstream/__init__.py, README.md
git add pyproject.toml setup.py toonstream/__init__.py README.md
git commit -m "Bump version to 1.0.2"
git push origin main

# 3. Create release tag
git tag -a v1.0.2 -m "Release v1.0.2 with encoder improvements"

# 4. Push tag to trigger CI/CD
git push origin v1.0.2

# 5. Wait for GitHub Actions to complete (~2-3 minutes)
# 6. Verify on PyPI: https://pypi.org/project/toonstream/1.0.2/
```

## Troubleshooting

### Pipeline Failed?

1. **Check the Actions tab** on GitHub to see error details
2. **Common issues:**
   - Tests failing: Fix code and re-push
   - Missing PyPI token: Add `PYPI_API_TOKEN` to secrets
   - Version mismatch: Ensure version tags match in all files

### Check Workflow Status

```powershell
# View recent commits and tags
git log --oneline -10

# View all tags
git tag -l

# View tag details
git show v1.0.2
```

## Best Practices

1. **Always run tests locally first:**
   ```powershell
   pytest tests/ -v
   ```

2. **Build locally before tagging:**
   ```powershell
   python -m build
   python -m twine check dist/*
   ```

3. **Use semantic versioning:**
   - MAJOR.MINOR.PATCH (e.g., 1.0.2)
   - MAJOR: Breaking changes
   - MINOR: New features
   - PATCH: Bug fixes

4. **Write meaningful commit messages:**
   ```
   Bump version to 1.0.2
   
   - Add new feature X
   - Fix bug Y
   - Improve performance Z
   ```

5. **Verify tag before pushing:**
   ```powershell
   # List all tags
   git tag -l
   
   # Show specific tag
   git show v1.0.2
   ```

## Quick Reference Commands

```powershell
# Create lightweight tag
git tag v1.0.2

# Create annotated tag (recommended)
git tag -a v1.0.2 -m "Release v1.0.2"

# Push specific tag
git push origin v1.0.2

# Push all tags
git push origin --tags

# Delete local tag
git tag -d v1.0.2

# Delete remote tag
git push origin --delete v1.0.2

# View tag information
git show v1.0.2

# List all tags
git tag -l

# List tags with descriptions
git tag -l -n
```

## Monitoring & Notifications

GitHub automatically sends:
- ✉️ Notifications when workflow succeeds/fails
- ✉️ Comments on commits with status
- ✉️ Release notifications to watchers

Set notification preferences in GitHub Settings → Notifications.

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI API Token Guide](https://pypi.org/help/#apitoken)
- [Semantic Versioning](https://semver.org/)
- [PEP 440 - Version Identification](https://www.python.org/dev/peps/pep-0440/)
