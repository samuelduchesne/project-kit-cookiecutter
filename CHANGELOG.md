# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-11-02

First tagged release of the Python and Node (TypeScript) templates.

### Changed

- The generated README and the tutorial install dependencies before the first push, so the first CI run has a lock file.

### Fixed

- The generated pre-commit hooks and Biome no longer reformat `.cruft.json` and `.specify/`, which made `make check` fail on projects set up with cruft and spec-kit.

[Unreleased]: https://github.com/samuelduchesne/project-kit-cookiecutter/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/samuelduchesne/project-kit-cookiecutter/releases/tag/v1.0.0
