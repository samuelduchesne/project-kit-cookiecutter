# Live Demo Guide

This guide provides a 5-minute live demonstration script for showcasing the cookiecutter template. It's designed for audiences who may not be Python experts.

!!! tip "Quick Start"

    === "macOS / Linux"

        ```bash
        uvx cookiecutter gh:samuelduchesne/project-kit-cookiecutter --no-input
        cd example-project && git init && git add . && make install
        ```

    === "Windows (PowerShell)"

        ```powershell
        uvx cookiecutter gh:samuelduchesne/project-kit-cookiecutter --no-input
        cd example-project
        git init
        git add .
        uv sync
        uv run pre-commit install
        ```

---

## Before the Demo

=== "macOS / Linux"

    ```bash
    # Clean up any previous demo
    rm -rf /tmp/example-project

    # Navigate to a clean directory
    cd /tmp
    ```

=== "Windows (PowerShell)"

    ```powershell
    # Clean up any previous demo
    Remove-Item -Recurse -Force $env:TEMP\example-project -ErrorAction SilentlyContinue

    # Navigate to a clean directory
    cd $env:TEMP
    ```

---

## The Story

> "Starting a new Python project the *right* way typically takes hours:
> setting up testing, linting, documentation, CI/CD, Docker...
>
> This template does it all in **30 seconds**."

---

## Part 1: Generate a Project

### Run the command

=== "macOS / Linux"

    ```bash
    uvx cookiecutter gh:samuelduchesne/project-kit-cookiecutter
    ```

=== "Windows (PowerShell)"

    ```powershell
    uvx cookiecutter gh:samuelduchesne/project-kit-cookiecutter
    ```

### Answer the prompts

Press Enter to accept defaults, or pause on key prompts to explain:

| Prompt | Explanation |
|--------|-------------|
| `author` | Your name goes in all the right places - README, LICENSE, pyproject.toml |
| `project_name` | This becomes your folder name and Python package name |
| `layout` | Flat is simpler, src/ layout is for larger projects |
| `include_github_actions` | Free CI/CD on every push to GitHub |
| `dockerfile` | Ready for containerization with Docker or Podman |
| `agent_instructions` | Instructions for AI coding assistants (Copilot, Codex, Claude, Cursor) |

!!! tip
    Press Enter rapidly through the prompts to show how quick it is!

---

## Part 2: Explore What You Got

### Show the structure

=== "macOS / Linux"

    ```bash
    cd example-project
    tree -L 2 -a --dirsfirst
    ```

=== "Windows (PowerShell)"

    ```powershell
    cd example-project
    tree /F
    ```

    Or for a cleaner view, use:

    ```powershell
    Get-ChildItem -Recurse -Depth 2 | Select-Object FullName
    ```

One command gave us a complete project structure - 23 files across 9 directories.

### Highlight key files

=== "macOS / Linux"

    ```bash
    # Show the main code file
    cat example_project/__init__.py

    # Show the test
    cat tests/test_foo.py

    # Show the pyproject.toml (modern Python standard)
    head -30 pyproject.toml
    ```

=== "Windows (PowerShell)"

    ```powershell
    # Show the main code file
    Get-Content example_project\__init__.py

    # Show the test
    Get-Content tests\test_foo.py

    # Show the pyproject.toml (modern Python standard)
    Get-Content pyproject.toml -TotalCount 30
    ```

Your package is ready to import. Tests are already set up and passing. All dependencies and tool configs in one place - the modern Python way.

---

## Part 3: Everything Works Out of the Box

### Initialize git and install dependencies

=== "macOS / Linux"

    ```bash
    git init && git add .
    make install
    ```

=== "Windows (PowerShell)"

    ```powershell
    git init
    git add .
    uv sync
    uv run pre-commit install
    ```

Git is required for the pre-commit hooks. uv installs everything in seconds - it's 10-100x faster than pip.

### Run the tests

=== "macOS / Linux"

    ```bash
    make test
    ```

=== "Windows (PowerShell)"

    ```powershell
    uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml
    ```

Tests pass with coverage reporting included.

### Run code quality checks

=== "macOS / Linux"

    ```bash
    make check
    ```

=== "Windows (PowerShell)"

    ```powershell
    uv lock --locked
    uv run pre-commit run -a
    uv run mypy
    uv run deptry .
    ```

Linting, type checking, and dependency checking - all configured and passing.

!!! note
    The first run may auto-fix minor formatting issues - that's the pre-commit hooks doing their job!

---

## Part 4: Explore the Tooling

### Show the Makefile

=== "macOS / Linux"

    ```bash
    cat Makefile
    ```

=== "Windows (PowerShell)"

    ```powershell
    Get-Content Makefile
    ```

Everything is documented. New team members can get started immediately.

### Show GitHub Actions

=== "macOS / Linux"

    ```bash
    cat .github/workflows/main.yml
    ```

=== "Windows (PowerShell)"

    ```powershell
    Get-Content .github\workflows\main.yml
    ```

Push to GitHub and CI runs automatically - tests, linting, everything.

### Show the documentation site

=== "macOS / Linux"

    ```bash
    make docs
    ```

=== "Windows (PowerShell)"

    ```powershell
    uv run mkdocs serve
    ```

Your documentation site is ready at `localhost:8000`.

---

## Summary

What we created in 30 seconds would normally take hours:

- Dependency management with uv
- Testing setup with pytest and coverage
- Code quality tools (ruff, mypy, deptry)
- CI/CD pipeline with GitHub Actions
- Documentation site with MkDocs
- Docker support
- AI assistant instructions (AGENTS.md, CLAUDE.md, .cursorrules, .github/copilot-instructions.md)

All following best practices, all working together.

---

## Recovery Commands

If something goes wrong:

=== "macOS / Linux"

    ```bash
    # Start fresh
    cd /tmp && rm -rf example-project

    # Skip prompts with defaults
    uvx cookiecutter gh:samuelduchesne/project-kit-cookiecutter --no-input

    # Quick setup after generation
    cd example-project && git init && git add . && make install
    ```

=== "Windows (PowerShell)"

    ```powershell
    # Start fresh
    cd $env:TEMP
    Remove-Item -Recurse -Force example-project -ErrorAction SilentlyContinue

    # Skip prompts with defaults
    uvx cookiecutter gh:samuelduchesne/project-kit-cookiecutter --no-input

    # Quick setup after generation
    cd example-project
    git init
    git add .
    uv sync
    uv run pre-commit install
    ```

---

## Presentation Tips

1. **Increase font size** - Terminal should be readable from the back of the room
2. **Pre-type long commands** - Copy/paste from this guide
3. **Pause after each section** - Let the output sink in
4. **Have backup** - Keep a pre-generated project ready in case of network issues
