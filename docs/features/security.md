# Security Features

This cookiecutter template implements a **defense-in-depth security architecture** with multiple layers of protection enabled by default. Every generated project ships with industry-standard security tooling configured and enforced.

## Overview

| Layer | Tool/Feature | Protection |
|-------|-------------|------------|
| Static Analysis | Ruff + Bandit (S rules) | Vulnerability detection |
| Type Safety | pyright/mypy/ty (strict) | Type confusion prevention |
| Dependency Security | uv lock + deptry | Supply chain protection |
| Pre-commit Hooks | 8+ validation hooks | Input sanitization |
| CI/CD | GitHub Actions | Automated enforcement |
| Containers | Docker slim images | Minimal attack surface |

## Static Security Analysis with Bandit

The template enables comprehensive security scanning via Ruff's [flake8-bandit](https://github.com/PyCQA/bandit) integration. The `"S"` rules are enabled by default in `pyproject.toml`:

```toml
[tool.ruff.lint]
select = [
    "S",        # flake8-bandit - security scanner
    # ... other rules
]
```

### What Bandit Detects

Bandit scans for common security vulnerabilities including:

| Rule Range | Category | Examples |
|------------|----------|----------|
| S101-S113 | General | Assert in production, exec(), hardcoded passwords |
| S301-S324 | Cryptography | Insecure pickle, weak hashes (MD5, SHA1), insecure random |
| S501-S509 | Network | SSL/TLS validation disabled, HTTP without TLS |
| S601-S612 | Injection | Shell injection, SQL injection, code injection |
| S701-S703 | Templates | Jinja2 autoescape disabled, Django XSS |

### Example Detections

```python
# S105: Hardcoded password - DETECTED
password = "secret123"

# S608: SQL injection - DETECTED
query = f"SELECT * FROM users WHERE id = {user_id}"

# S301: Insecure pickle - DETECTED
data = pickle.loads(untrusted_data)

# S324: Insecure hash - DETECTED
hashlib.md5(data)
```

!!! note "Test Exemption"
    Only `S101` (assert usage) is exempted in tests. All other security rules remain enforced.

## Type Safety

Strict type checking prevents type confusion attacks and ensures data validation:

=== "pyright (default)"

    ```toml
    [tool.pyright]
    pythonVersion = "3.9"
    typeCheckingMode = "strict"
    ```

=== "mypy"

    ```toml
    [tool.mypy]
    disallow_untyped_defs = true
    disallow_any_unimported = true
    no_implicit_optional = true
    check_untyped_defs = true
    warn_return_any = true
    ```

=== "ty"

    ```toml
    [tool.ty.environment]
    python-version = "3.9"
    ```

### Security Benefits

- **Type confusion prevention**: Catches mismatched types that could lead to vulnerabilities
- **Input validation**: Forces explicit type declarations on function boundaries
- **Data flow tracking**: Warns when `Any` types bypass validation

## Dependency Security

### Locked Dependencies

The template uses `uv` with locked dependencies to prevent supply chain attacks:

```bash
# Verified in CI/CD
uv lock --locked
```

This ensures:

- No unexpected dependency upgrades
- Reproducible builds across environments
- Protection against dependency injection attacks

### Dependency Auditing with Deptry

When `deptry` is enabled (default), it scans for:

- **Unused dependencies**: Reduces attack surface
- **Obsolete packages**: Flags deprecated libraries
- **Missing dependencies**: Catches incomplete requirements

```bash
make check  # Includes deptry scan
```

## Pre-commit Security Hooks

The `.pre-commit-config.yaml` includes validation hooks that run before every commit:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: check-yaml          # Prevents YAML injection
      - id: check-toml          # Validates TOML syntax
      - id: check-json          # Validates JSON syntax
      - id: check-merge-conflict # Detects unresolved conflicts

  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff-check          # Security + linting rules
      - id: ruff-format         # Consistent formatting
```

### Security Value

- Prevents malformed configuration files that could bypass security controls
- Enforces consistent formatting (malicious code is harder to hide)
- Validates all structured data formats before commit

## CI/CD Security

### GitHub Actions Hardening

The generated workflows follow security best practices:

```yaml
# Pinned action versions (not @latest)
- uses: actions/checkout@v4
- uses: actions/cache@v4

# Secrets via environment variables
env:
  CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

### Security Controls

| Practice | Implementation |
|----------|----------------|
| Pinned versions | All actions use specific versions (`v4`, `v5`) |
| Secret isolation | Credentials via GitHub Secrets, never in code |
| Multi-version testing | Python 3.9-3.14 matrix testing |
| Mandatory checks | `make check` must pass before merge |

## Secrets Management

### .gitignore Protection

The template excludes sensitive files by default:

```gitignore
# Environment files
.env
.envrc

# Credentials
.pypirc
.netrc

# Virtual environments
.venv/
venv/
```

### CI/CD Secrets

Secrets are managed via GitHub repository settings:

| Secret | Purpose |
|--------|---------|
| `PYPI_TOKEN` | PyPI publishing authentication |
| `CODECOV_TOKEN` | Code coverage reporting |
| `AWS_ACCESS_KEY_ID` | DVC S3 storage (optional) |
| `GCP_SERVICE_ACCOUNT_KEY` | DVC GCS storage (optional) |

## Container Security

When `dockerfile` is enabled, the generated Dockerfile follows security best practices:

```dockerfile
# Minimal base image (smaller attack surface)
FROM python:3.14-slim

# Locked dependencies
RUN uv sync --locked

# BuildKit cache mounts (prevents cache poisoning)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked
```

### Security Features

- **Minimal base image**: `python:3.14-slim` has fewer packages to exploit
- **Locked dependencies**: `--locked` flag ensures exact versions
- **No secrets in image**: Credentials passed at runtime via environment
- **BuildKit caching**: Secure cache management

## Input Validation

The pre-generation hook validates all user inputs:

```python
# hooks/pre_gen_project.py
PROJECT_NAME_REGEX = r"^[-a-zA-Z][-a-zA-Z0-9]+$"
PROJECT_SLUG_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
```

This prevents:

- Command injection via malformed project names
- Path traversal vulnerabilities
- Invalid Python module names

## The Security Gate

All security checks are enforced via a single command:

```bash
make check
```

This runs:

1. `uv lock --locked` - Dependency consistency
2. `uv run pre-commit run -a` - All pre-commit hooks (including Bandit)
3. `uv run pyright` (or mypy/ty) - Type checking
4. `uv run deptry .` - Dependency audit (if enabled)

!!! warning "CI/CD Enforcement"
    The `make check` command runs in CI/CD on every pull request and push to main. Code cannot be merged if any security check fails.

## Summary

This template provides enterprise-grade security out of the box:

- **OWASP Top 10 coverage** via Bandit rules
- **Supply chain protection** via locked dependencies
- **Type safety** via strict type checking
- **Secret protection** via .gitignore and GitHub Secrets
- **Container hardening** via minimal images and locked deps
- **Automated enforcement** via CI/CD pipelines

All security features are enabled by default and enforced automatically.
