# Agent Instructions

This cookiecutter template can generate instruction files for various AI coding agents. Use the `agent_instructions` option to select which agents to configure.

## Available Options

| Option | Files Generated | Description |
|--------|----------------|-------------|
| `suggested` (default) | `AGENTS.md`, `.github/copilot-instructions.md` | Copilot + Codex — recommended for most projects |
| `codex` | `AGENTS.md` | OpenAI Codex/ChatGPT instructions |
| `claude` | `CLAUDE.md` | Claude Code instructions |
| `copilot` | `.github/copilot-instructions.md` | GitHub Copilot instructions |
| `cursor` | `.cursorrules` | Cursor editor instructions |
| `all` | All files | All agent instruction files |
| `none` | None | No agent instructions |

## Agent Profile

You can choose between two detail levels with `agent_profile`:

- **Minimal**: A lightweight version with essential commands and quality gates
- **Full**: A comprehensive version with detailed guidelines, project structure, code conventions, and common task workflows

When `changelog` is `true`, every generated agent file also tells agents to add an entry under `## [Unreleased]` in
`CHANGELOG.md` for user-facing changes. See [Changelog with Keep a Changelog](./changelog.md).

## AGENTS.md (Codex)

The `AGENTS.md` file provides concise, actionable instructions for AI coding agents. This format is recognized by OpenAI's Codex and many other AI assistants. It includes:

- **Environment setup**: How to install dependencies using uv
- **Quality gates**: Commands to run before proposing changes (formatting, linting, type checking, tests)
- **Conventions**: Code style guidelines (line length, docstring formats)
- **PR etiquette**: Best practices for pull requests

### Example AGENTS.md content

```markdown
# AGENTS.md — rules for coding agents

> This repository follows the uv/Ruff/mypy/pytest stack.

## Environment & install

- Use **uv** for everything.
- Install: `uv sync`
- Run commands with `uv run …`

## Quality gate (do these before proposing changes)

- Format: `uv run ruff format .`
- Lint:   `uv run ruff check .`
- Types:  `uv run mypy .`
- Tests:  `uv run pytest -q`

## PR etiquette

- Small, focused PRs.
- Include/adjust tests and docs.
- Use Conventional Commits in the title.
```

## CLAUDE.md (Claude Code)

The `CLAUDE.md` file provides project-specific guidance for Claude Code (claude.ai/code). It follows Claude's conventions for project instructions and includes:

- Project overview and technology stack
- Common commands for development workflow
- Project structure explanation
- Code style and type checking requirements
- Testing guidelines

## .github/copilot-instructions.md (GitHub Copilot)

The `.github/copilot-instructions.md` file provides detailed guidelines for GitHub Copilot code generation:

### Project Context & Environment

- Specifies that the project uses **uv** for dependency management
- Ensures all Python commands run through the `.venv` virtual environment

### Typing & Data Models

- Enforces **strong typing** with type annotations for all code
- Prefers `@dataclass` or Pydantic models over unstructured dictionaries
- Requires triple-quoted documentation for all dataclass attributes

### Function & Method Signatures

- Requires explicit type annotations for parameters and return values
- Uses `-> None` explicitly for functions without return values

### Testing

- Generates unit tests alongside implementations
- Covers both happy-path and error conditions
- Uses explicit type/attribute assertions

## .cursorrules (Cursor)

The `.cursorrules` file provides instructions for the Cursor editor's AI features. It includes:

- Environment setup with uv
- Quality gate commands
- Code conventions (when using the full profile)
- Project structure overview
- PR guidelines

## Benefits

By configuring agent instructions, you:

1. **Ensure consistency**: All AI-generated code follows your project's conventions
2. **Improve code quality**: Agents automatically apply best practices and type safety
3. **Reduce review time**: Generated code meets quality standards from the start
4. **Accelerate onboarding**: New contributors (human or AI) quickly understand the workflow
5. **Maintain standards**: Project guidelines are enforced automatically during code generation

## Configuration

To configure agent instructions when generating your project:

```bash
# Use the suggested combination (Copilot + Codex)
agent_instructions: "suggested"

# Or choose a specific agent
agent_instructions: "claude"

# Choose the detail level
agent_profile: "full"  # or "minimal"
```

These options can be set when running cookiecutter, or configured in your `cookiecutter.json` defaults.
