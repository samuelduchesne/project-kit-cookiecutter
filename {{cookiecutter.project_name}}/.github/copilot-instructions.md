---
description: "Copilot guidelines for the {{ cookiecutter.project_name }} project"
applyTo: "**/*.py"
---

# Copilot Instructions — {{ cookiecutter.project_name }}

Below are the conventions Copilot should follow when writing Python code in this repository.

## Project Environment

- Use **uv** for dependency management and running commands
- Virtual environment is in `.venv/` — always use `uv run` to execute Python
- Run quality checks: `make check` | Run tests: `make test`
{% if cookiecutter.agent_profile == "full" %}
## Type System Requirements

- **All code must be strongly typed** using the typing module
- Annotate all function parameters and return types
- Use `-> None` explicitly for void functions
- Prefer modern syntax: `list[T]` over `List[T]`, `X | None` over `Optional[X]`

## Data Modeling

- **Never use unstructured `dict[str, Any]`** for domain models or APIs
- Use `@dataclass` from dataclasses for simple structured types
- Use Pydantic `BaseModel` when validation/serialization is needed
- Document dataclass attributes with inline triple-quoted strings:

```python
@dataclass
class Item:
    id: int
    """Unique identifier for the item; must be positive."""
    name: str
    """Human-readable name of the item."""
    tags: list[str] | None = None
    """Optional list of tag strings; None when unset."""
```

## Function & Method Guidelines

- Keep functions focused and small (~50 lines max)
- Always annotate parameter types and return types
- Use explicit exceptions with custom types for domain errors
- Document exceptions in docstrings with `Raises:` blocks
- Avoid broad `except Exception:` — be specific

## Project Structure

Organize modules by domain:
```
{% if cookiecutter.layout == "src" %}src/{% endif %}{{ cookiecutter.project_slug }}/
├── models/      # Data models and types
├── services/    # Business logic
├── utils/       # Shared utilities
└── ...
```

## Error Handling

- Validate inputs at function boundaries (fail fast)
- Use specific exception types for domain errors
- Separate pure logic from side effects (I/O, network, DB)
- Avoid global mutable state

## Testing

- Generate unit tests alongside implementations
- Cover both success cases and error conditions
- Use pytest fixtures for shared setup
- Prefer dependency injection over heavy mocking
- Assert types/attributes explicitly

```python
def test_invalid_input_raises_value_error():
    with pytest.raises(ValueError, match="expected pattern"):
        function_under_test(invalid_input)
```
{%- if cookiecutter.changelog %}

## Changelog

- Add an entry under `## [Unreleased]` in `CHANGELOG.md` for user-facing changes, using the Keep a Changelog categories (Added, Changed, Deprecated, Removed, Fixed, Security)
- Create the category heading if it is missing; skip internal-only changes (refactors, tests, CI)

```markdown
## [Unreleased]

### Fixed

- Handle empty input in `load_config` instead of raising `KeyError`.
```
{%- endif %}
{%- else %}
## Quick Reference

- **Types**: All functions must have type annotations
- **Data**: Use dataclasses/Pydantic, not raw dicts
- **Errors**: Use specific exceptions, document with `Raises:`
- **Tests**: Write tests for all new code
- **Style**: 120 char line length, Google/NumPy docstrings
{%- if cookiecutter.changelog %}
- **Changelog**: Add an entry under `## [Unreleased]` in `CHANGELOG.md` for user-facing changes, using the Keep a Changelog categories (Added, Changed, Deprecated, Removed, Fixed, Security)
{%- endif %}
{%- endif %}
