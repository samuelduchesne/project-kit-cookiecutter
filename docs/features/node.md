# Node (TypeScript) template

project-kit-cookiecutter also holds a template for TypeScript libraries, in the `node/` folder of the repository. It applies the same standards as the Python template (linting and formatting through pre-commit, a Keep a Changelog `CHANGELOG.md`, agent instructions, GitHub Actions, a license choice and a devcontainer) to a Node project.

## Generate a project

Pass the folder with `--directory`:

```bash
uvx cookiecutter https://github.com/samuelduchesne/project-kit-cookiecutter.git --directory node
```

With [cruft](https://cruft.github.io/cruft/), so the project can be updated later:

```bash
uvx cruft create https://github.com/samuelduchesne/project-kit-cookiecutter.git --directory node
```

The project-kit plugin's `new-project` workflow does this for you when you ask for a Node project.

## What you get

| Concern | Tool |
|---------|------|
| Package manager | [pnpm](https://pnpm.io/), pinned in `packageManager` (install pnpm with `npm install -g pnpm`; it switches to the pinned version. Node.js 25 and later no longer include corepack) |
| Language | TypeScript, strict, ES modules; `tsc` builds `dist/` with type declarations |
| Tests | [Vitest](https://vitest.dev/) with V8 coverage |
| Linting and formatting | [Biome](https://biomejs.dev/), run by a local pre-commit hook with the project's own Biome version |
| Other hooks | The Python template's generic pre-commit hooks (merge conflicts, YAML, JSON, end of file, trailing whitespace) |
| CI | `make check` and a test-and-build matrix from the chosen Node version up |

`make install` installs the dependencies and the pre-commit hooks, `make check` runs the lockfile, pre-commit and type checks, `make test` runs the tests and `make build` compiles. The pre-commit hooks run with `uvx`, so contributors need [uv](https://docs.astral.sh/uv/) as well as Node and pnpm.

Commit `pnpm-lock.yaml` after the first `make install`: CI installs with `--frozen-lockfile`.

## Options

| Option | Default | Effect |
|--------|---------|--------|
| `project_name` | `example-project` | Folder and npm package name: lowercase letters, digits and `-`, starting with a letter |
| `node_version` | `24` | Minimum Node version (`engines`), `.nvmrc`, devcontainer image and the lowest CI version; `22` and `26` are also offered |
| `include_github_actions` | `true` | `.github/workflows/main.yml` |
| `codecov` | `true` | Coverage upload in CI, `codecov.yaml` and the badge |
| `publish_to_npm` | `false` | `.github/workflows/release.yml`, which publishes to npm with provenance when a GitHub release is published; otherwise the package is `private` |
| `devcontainer` | `true` | `.devcontainer/devcontainer.json` |
| `changelog` | `true` | `CHANGELOG.md` and the changelog rule in the agent files and `CONTRIBUTING.md` |
| `agent_instructions`, `agent_profile` | `suggested`, `minimal` | Same as the Python template, see [Agent Instructions](./agents.md) |
| `open_source_license` | `MIT license` | `LICENSE` and the `license` field (`UNLICENSED` for "Not open source") |

## Publishing to npm

The release workflow uses [npm trusted publishing](https://docs.npmjs.com/trusted-publishers): no token is stored in the repository. Before the first release, add the repository and the `release.yml` workflow as a trusted publisher of the package on npmjs.com. Then bump the version (`npm version <major|minor|patch> --no-git-tag-version`), commit, push, and publish a GitHub release whose tag matches the version (`1.2.0` or `v1.2.0`).
