# Changelog with Keep a Changelog

If `changelog` is set to `true` (the default), the generated project includes a `CHANGELOG.md` that follows the
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) format. Recording changes as they land, rather than
reconstructing them from commit history at release time, gives contributors, release tooling and AI coding agents a
single place to read and update.

## What's Included

The generated `CHANGELOG.md` starts with:

- The standard Keep a Changelog header, linking to [keepachangelog.com](https://keepachangelog.com/en/1.1.0/) and
  [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- An `## [Unreleased]` section with an `### Added` entry for the initial project scaffold
- An `[Unreleased]` link reference pointing at the commit history of the `main` branch on GitHub, since no releases
  exist yet

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial project scaffold generated from [project-kit-cookiecutter](https://github.com/samuelduchesne/project-kit-cookiecutter).

[Unreleased]: https://github.com/<handle>/<project_name>/commits/main
```

## Integration with Other Options

When `changelog` is `true`:

- **Agent instructions**: every generated agent file (`AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`,
  `.cursorrules`) tells agents to add an entry under `## [Unreleased]` for user-facing changes. The `minimal`
  `agent_profile` keeps this to one line; the `full` profile adds a short example.
- **CONTRIBUTING.md**: the pull request guidelines include a reminder to update `CHANGELOG.md` under `[Unreleased]`.
- **MkDocs**: if `mkdocs` is `true`, a `Changelog` page is added to the docs navigation. It includes the root
  `CHANGELOG.md` with the `pymdownx.snippets` extension, so there is only one file to maintain.

When `changelog` is `false`, none of these files or rules are generated.

## Conventions

Keep a Changelog groups entries under these categories, in this order:

| Category | Use for |
|----------|---------|
| `Added` | New features |
| `Changed` | Changes in existing functionality |
| `Deprecated` | Features that will be removed in an upcoming release |
| `Removed` | Features removed in this release |
| `Fixed` | Bug fixes |
| `Security` | Fixes for vulnerabilities |

A few rules keep the file useful:

- Write entries for people using the project, not for the commit log. Internal refactors, test and CI changes
  usually do not need an entry.
- Add new entries under `## [Unreleased]`, creating the category heading if it is missing.
- When cutting a release, rename `## [Unreleased]` to `## [x.y.z] - YYYY-MM-DD`, add a fresh empty
  `## [Unreleased]` section above it, and update the link references at the bottom of the file:

```markdown
## [Unreleased]

## [0.1.0] - 2026-01-15

### Added

- Initial project scaffold generated from [project-kit-cookiecutter](https://github.com/samuelduchesne/project-kit-cookiecutter).

[Unreleased]: https://github.com/<handle>/<project_name>/compare/0.1.0...HEAD
[0.1.0]: https://github.com/<handle>/<project_name>/releases/tag/0.1.0
```
