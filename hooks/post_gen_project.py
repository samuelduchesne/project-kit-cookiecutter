#!/usr/bin/env python
from __future__ import annotations

import os
import shutil
import sys

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

TRUE_STRINGS = frozenset({"1", "true", "t", "yes", "y", "on"})
FALSE_STRINGS = frozenset({"0", "false", "f", "no", "n", "off"})


def as_bool(value: str, name: str = "value") -> bool:
    """Convert a rendered cookiecutter boolean (``True``, ``false``, ``yes``, ``0``...) to a bool.

    Booleans are rendered into this script as strings, never as Python literals, because a command-line override
    such as ``dvc=false`` would otherwise render as ``false`` and raise a NameError.
    """
    lowered = value.strip().lower()
    if lowered in TRUE_STRINGS:
        return True
    if lowered in FALSE_STRINGS:
        return False
    print(
        f"ERROR: {value!r} is not a valid value for the boolean option {name}. "
        f"Use one of: {', '.join(sorted(TRUE_STRINGS | FALSE_STRINGS))}."
    )
    sys.exit(1)


def remove_file(filepath: str) -> None:
    """Remove a file, with error handling."""
    full_path = os.path.join(PROJECT_DIRECTORY, filepath)
    try:
        os.remove(full_path)
    except FileNotFoundError:
        print(f"Warning: File not found, skipping removal: {filepath}", file=sys.stderr)
    except OSError as e:
        print(f"Error removing file {filepath}: {e}", file=sys.stderr)
        raise


def remove_dir(filepath: str) -> None:
    """Remove a directory recursively, with error handling."""
    full_path = os.path.join(PROJECT_DIRECTORY, filepath)
    try:
        shutil.rmtree(full_path)
    except FileNotFoundError:
        print(f"Warning: Directory not found, skipping removal: {filepath}", file=sys.stderr)
    except OSError as e:
        print(f"Error removing directory {filepath}: {e}", file=sys.stderr)
        raise


def move_file(filepath: str, target: str) -> None:
    """Move/rename a file, with error handling."""
    src_path = os.path.join(PROJECT_DIRECTORY, filepath)
    dst_path = os.path.join(PROJECT_DIRECTORY, target)
    try:
        os.rename(src_path, dst_path)
    except FileNotFoundError:
        print(f"Warning: Source file not found, skipping move: {filepath}", file=sys.stderr)
    except OSError as e:
        print(f"Error moving file {filepath} to {target}: {e}", file=sys.stderr)
        raise


