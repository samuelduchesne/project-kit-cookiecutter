# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **cookiecutter template** for generating modern Python projects with uv dependency management. The template itself lives in `{{cookiecutter.project_name}}/` and is processed by cookiecutter to create new projects.

## Common Commands

```bash
# Install dependencies
make install          # or: uv sync

# Run tests
make test             # runs pytest with coverage

# Code quality checks
make check            # runs lock check, pre-commit, mypy, deptry

# Generate a test project (no prompts)
make bake             # creates example-project/ with flat layout
make bake-src         # creates example-project/ with src/ layout
make bake-with-inputs # interactive prompts

# Documentation
make docs             # serve docs locally
make docs-test        # build docs and check for errors

# Multi-version testing
tox                   # test across Python 3.9-3.14
```

## Running a Single Test

```bash
uv run pytest tests/test_cookiecutter.py::test_bake_project -v
```

## Architecture

### Directory Structure

- `{{cookiecutter.project_name}}/` - The cookiecutter template directory containing all files that get copied to generated projects
- `node/` - A second, self-contained template for TypeScript libraries (`cookiecutter.json`, `hooks/`, `local_extensions.py` and `{{cookiecutter.project_name}}/`), generated with `--directory node`. Its `local_extensions.py` must stay identical to the root one (a test checks this). Tests: `tests/test_node_template.py`
- `cookiecutter.json` - Template variables and prompts
- `hooks/` - Pre/post generation scripts:
  - `pre_gen_project.py` - Validates inputs before generation
  - `post_gen_project.py` - Cleans up files based on user choices (removes unused license files, moves to src layout, etc.)
- `tests/` - Template tests using pytest-cookies
- `docs/` - MkDocs documentation for the template itself

### Template Features (controlled by cookiecutter.json)

The template supports various toggleable features:
- `layout`: flat vs src directory structure
- `include_github_actions`, `publish_to_pypi`, `codecov`, `mkdocs`, `dockerfile`, `devcontainer`, `deptry`
- `type_checker`: pyright, ty, mypy, or pyrefly
- `include_agents_md`, `include_copilot`: AI agent instruction files (AGENTS.md, CLAUDE.md, copilot-instructions.md)
- `agent_profile`: minimal (quick reference) or full (comprehensive guidance for AI agents)
- `include_py_typed`: PEP 561 marker for typed packages
- `changelog`: CHANGELOG.md in Keep a Changelog format, plus a changelog rule in agent files and CONTRIBUTING.md
- `open_source_license`: MIT, BSD, ISC, Apache 2.0, GPL v3, or none

### Testing Pattern

Tests use `pytest-cookies` which provides a `cookies` fixture. The pattern is:
```python
def test_feature(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"feature": True})
        assert result.exit_code == 0
        # verify generated files...
```

## Code Style

- Line length: 120 characters
- All Python files require `from __future__ import annotations`
- Ruff for linting/formatting with rules: YTT, S, B, A, C4, T10, SIM, I, C90, E, W, F, PGH, UP, RUF, TRY
- Generated projects additionally enable DTZ, LOG, PIE, PT, RET, TC, PTH, PERF, FURB (see `{{cookiecutter.project_name}}/pyproject.toml`)
- mypy with strict settings (disallow_untyped_defs, check_untyped_defs, etc.)

## Important Notes

- **Linting template files**: Running `ruff` on the entire repo will fail because `{{cookiecutter.project_name}}/` contains Jinja2 template files that aren't valid Python/TOML. Run linting only on `hooks/`, `node/hooks/` and `tests/`:
  ```bash
  uv run ruff check hooks/ node/hooks/ tests/
  ```
- **Template conditionals**: Use `{% if cookiecutter.option %}` for booleans (not `== 'y'`)
