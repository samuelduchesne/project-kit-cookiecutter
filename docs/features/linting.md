# Linting and code quality

Code can be linted and quality-checked with the command

```bash
make check
```

Note that this requires the pre-commit hooks to be installed.

This command will run the following tools:

## ruff

[ruff](https://github.com/charliermarsh/ruff) is used to lint and format the code, and it is configured through `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py39"
line-length = 120
fix = true

[tool.ruff.lint]
select = [
    "YTT",   # flake8-2020
    "S",     # flake8-bandit
    "DTZ",   # flake8-datetimez
    "LOG",   # flake8-logging
    "PIE",   # flake8-pie
    "PT",    # flake8-pytest-style
    "RET",   # flake8-return
    "TC",    # flake8-type-checking
    "PTH",   # flake8-use-pathlib
    "B",     # flake8-bugbear
    "A",     # flake8-builtins
    "C4",    # flake8-comprehensions
    "T10",   # flake8-debugger
    "SIM",   # flake8-simplify
    "I",     # isort
    "C90",   # mccabe
    "E", "W",  # pycodestyle
    "F",     # pyflakes
    "PGH",   # pygrep-hooks
    "UP",    # pyupgrade
    "RUF",   # ruff
    "TRY",   # tryceratops
    "PERF",  # perflint
    "FURB",  # refurb
]
ignore = [
    "E501",  # LineTooLong
    "E731",  # DoNotAssignLambda
]
# Let TC fixes add `from __future__ import annotations` instead of quoting types
future-annotations = true

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]

[tool.ruff.format]
preview = true
```

The rule families beyond the core pyflakes/pycodestyle/isort set are taken from the ones Ruff itself
enables by default since v0.16 (datetimes, logging, pytest style, pathlib, performance, refurb and
type-checking imports). Because the template sets an explicit `select`, upgrading Ruff never changes
which rules run in your project.

Formatter preview mode only opts into the two styles Ruff still marks as preview since its 2026 style
guide (v0.15): fluent method-chain layout and bracket hugging. Remove `preview = true` if you prefer
the stable style only.

## mypy

[mypy](https://mypy.readthedocs.io/en/stable/) is used for static type checking, and it's configuration can be edited in `pyproject.toml`.

```toml
[tool.mypy]
disallow_untyped_defs = true
disallow_any_unimported = true
no_implicit_optional = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true
exclude = [
    '\.venv',
    '{{cookiecutter.project_name}}',
    'tests'
]
```

## ty

[ty](https://docs.astral.sh/ty/) is an extremely fast type checker (and language server) that can be used instead of mypy, and it's configuration can be edited in `pyproject.toml`.

```toml
[tool.ty.environment]
python = "./.venv"
python-version = "3.9"

[tool.ty.terminal]
error-on-warning = true
```

ty is still in beta (0.0.x), and its defaults and diagnostics can change between releases. The template
therefore pins an exact version (`ty==0.0.94`) in the dev dependency group; bump it deliberately.
ty has no single strict preset: tune individual rules under `[tool.ty.rules]`.

## pyrefly

[Pyrefly](https://pyrefly.org/) is a fast type checker and language server from Meta that reached a
stable 1.0 in 2026. The template enables its `strict` preset, because without a preset Pyrefly only runs
a minimal set of checks.

```toml
[tool.pyrefly]
project-includes = ["example_project", "tests"]
python-version = "3.9"
preset = "strict"
```

If you are migrating an existing mypy project, `uv run pyrefly init` converts a `[tool.mypy]`
configuration.

## pyright

[pyright](https://microsoft.github.io/pyright/) is a fast type checker for Python created by Microsoft. It's the type checker that powers Pylance in VS Code. Configuration can be edited in `pyproject.toml`.

```toml
[tool.pyright]
pythonVersion = "3.9"
typeCheckingMode = "strict"
```

## deptry

[deptry](https://github.com/osprey-oss/deptry) is used to check the code for dependency issues, and it can be configured by adding a `[tool.deptry]` section in `pyproject.toml`. For more information, see [this section](https://deptry.com/usage/#configuration) documentation of deptry.

## Github Actions

If `include_github_actions` is set to `true`, code formatting is checked
for every merge request, every merge to main, and every release.
