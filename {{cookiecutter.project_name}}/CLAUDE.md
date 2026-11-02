# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
{% if cookiecutter.agent_profile == "full" %}
## Project Overview

{{ cookiecutter.project_description }}

This project uses:
- **uv** for dependency management
- **Ruff** for linting and formatting
- **{{ cookiecutter.type_checker }}** for type checking
- **pytest** for testing
{%- if cookiecutter.mkdocs %}
- **MkDocs** for documentation
{%- endif %}
{%- if cookiecutter.dockerfile %}
- **Docker** for containerization
{%- endif %}
{% endif %}
## Common Commands

```bash
# Install dependencies
uv sync

# Run all quality checks (lint, format, type check{% if cookiecutter.deptry %}, deptry{% endif %})
make check

# Run tests
make test

# Run a single test
uv run pytest tests/test_file.py::test_function -v
{%- if cookiecutter.mkdocs %}

# Serve documentation locally
make docs
{%- endif %}
{%- if cookiecutter.dockerfile %}

# Build and run Docker container
make docker-build && make docker-run
{%- endif %}
```
{% if cookiecutter.agent_profile == "full" %}
## Project Structure

```
{% if cookiecutter.layout == "src" %}src/{% endif %}{{ cookiecutter.project_slug }}/    # Main package
tests/              # Test files (mirror source structure)
{%- if cookiecutter.mkdocs %}
docs/               # MkDocs documentation
{%- endif %}
pyproject.toml      # Project configuration and dependencies
```

## Code Style

- **Line length**: 120 characters
- **Imports**: Always include `from __future__ import annotations`
- **Type hints**: Required on all functions (parameters and return types)
- **Docstrings**: Google or NumPy style for public APIs
- **Data models**: Use dataclasses or Pydantic instead of raw dicts

## Testing

Tests live in `tests/` and mirror the source structure. When adding new functionality:

1. Create test file: `tests/test_<module_name>.py`
2. Write tests before or alongside implementation
3. Run tests: `uv run pytest tests/test_<module_name>.py -v`
4. Verify all tests pass: `make test`

Use pytest fixtures (in `conftest.py`) for shared test setup.

## Type Checking

This project uses **{{ cookiecutter.type_checker }}** for static type analysis.

```bash
uv run {{ cookiecutter.type_checker }}{% if cookiecutter.type_checker in ["ty", "pyrefly"] %} check{% endif %}
```

Ensure all new code is fully typed. The configuration is in `pyproject.toml`.
{% endif %}
## Before Committing

Always run the full quality gate before proposing changes:

```bash
make check && make test
```

This runs: lock file validation, pre-commit hooks (ruff format/lint), {{ cookiecutter.type_checker }}{% if cookiecutter.deptry %}, deptry{% endif %}, and pytest.
{%- if cookiecutter.changelog %}

Add an entry under `## [Unreleased]` in `CHANGELOG.md` for user-facing changes, using the Keep a Changelog categories (Added, Changed, Deprecated, Removed, Fixed, Security).
{%- if cookiecutter.agent_profile == "full" %} Create the category heading if it is missing, and skip internal-only changes (refactors, tests, CI):

```markdown
## [Unreleased]

### Fixed

- Handle empty input in `load_config` instead of raising `KeyError`.
```
{%- endif %}
{%- endif %}
{%- if cookiecutter.dvc %}

## DVC Pipeline

This project uses DVC for data versioning and ML pipelines. Pipeline parameters are defined in `params.yaml` and validated using Pydantic.

**Important**: When modifying `params.yaml`, you must also update the schema:

1. Edit `{% if cookiecutter.layout == 'src' %}src/{% endif %}{{ cookiecutter.project_slug }}/schemas/params.py` to add/modify parameter definitions
2. Regenerate JSON schema: `uv run python -c "from {{ cookiecutter.project_slug }}.schemas import PipelineParams; PipelineParams.generate_json_schema()"`
3. Commit both files together

```bash
# Run the pipeline
make dvc-repro

# Check pipeline status
make dvc-status
```
{%- endif %}
