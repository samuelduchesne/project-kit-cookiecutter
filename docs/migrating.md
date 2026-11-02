# Migrating Existing Projects

Have an existing Python project and want to adopt the best practices from this template? This guide covers your options.

## Option 1: Cruft (Recommended)

[Cruft](https://github.com/cruft/cruft) is a tool that links existing projects to cookiecutter templates, allowing you to pull template updates over time.

### Installation

```bash
pip install cruft
# or
uv tool install cruft
```

### Link Your Project

Navigate to your existing project and link it to the template:

```bash
cd my-existing-project
cruft link gh:samuelduchesne/cookiecutter-project-kit
```

Cruft will prompt you for the template variables (project name, author, etc.). Answer them to match your existing project.

This creates a `.cruft.json` file that tracks which template version your project is based on.

### Check for Updates

See if the template has been updated since you linked:

```bash
cruft check
```

Returns exit code 1 if updates are available (useful for CI).

### View Changes

See what changed in the template:

```bash
cruft diff
```

### Apply Updates

Pull template updates into your project:

```bash
cruft update
```

Cruft will show you the changes and ask for confirmation. If there are conflicts with files you've customized, you'll need to resolve them manually (similar to git merge conflicts).

### Skip Files

Some files shouldn't be updated from the template (e.g., your actual source code, tests, README). Add them to the `skip` section in `.cruft.json`:

```json
{
  "template": "gh:samuelduchesne/cookiecutter-project-kit",
  "commit": "abc123...",
  "context": {
    "cookiecutter": {
      "project_name": "my-project",
      ...
    }
  },
  "skip": [
    "README.md",
    "src/my_project/**",
    "tests/**"
  ]
}
```

### CI Integration

Add a check to your CI pipeline to alert when template updates are available:

```yaml
# .github/workflows/main.yml
- name: Check for template updates
  run: |
    pip install cruft
    cruft check || echo "::warning::Template updates available. Run 'cruft update' to apply."
```

## Option 2: Manual Migration

If you prefer not to use Cruft, you can manually adopt template practices:

### 1. Generate a Reference Project

```bash
# Create a fresh project with your settings
uvx cookiecutter gh:samuelduchesne/cookiecutter-project-kit -o /tmp/reference
```

### 2. Copy Configuration Files

Copy these files from the reference project to yours:

| File | Purpose |
|------|---------|
| `pyproject.toml` | Merge with your existing config |
| `Makefile` | Development commands |
| `.pre-commit-config.yaml` | Code quality hooks |
| `.github/workflows/` | CI/CD pipelines |
| `tox.ini` | Multi-version testing |
| `.python-version` | Recommended Python version |

### 3. Key Changes Checklist

- [ ] Migrate from `setup.py`/`setup.cfg` to `pyproject.toml`
- [ ] Add `from __future__ import annotations` to all Python files
- [ ] Set up pre-commit: `uv run pre-commit install`
- [ ] Add type hints and configure type checker
- [ ] Update CI workflows for uv
- [ ] Add Makefile targets

## Option 3: Start Fresh

For heavily divergent projects, it may be easier to:

1. Create a new project from the template
2. Copy your source code into it
3. Adjust configurations as needed

```bash
# Create new project
uvx cookiecutter gh:samuelduchesne/cookiecutter-project-kit

# Copy your code
cp -r old-project/src/* new-project/src/
cp -r old-project/tests/* new-project/tests/

# Install and verify
cd new-project
uv sync
make check && make test
```

## Comparison

| Approach | Effort | Future Updates | Best For |
|----------|--------|----------------|----------|
| **Cruft** | Medium | Automatic | Active projects you maintain long-term |
| **Manual** | High | Manual | One-time adoption, heavily customized projects |
| **Start Fresh** | Low | Automatic | Small projects, major rewrites |

## Tips

1. **Commit before migrating** - Ensure you can revert if something goes wrong
2. **Run tests after each step** - Catch issues early
3. **Review diffs carefully** - Don't blindly accept all template changes
4. **Customize `.cruft.json` skip list** - Protect files you don't want overwritten