def move_dir(src: str, target: str) -> None:
    """Move a directory, with error handling."""
    src_path = os.path.join(PROJECT_DIRECTORY, src)
    dst_path = os.path.join(PROJECT_DIRECTORY, target)
    try:
        shutil.move(src_path, dst_path)
    except FileNotFoundError:
        print(f"Warning: Source directory not found, skipping move: {src}", file=sys.stderr)
    except OSError as e:
        print(f"Error moving directory {src} to {target}: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    changelog = as_bool("{{ cookiecutter.changelog }}", "changelog")
    codecov = as_bool("{{ cookiecutter.codecov }}", "codecov")
    devcontainer = as_bool("{{ cookiecutter.devcontainer }}", "devcontainer")
    dockerfile = as_bool("{{ cookiecutter.dockerfile }}", "dockerfile")
    dvc = as_bool("{{ cookiecutter.dvc }}", "dvc")
    include_github_actions = as_bool("{{ cookiecutter.include_github_actions }}", "include_github_actions")
    include_py_typed = as_bool("{{ cookiecutter.include_py_typed }}", "include_py_typed")
    mkdocs = as_bool("{{ cookiecutter.mkdocs }}", "mkdocs")
    publish_to_pypi = as_bool("{{ cookiecutter.publish_to_pypi }}", "publish_to_pypi")

    if not include_github_actions:
        remove_dir(".github")
    else:
        if not mkdocs and not publish_to_pypi:
            remove_file(".github/workflows/on-release-main.yml")

    # Handle agent instructions based on selected option
    agent_instructions = "{{cookiecutter.agent_instructions}}"

    # Define which files each agent needs
    # suggested = copilot + codex
    if agent_instructions == "suggested":
        remove_file("CLAUDE.md")
        remove_file(".cursorrules")
    elif agent_instructions == "codex":
        remove_file("CLAUDE.md")
        remove_file(".cursorrules")
        remove_file(".github/copilot-instructions.md")
        remove_file(".github/workflows/copilot-setup-steps.yml")
    elif agent_instructions == "claude":
        remove_file("AGENTS.md")
        remove_file(".cursorrules")
        remove_file(".github/copilot-instructions.md")
        remove_file(".github/workflows/copilot-setup-steps.yml")
    elif agent_instructions == "copilot":
        remove_file("AGENTS.md")
        remove_file("CLAUDE.md")
        remove_file(".cursorrules")
    elif agent_instructions == "cursor":
        remove_file("AGENTS.md")
        remove_file("CLAUDE.md")
        remove_file(".github/copilot-instructions.md")
        remove_file(".github/workflows/copilot-setup-steps.yml")
    elif agent_instructions == "none":
        remove_file("AGENTS.md")
        remove_file("CLAUDE.md")
        remove_file(".cursorrules")
        remove_file(".github/copilot-instructions.md")
        remove_file(".github/workflows/copilot-setup-steps.yml")
    # "all" keeps everything, no removals needed

    if not include_py_typed:
        remove_file("{{cookiecutter.project_slug}}/py.typed")

    if not mkdocs:
        remove_dir("docs")
        remove_file("mkdocs.yml")

    if not changelog:
        remove_file("CHANGELOG.md")
        if mkdocs:
            remove_file("docs/changelog.md")

    if not dockerfile:
        remove_file("Dockerfile")

    if not codecov:
        remove_file("codecov.yaml")
        if include_github_actions:
            remove_file(".github/workflows/validate-codecov-config.yml")

    if not devcontainer:
        remove_dir(".devcontainer")

    if not dvc:
        remove_dir(".dvc")
        remove_file(".dvcignore")
        remove_file("dvc.yaml")
        remove_file("params.yaml")
        remove_dir("data")
        remove_dir("{{cookiecutter.project_slug}}/schemas")
        remove_file("{{cookiecutter.project_slug}}/prepare.py")
        remove_file("{{cookiecutter.project_slug}}/train.py")
        remove_file("{{cookiecutter.project_slug}}/evaluate.py")

    if "{{cookiecutter.open_source_license}}" == "MIT license":
        move_file("LICENSE_MIT", "LICENSE")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_APACHE")
        remove_file("LICENSE_GPL")

    if "{{cookiecutter.open_source_license}}" == "BSD license":
        move_file("LICENSE_BSD", "LICENSE")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_APACHE")
        remove_file("LICENSE_GPL")

    if "{{cookiecutter.open_source_license}}" == "ISC license":
        move_file("LICENSE_ISC", "LICENSE")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_APACHE")
        remove_file("LICENSE_GPL")

    if "{{cookiecutter.open_source_license}}" == "Apache Software License 2.0":
        move_file("LICENSE_APACHE", "LICENSE")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_GPL")

    if "{{cookiecutter.open_source_license}}" == "GNU General Public License v3":
        move_file("LICENSE_GPL", "LICENSE")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_APACHE")

    if "{{cookiecutter.open_source_license}}" == "Not open source":
        remove_file("LICENSE_GPL")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_APACHE")

    if "{{cookiecutter.layout}}" == "src":
        if os.path.isdir("src"):
            remove_dir("src")
        move_dir("{{cookiecutter.project_slug}}", os.path.join("src", "{{cookiecutter.project_slug}}"))
