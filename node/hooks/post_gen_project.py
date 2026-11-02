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


if __name__ == "__main__":
    changelog = as_bool("{{ cookiecutter.changelog }}", "changelog")
    codecov = as_bool("{{ cookiecutter.codecov }}", "codecov")
    devcontainer = as_bool("{{ cookiecutter.devcontainer }}", "devcontainer")
    include_github_actions = as_bool("{{ cookiecutter.include_github_actions }}", "include_github_actions")
    publish_to_npm = as_bool("{{ cookiecutter.publish_to_npm }}", "publish_to_npm")

    if not include_github_actions:
        remove_dir(".github/workflows")
    elif not publish_to_npm:
        remove_file(".github/workflows/release.yml")

    # Files each agent choice removes; "all" keeps everything. Same choices as the Python template.
    copilot_files = [".github/copilot-instructions.md"]
    if include_github_actions:
        copilot_files.append(".github/workflows/copilot-setup-steps.yml")
    removals = {
        "suggested": ["CLAUDE.md", ".cursorrules"],
        "codex": ["CLAUDE.md", ".cursorrules", *copilot_files],
        "claude": ["AGENTS.md", ".cursorrules", *copilot_files],
        "copilot": ["AGENTS.md", "CLAUDE.md", ".cursorrules"],
        "cursor": ["AGENTS.md", "CLAUDE.md", *copilot_files],
        "none": ["AGENTS.md", "CLAUDE.md", ".cursorrules", *copilot_files],
        "all": [],
    }
    for path in removals["{{ cookiecutter.agent_instructions }}"]:
        remove_file(path)

    # .github holds only workflows and Copilot instructions; drop it when both are gone.
    github_dir = os.path.join(PROJECT_DIRECTORY, ".github")
    if os.path.isdir(github_dir) and not os.listdir(github_dir):
        os.rmdir(github_dir)

    if not changelog:
        remove_file("CHANGELOG.md")

    if not codecov:
        remove_file("codecov.yaml")

    if not devcontainer:
        remove_dir(".devcontainer")

    licenses = {
        "MIT license": "LICENSE_MIT",
        "BSD license": "LICENSE_BSD",
        "ISC license": "LICENSE_ISC",
        "Apache Software License 2.0": "LICENSE_APACHE",
        "GNU General Public License v3": "LICENSE_GPL",
    }
    chosen = licenses.get("{{ cookiecutter.open_source_license }}")
    for license_file in licenses.values():
        if license_file == chosen:
            move_file(license_file, "LICENSE")
        else:
            remove_file(license_file)
