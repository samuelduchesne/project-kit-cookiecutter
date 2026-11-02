# {{cookiecutter.project_name}}

[![Release](https://img.shields.io/github/v/release/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/releases)
[![Build status](https://img.shields.io/github/actions/workflow/status/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/main.yml?branch=main)](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/actions/workflows/main.yml?query=branch%3Amain)
{%- if cookiecutter.codecov %}
[![codecov](https://codecov.io/gh/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})
{%- endif %}
[![License](https://img.shields.io/github/license/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/blob/main/LICENSE)

{{cookiecutter.project_description}}
{% if cookiecutter.mkdocs %}
**[Documentation](https://{{cookiecutter.author_github_handle}}.github.io/{{cookiecutter.project_name}}/)** | **[GitHub](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/)**
{%- else %}
**[GitHub](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/)**
{%- endif %}

## Installation

```bash
pip install {{cookiecutter.project_name}}
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add {{cookiecutter.project_name}}
```

## Usage

```python
import {{cookiecutter.project_slug}}

# TODO: Add usage examples
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

### Setup

```bash
# Clone the repository
git clone https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}.git
cd {{cookiecutter.project_name}}

# Install dependencies and pre-commit hooks
make install
```

> **Note:** Run `git init -b main` first if you're starting from a cookiecutter template.

### Commands

```bash
make install    # Install dependencies and pre-commit hooks
make check      # Run linting, formatting, and type checks
make test       # Run tests{% if cookiecutter.codecov %} with coverage{% endif %}
{%- if cookiecutter.mkdocs %}
make docs       # Serve documentation locally
make docs-test  # Test documentation build
{%- endif %}
{%- if cookiecutter.dockerfile %}
make docker-build  # Build Docker image
make docker-run    # Run Docker container
{%- endif %}
```

### First-time setup for new projects

If you just created this project from the cookiecutter template:

1. Create a GitHub repository with the same name
2. Push your code:

   ```bash
   git init -b main
   git add .
   git commit -m "Initial commit"
   git remote add origin git@github.com:{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}.git
   git push -u origin main
   ```

3. Install dependencies: `make install`
4. Fix formatting and commit:

   ```bash
   git add .
   uv run pre-commit run -a
   git add .
   git commit -m "Apply formatting"
   git push
   ```

For detailed setup instructions, see the [project-kit-cookiecutter tutorial](https://samuelduchesne.github.io/project-kit-cookiecutter/tutorial/).
{% if cookiecutter.publish_to_pypi %}

## Releasing

1. Bump the version: `uv version --bump <major|minor|patch>`
2. Commit and push
3. Create a [new release](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/releases/new) on GitHub with a tag matching the version (e.g., `1.0.0`)

The GitHub Action will automatically publish to PyPI. See the [publishing guide](https://samuelduchesne.github.io/project-kit-cookiecutter/features/publishing/) for initial setup.
{%- if cookiecutter.mkdocs %}

> **First release?** After the workflow completes, enable GitHub Pages: go to `Settings > Pages` and select the `gh-pages` branch.
{%- endif %}
{% endif %}

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

*Built with [project-kit-cookiecutter](https://github.com/samuelduchesne/project-kit-cookiecutter)*
