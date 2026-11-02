# Prompt arguments

When running the command `ccp` a prompt will start which enables you to configure your repository. The
prompt values and their explanation are as follows:

---

**author**

Your full name.

**email**

Your email address.

**author_github_handle**

Your github handle, i.e. `<handle>` in `https://github.com/<handle>`

**project_name**

Your project name. Should be equal to the name of your repository
and it should only contain alphanumeric characters and `-`'s.

**project_slug**

The project slug, will default to the `project_name` with all `-`'s
replaced with `_`. This will be how you import your code later, e.g.

```python
from <project_slug> import foo
```

**project_description**

A short description of your project.

**layout**

`"flat"` or `"src"`, defaults to `"flat"`.

- `"flat"`: Places the Python module in the root directory.
- `"src"`: Organizes the project by placing the Python module inside a `src` directory.

> **Tip for beginners:** Choose `flat` for simplicity. Use `src` layout if you're publishing a library to PyPI (it prevents accidental imports from the wrong location during development).

**minimum_python_version**

The oldest Python version the project supports: `"3.9"` to `"3.14"`, defaults to `"3.9"`. It sets
`requires-python`, the PyPI classifiers, ruff's `target-version`, the type checker's Python version,
and the CI and tox test matrix (every version from the minimum up to 3.14).

> **Tip for beginners:** Choose `3.11` unless you need to support older systems.

**development_python_version**

The Python version you develop with: `"3.9"` to `"3.14"`, defaults to `"3.14"`. It is written to
`.python-version` (which uv uses to pick the interpreter) and sets the Docker base image
(`python:<version>-slim`) and the devcontainer image (`mcr.microsoft.com/devcontainers/python:<version>`).
It must be greater than or equal to `minimum_python_version`; otherwise project generation fails.
Images for Python versions past end-of-life no longer receive updates.

> **Boolean options on the command line:** the `true`/`false` options below accept any of `true`/`false`,
> `yes`/`no`, `y`/`n`, `on`/`off` and `1`/`0`, in any case, e.g.
> `uvx cookiecutter gh:samuelduchesne/project-kit-cookiecutter --no-input changelog=false dvc=yes`.
> Any other value stops generation with an error.

**include_github_actions**

`true` or `false`. Adds a `.github` directory with various actions and
workflows to setup the environment and run code formatting checks
and unittests.

**publish_to_pypi**

`true` or `false`. Adds functionality to the
`Makefile` and Github workflows to make publishing your code as
simple as creating a new release release on Github. For more info,
see
[Publishing to PyPI](./features/publishing.md).

**deptry**

`true` or `false`. Adds [deptry](https://deptry.com/)
to the development dependencies of the project, and adds it to the `make check` command. `deptry` is a command line tool to check for issues with dependencies in a Python project, such as obsolete or missing dependencies.

**mkdocs**

`true` or `false`. Adds [MkDocs](https://www.mkdocs.org/)
documentation to your project. This includes automatically parsing
your docstrings and adding them to the documentation. Documentation
will be deployed to the `gh-pages` branch.

**codecov**

`true` or `false`. Adds code coverage checks with [codecov](https://about.codecov.io/).

**dockerfile**

`true` or `false`. Adds a simple [Dockerfile](https://docker.com).

**devcontainer**

`true` or `false`. Adds a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) specification to the project along with pre-installed pre-commit hooks and VSCode python extension configuration.

**dvc**

`true` or `false`. Adds [DVC (Data Version Control)](https://dvc.org/) for data versioning, ML pipelines, and experiment tracking. Includes a sample pipeline configuration (`dvc.yaml`), parameters file (`params.yaml`), and data directory structure. Ideal for data science and machine learning projects. The pipeline's parameter schema imports `pydantic` and `pyyaml` at runtime, so they are added to the project's `dependencies`; `dvc` itself (and `types-PyYAML` when `type_checker` is `mypy`) goes in the `dev` dependency group.

**changelog**

`true` or `false`, defaults to `true`. Adds a `CHANGELOG.md` in the
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) format, with an `## [Unreleased]` section ready for the
first entries. When enabled, the generated agent instruction files and `CONTRIBUTING.md` remind contributors to log
user-facing changes under `## [Unreleased]`, and the changelog is added to the MkDocs navigation if `mkdocs` is `true`.
For more info, see [Changelog with Keep a Changelog](./features/changelog.md).

**type_checker**

The type checker to use in the generated project. Supported values are `pyright`, `ty`, `mypy`, and `pyrefly`. When enabled, the project will include configuration and CI steps (where applicable) to run the selected type checker.

> **Tip for beginners:** Choose `pyright` — it's fast and has excellent VS Code integration.

**agent_instructions**

Select which AI coding agent instruction files to include. Options:

- `"suggested"` (default): Copilot + Codex — includes both `.github/copilot-instructions.md` and `AGENTS.md`
- `"codex"`: Codex only — includes `AGENTS.md`
- `"claude"`: Claude only — includes `CLAUDE.md`
- `"copilot"`: Copilot only — includes `.github/copilot-instructions.md`
- `"cursor"`: Cursor only — includes `.cursorrules`
- `"all"`: All agents — includes all instruction files
- `"none"`: No agent instructions

**include_py_typed**

`true` or `false`. Includes a `py.typed` marker file in the package so downstream consumers know the package exposes type information. Recommended for libraries that expose type hints.

> **Tip for beginners:** Leave as `true` unless you know you don't need it. This only matters if others will import your package as a library.

**agent_profile**

Select an agent profile from the available options. Choices include `minimal` and `full`.

- `minimal`: A small, lightweight agent configuration with minimal dependencies and examples.
- `full`: A more feature-complete agent configuration with additional example code, documentation, and optional dependencies.

**open_source_license**

Choose a [license](https://choosealicense.com/). Options:
`["1. MIT License", "2. BSD license", "3. ISC license",  "4. Apache Software License 2.0", "5. GNU General Public License v3", "6. Not open source"]`

---
