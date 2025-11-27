# PyPI API Token Security: Manual Approval Setup

## Overview

The GitHub Actions workflow now includes a **manual approval gate** that requires you to approve each PyPI deployment. This provides:

✅ **Security**: You manually approve before code goes to PyPI  
✅ **Control**: Review tests pass before deploying  
✅ **Safety**: Prevent accidental deployments  

## How It Works

### When You Push a Tag

```powershell
git tag -a v1.0.2 -m "Release v1.0.2"
git push origin v1.0.2
```

### Workflow Execution Flow

1. **Build Phase** (Automatic)
   - Tests run automatically
   - Distributions built
   - Package validated
   - Artifacts uploaded

2. **Approval Required** ⏸️
   - Workflow pauses at `publish` job
   - Waits for your approval
   - Requires environment review

3. **Publish Phase** (Manual Approval)
   - You approve in GitHub UI
   - PyPI upload proceeds
   - Release created on GitHub

## Setup: GitHub Environment Protection

### Step 1: Create Production Environment

1. Go to your GitHub repository
2. Click **Settings** → **Environments**
3. Click **New environment**
4. Name it: `production`
5. Click **Configure environment**

### Step 2: Set Reviewers (Optional)

1. In the `production` environment settings
2. Check **Required reviewers**
3. Add yourself or team members
4. Save

### Step 3: Add Secret (Already Done)

Your `PYPI_API_TOKEN` secret is already configured and accessible to the production environment.

## Approving a Deployment

### In GitHub UI

1. Go to your repository
2. Click **Actions** tab
3. Find the workflow run (by tag name, e.g., `v1.0.2`)
4. Click on the workflow run
5. Scroll down to see the "Waiting for review" message
6. Click **Review deployments**
7. Check the `production` box
8. Select **Approve and deploy**

### Alternative: Via Email

GitHub sends email notifications when workflows await approval. You can approve directly from the email link (if configured).

## Complete Workflow Example

```powershell
# 1. Make code changes
git add .
git commit -m "Add feature X"
git push origin main

# 2. Update version everywhere
# Edit: pyproject.toml, setup.py, toonstream/__init__.py, README.md
git add pyproject.toml setup.py toonstream/__init__.py README.md
git commit -m "Bump to v1.0.2"
git push origin main

# 3. Create and push tag (starts CI/CD)
git tag -a v1.0.2 -m "Release v1.0.2: Add feature X"
git push origin v1.0.2

# 4. Monitor GitHub Actions
# - Tests run automatically
# - Workflow pauses at "Waiting for review"
# - You receive notification

# 5. Approve deployment (manual)
# - Go to: https://github.com/vivekpandian08/toonstream/actions
# - Find the v1.0.2 workflow
# - Click "Review deployments"
# - Select "production" and "Approve and deploy"

# 6. Verify on PyPI
# - Package published automatically after approval
# - Check: https://pypi.org/project/toonstream/1.0.2/
```

## What Happens at Each Stage

### Build Stage (Automatic) ✅
```
✓ Checkout code
✓ Set up Python 3.11
✓ Install dependencies
✓ Run pytest (51 tests)
✓ Build wheel + tarball
✓ Validate with twine
✓ Upload artifacts to workflow
```

### Approval Gate ⏸️
```
⏸ Workflow pauses here
⏸ Requires manual approval
⏸ Email notification sent to you
```

### Publish Stage (After Approval) ✅
```
✓ Download artifacts
✓ Upload to PyPI (requires PYPI_API_TOKEN)
✓ Create GitHub Release
✓ Attach wheel + tarball to release
✓ Workflow complete
```

## View Deployment History

```powershell
# See all deployments
https://github.com/vivekpandian08/toonstream/deployments

# See specific workflow run
https://github.com/vivekpandian08/toonstream/actions/runs/<run-id>
```

## Security Benefits

### Before (Manual Upload)
- Manual twine upload locally
- API token in shell history
- Accidental uploads possible
- No audit trail

### Now (With Approval Gate)
- ✅ Automatic testing
- ✅ Manual approval required
- ✅ Full audit trail in GitHub
- ✅ API token never stored locally
- ✅ Safer deployment process

## Troubleshooting

### Workflow Stuck at Approval?

1. Check if you have reviewer permissions
2. Go to Actions tab → find the workflow
3. Click **Review deployments**
4. Make sure `production` environment is selected
5. Click **Approve and deploy**

### Approval Option Not Appearing?

1. Check environment exists: Settings → Environments → production
2. Verify the workflow uses: `environment: { name: production }`
3. Ensure PYPI_API_TOKEN secret exists
4. Try re-running the workflow

### Test Failures Prevent Approval?

1. If tests fail, workflow stops
2. Fix the issues locally
3. Push fixes to main branch
4. Create a new tag and push
5. Workflow will retry with fixed code

## Disabling Approval (Not Recommended)

If you want automatic deployment without approval:

```yaml
# Remove this from the publish job:
environment:
  name: production
```

⚠️ **Warning**: Not recommended - manual approval provides important safety checks.

## Next Steps

1. ✅ Verify the `production` environment exists in Settings
2. ✅ Keep your PYPI_API_TOKEN secure (only in GitHub Secrets)
3. ✅ Test with the v1.0.1 tag (already created)
4. ✅ For next releases, follow the workflow example above

## Quick Reference

```powershell
# Create release (triggers CI/CD + approval gate)
git tag -a v1.0.2 -m "Release v1.0.2"
git push origin v1.0.2

# Monitor workflow
https://github.com/vivekpandian08/toonstream/actions

# Approve deployment
https://github.com/vivekpandian08/toonstream/actions
→ Find v1.0.2 workflow → Review deployments → Approve

# Verify on PyPI
https://pypi.org/project/toonstream/
```

## Additional Resources

- [GitHub Environments Documentation](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [GitHub Deployment Protection Rules](https://docs.github.com/en/actions/deployment/protection-rules)
- [PyPI Security Best Practices](https://pypi.org/help/#apitoken)
