# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
{% if cookiecutter.agent_profile == "full" %}
## Project Overview

{{ cookiecutter.project_description }}

This project uses:
- **pnpm** for dependency management
- **Biome** for linting and formatting
- **TypeScript** (strict) for type checking and the build
- **Vitest** for testing
{% endif %}
## Common Commands

```bash
# Install dependencies
pnpm install

# Run all quality checks (lockfile, Biome through pre-commit, tsc)
make check

# Run tests
make test

# Run a single test file
pnpm vitest run tests/index.test.ts

# Build to dist/
make build
```
{% if cookiecutter.agent_profile == "full" %}
## Project Structure

```
src/                # Library source; src/index.ts is the entry point
tests/              # Vitest tests (*.test.ts)
package.json        # Manifest, scripts and dependencies
tsconfig.json       # Type checking; tsconfig.build.json emits dist/
biome.json          # Lint and format rules
```

## Code Style

- **Line length**: 120 characters
- **Modules**: ES modules; relative imports end in `.js`
- **Types**: strict TypeScript, no `any`; `import type` for type-only imports
- **Docs**: TSDoc on every export
{% endif %}
## Before Committing

Always run the full quality gate before proposing changes:

```bash
make check && make test
```

This runs: lockfile validation, pre-commit hooks (Biome lint and format), tsc and Vitest.
{%- if cookiecutter.changelog %}

Add an entry under `## [Unreleased]` in `CHANGELOG.md` for user-facing changes, using the Keep a Changelog categories (Added, Changed, Deprecated, Removed, Fixed, Security).
{%- if cookiecutter.agent_profile == "full" %} Create the category heading if it is missing, and skip internal-only changes (refactors, tests, CI):

```markdown
## [Unreleased]

### Fixed

- Reject an empty name in `greet` instead of returning `Hello, !`.
```
{%- endif %}
{%- endif %}
