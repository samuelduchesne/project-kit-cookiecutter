# {{cookiecutter.project_name}}

{% if cookiecutter.publish_to_npm -%}
[![npm](https://img.shields.io/npm/v/{{cookiecutter.project_name}})](https://www.npmjs.com/package/{{cookiecutter.project_name}})
{% endif -%}
{% if cookiecutter.include_github_actions -%}
[![Build status](https://img.shields.io/github/actions/workflow/status/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/main.yml?branch=main)](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/actions/workflows/main.yml?query=branch%3Amain)
{% endif -%}
{% if cookiecutter.codecov -%}
[![codecov](https://codecov.io/gh/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})
{% endif -%}
[![License](https://img.shields.io/github/license/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/blob/main/LICENSE)

{{cookiecutter.project_description}}

**[GitHub](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/)**
{%- if cookiecutter.publish_to_npm %}

## Installation

```bash
pnpm add {{cookiecutter.project_name}}
```

Or with npm: `npm install {{cookiecutter.project_name}}`.
{%- endif %}

## Usage

```ts
import { greet } from "{{cookiecutter.project_name}}";

console.log(greet("world"));
```

## Development

This project uses [pnpm](https://pnpm.io/) for dependency management, [Biome](https://biomejs.dev/) for linting and formatting, [TypeScript](https://www.typescriptlang.org/) and [Vitest](https://vitest.dev/). The [pre-commit](https://pre-commit.com/) hooks run with [uv](https://docs.astral.sh/uv/).

### Setup

You need Node.js {{cookiecutter.node_version}} or newer (see `.nvmrc`), pnpm (`npm install -g pnpm`; it switches to the version pinned in `package.json`) and uv.

```bash
git clone https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}.git
cd {{cookiecutter.project_name}}
make install    # install dependencies and pre-commit hooks
```

Commit `pnpm-lock.yaml` after the first install: CI installs with `--frozen-lockfile`.

### Commands

```bash
make install    # Install dependencies and pre-commit hooks
make check      # Lockfile, Biome (through pre-commit) and type checks
make test       # Run tests{% if cookiecutter.codecov %} with coverage{% endif %}
make build      # Compile to dist/
```
{%- if cookiecutter.publish_to_npm %}

## Releasing

1. Bump the version: `npm version <major|minor|patch> --no-git-tag-version`
2. Commit and push
{%- if cookiecutter.include_github_actions %}
3. Create a [new release](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/releases/new) on GitHub with a tag matching the version (e.g., `1.0.0` or `v1.0.0`)

The `release` workflow tests, builds and publishes the package to npm with provenance. Before the first release, add this repository and the `release.yml` workflow as a [trusted publisher](https://docs.npmjs.com/trusted-publishers) for the package on npmjs.com.
{%- else %}
3. Test, build and publish: `make test && make build && pnpm publish --access public`
{%- endif %}
{%- endif %}

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

_Built with [project-kit-cookiecutter](https://github.com/samuelduchesne/project-kit-cookiecutter)_
