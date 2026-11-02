# Publishing to PyPI

## Overview

When `publish_to_pypi` is set to `true`, the `on-release-main.yml` workflow automatically publishes your package to [PyPI](https://pypi.org) whenever you create a new release.

## Set up PyPI Token

Before your first release, add your PyPI API token as a GitHub secret:

1. **Get your PyPI token:**
    - Go to [PyPI Account Settings](https://pypi.org/manage/account/)
    - Scroll to "API tokens" and click "Add API token"
    - Give it a name (e.g., "GitHub Actions")
    - Set scope to "Entire account" (or project-specific after first publish)
    - Copy the token (starts with `pypi-`)

2. **Add to GitHub:**
    - Go to your repository → `Settings` → `Secrets and variables` → `Actions`
    - Click "New repository secret"
    - Name: `PYPI_TOKEN`
    - Value: paste your token
    - Click "Add secret"

## Testing with TestPyPI (Recommended)

Before publishing to the real PyPI, test your setup with [TestPyPI](https://test.pypi.org/):

1. **Get a TestPyPI token:**
    - Create an account at [test.pypi.org](https://test.pypi.org/account/register/)
    - Go to [Account Settings](https://test.pypi.org/manage/account/) → "Add API token"
    - Copy the token

2. **Modify workflow for testing:**

    Edit `.github/workflows/on-release-main.yml`, add `UV_PUBLISH_URL`:

    ```yaml
    - name: Publish package
      run: uv publish
      env:
        UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
        UV_PUBLISH_URL: https://test.pypi.org/legacy/  # Remove after testing
    ```

3. **Add TestPyPI token as `PYPI_TOKEN` secret** (temporarily)

4. **Create a test release** and verify at `https://test.pypi.org/project/your-package/`

5. **Switch to real PyPI:**
    - Remove the `UV_PUBLISH_URL` line from the workflow
    - Update `PYPI_TOKEN` secret with your real PyPI token

## Publishing from your local machine

Not recommended, but possible:

```bash
make build-and-publish
```
