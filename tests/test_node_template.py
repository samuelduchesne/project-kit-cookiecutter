"""Tests for the Node (TypeScript) template in ``node/``."""

from __future__ import annotations

import json
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tests.utils import file_contains_text, is_valid_yaml, run_within_dir

ROOT = Path(__file__).resolve().parents[1]
NODE_TEMPLATE = ROOT / "node"

AGENT_FILES = ("AGENTS.md", "CLAUDE.md", ".cursorrules", ".github/copilot-instructions.md")
AGENT_CHOICES = {
    "suggested": {"AGENTS.md", ".github/copilot-instructions.md"},
    "codex": {"AGENTS.md"},
    "claude": {"CLAUDE.md"},
    "copilot": {".github/copilot-instructions.md"},
    "cursor": {".cursorrules"},
    "all": set(AGENT_FILES),
    "none": set(),
}
LICENSES = {
    "MIT license": ("MIT", "MIT License"),
    "BSD license": ("BSD-3-Clause", "BSD 3-Clause License"),
    "ISC license": ("ISC", "ISC License"),
    "Apache Software License 2.0": ("Apache-2.0", "Apache License"),
    "GNU General Public License v3": ("GPL-3.0-only", "GNU GENERAL PUBLIC LICENSE"),
}


def bake(cookies, **context):
    result = cookies.bake(template=str(NODE_TEMPLATE), extra_context=context)
    assert result.exception is None, result.exception
    assert result.exit_code == 0
    return result.project_path


def package_json(project: Path) -> dict:
    return json.loads((project / "package.json").read_text(encoding="utf-8"))


def generated_files(project: Path) -> list[Path]:
    return [path for path in project.rglob("*") if path.is_file()]


def test_bake_defaults(cookies, tmp_path):
    with run_within_dir(tmp_path):
        project = bake(cookies, project_name="my-lib")
        assert project.name == "my-lib"
        for name in (
            "package.json",
            "tsconfig.json",
            "tsconfig.build.json",
            "biome.json",
            "vitest.config.ts",
            "src/index.ts",
            "tests/index.test.ts",
            ".pre-commit-config.yaml",
            ".nvmrc",
            "Makefile",
            "README.md",
            "CONTRIBUTING.md",
            "CHANGELOG.md",
            "LICENSE",
            "codecov.yaml",
            ".github/workflows/main.yml",
            ".devcontainer/devcontainer.json",
        ):
            assert (project / name).is_file(), name
        assert not (project / ".github/workflows/release.yml").exists()
        assert not list(project.glob("LICENSE_*"))

        manifest = package_json(project)
        assert manifest["name"] == "my-lib"
        assert manifest["private"] is True
        assert manifest["type"] == "module"
        assert manifest["engines"] == {"node": ">=24"}
        assert manifest["packageManager"].startswith("pnpm@")
        assert manifest["license"] == "MIT"


def test_generated_files_are_valid(cookies, tmp_path):
    """Every YAML and JSON file parses, nothing is left unrendered, and every file ends with one newline."""
    with run_within_dir(tmp_path):
        project = bake(cookies, publish_to_npm=True, agent_instructions="all", agent_profile="full")
        for path in generated_files(project):
            text = path.read_text(encoding="utf-8")
            assert "cookiecutter." not in text and "{%" not in text, path
            assert text.endswith("\n") and not text.endswith("\n\n"), path
            if path.suffix in {".yml", ".yaml"}:
                assert is_valid_yaml(path), path
            if path.suffix == ".json":
                json.loads(text)


def test_pre_commit_runs_biome(cookies, tmp_path):
    with run_within_dir(tmp_path):
        project = bake(cookies)
        assert file_contains_text(project / ".pre-commit-config.yaml", "biome check")
        assert file_contains_text(project / ".pre-commit-config.yaml", "pre-commit/pre-commit-hooks")


@pytest.mark.parametrize("node_version", ["22", "24", "26"])
def test_node_version(cookies, tmp_path, node_version):
    with run_within_dir(tmp_path):
        project = bake(cookies, node_version=node_version)
        assert (project / ".nvmrc").read_text(encoding="utf-8") == f"{node_version}\n"
        manifest = package_json(project)
        assert manifest["engines"]["node"] == f">={node_version}"
        assert manifest["devDependencies"]["@types/node"].startswith(f"{node_version}.")
        assert file_contains_text(project / ".devcontainer/devcontainer.json", f"typescript-node:{node_version}")
        workflow = (project / ".github/workflows/main.yml").read_text(encoding="utf-8")
        newer = [v for v in ("22", "24", "26") if int(v) >= int(node_version)]
        assert "node-version: [" + ", ".join(f'"{v}"' for v in newer) + "]" in workflow


def test_publish_to_npm(cookies, tmp_path):
    with run_within_dir(tmp_path):
        project = bake(cookies, publish_to_npm=True)
        assert "private" not in package_json(project)
        release = project / ".github/workflows/release.yml"
        assert release.is_file()
        assert file_contains_text(release, "npm publish --provenance")
        assert file_contains_text(release, "id-token: write")
        assert file_contains_text(project / "README.md", "## Releasing")


def test_no_github_actions(cookies, tmp_path):
    with run_within_dir(tmp_path):
        project = bake(cookies, include_github_actions=False, publish_to_npm=True)
        assert not (project / ".github/workflows").exists()
        assert (project / ".github/copilot-instructions.md").is_file()
        assert not file_contains_text(project / "README.md", "actions/workflows/main.yml")


def test_no_github_folder_without_actions_or_copilot(cookies, tmp_path):
    with run_within_dir(tmp_path):
        project = bake(cookies, include_github_actions=False, agent_instructions="codex")
        assert not (project / ".github").exists()


def test_no_codecov(cookies, tmp_path):
    with run_within_dir(tmp_path):
        project = bake(cookies, codecov=False)
        assert not (project / "codecov.yaml").exists()
        assert not file_contains_text(project / ".github/workflows/main.yml", "codecov")
        assert not file_contains_text(project / "README.md", "codecov")
        assert not file_contains_text(project / "Makefile", "test:coverage")


def test_no_devcontainer(cookies, tmp_path):
    with run_within_dir(tmp_path):
        project = bake(cookies, devcontainer=False)
        assert not (project / ".devcontainer").exists()


@pytest.mark.parametrize("agent_profile", ["minimal", "full"])
def test_changelog(cookies, tmp_path, agent_profile):
    with run_within_dir(tmp_path):
        project = bake(cookies, agent_instructions="all", agent_profile=agent_profile)
        assert file_contains_text(project / "CHANGELOG.md", "## [Unreleased]")
        for name in (*AGENT_FILES, "CONTRIBUTING.md"):
            assert file_contains_text(project / name, "[Unreleased]"), name


@pytest.mark.parametrize("agent_profile", ["minimal", "full"])
def test_no_changelog(cookies, tmp_path, agent_profile):
    with run_within_dir(tmp_path):
        project = bake(cookies, changelog=False, agent_instructions="all", agent_profile=agent_profile)
        assert not (project / "CHANGELOG.md").exists()
        for name in (*AGENT_FILES, "CONTRIBUTING.md"):
            assert not file_contains_text(project / name, "CHANGELOG"), name


@pytest.mark.parametrize("choice", sorted(AGENT_CHOICES))
def test_agent_instructions(cookies, tmp_path, choice):
    with run_within_dir(tmp_path):
        project = bake(cookies, agent_instructions=choice)
        present = {name for name in AGENT_FILES if (project / name).exists()}
        assert present == AGENT_CHOICES[choice]
        copilot = ".github/copilot-instructions.md" in AGENT_CHOICES[choice]
        assert (project / ".github/workflows/copilot-setup-steps.yml").exists() == copilot
        if copilot:
            # Copilot is told to run `make check`, whose pre-commit hooks run with uvx.
            assert file_contains_text(project / ".github/workflows/copilot-setup-steps.yml", "setup-uv")


def test_agent_profile_full(cookies, tmp_path):
    with run_within_dir(tmp_path):
        minimal = bake(cookies, agent_instructions="all", agent_profile="minimal")
        assert not file_contains_text(minimal / "AGENTS.md", "## Project Structure")
        full = bake(cookies, agent_instructions="all", agent_profile="full")
        for name in AGENT_FILES:
            assert file_contains_text(full / name, ".js"), name
        assert file_contains_text(full / "AGENTS.md", "## Project Structure")


@pytest.mark.parametrize("license_choice", sorted(LICENSES))
def test_license(cookies, tmp_path, license_choice):
    spdx, heading = LICENSES[license_choice]
    with run_within_dir(tmp_path):
        project = bake(cookies, open_source_license=license_choice)
        assert file_contains_text(project / "LICENSE", heading)
        assert package_json(project)["license"] == spdx
        assert not list(project.glob("LICENSE_*"))


def test_not_open_source(cookies, tmp_path):
    with run_within_dir(tmp_path):
        project = bake(cookies, open_source_license="Not open source")
        assert not (project / "LICENSE").exists()
        assert not list(project.glob("LICENSE_*"))
        assert package_json(project)["license"] == "UNLICENSED"


@pytest.mark.parametrize("name", ["My-Lib", "my_lib", "my lib", "1lib", "lib-", "-lib"])
def test_invalid_project_name(cookies, tmp_path, name):
    with run_within_dir(tmp_path):
        result = cookies.bake(template=str(NODE_TEMPLATE), extra_context={"project_name": name})
        assert result.exit_code != 0
        # pytest-cookies bakes into tmp_path/cookies/bakeNN, so look anywhere under tmp_path.
        assert not [path for path in tmp_path.rglob("*") if path.name == name]


def test_single_letter_project_name(cookies, tmp_path):
    with run_within_dir(tmp_path):
        assert package_json(bake(cookies, project_name="x"))["name"] == "x"


def test_description_and_author_are_escaped_in_package_json(cookies, tmp_path):
    with run_within_dir(tmp_path):
        project = bake(cookies, project_description='A "fast" C:\\ parser', author='Ada "A." Lovelace')
        manifest = package_json(project)
        assert manifest["description"] == 'A "fast" C:\\ parser'
        assert manifest["author"].startswith('Ada "A." Lovelace <')


def test_publish_to_npm_without_github_actions(cookies, tmp_path):
    with run_within_dir(tmp_path):
        project = bake(cookies, include_github_actions=False, publish_to_npm=True)
        assert file_contains_text(project / "README.md", "## Releasing")
        assert not file_contains_text(project / "README.md", "release.yml")
        assert file_contains_text(project / "README.md", "pnpm publish")


@pytest.mark.parametrize("spelling", ["false", "no", "0"])
def test_string_false_override_renders_like_false(cookies, tmp_path, spelling):
    """``publish_to_npm=false`` as a string renders the templates like a JSON false, not as a truthy string.

    The node template is baked in this process, where ``local_extensions`` resolves to the repository root's copy,
    so this also checks that the extension uses the node template's own boolean options.
    """
    with run_within_dir(tmp_path):
        project = bake(cookies, publish_to_npm=spelling)
        assert package_json(project)["private"] is True
        assert not file_contains_text(project / "README.md", "## Releasing")
        assert not (project / ".github/workflows/release.yml").exists()


def test_boolean_string_overrides(tmp_path):
    """``key=false`` on the command line is a real false, as in the Python template."""
    subprocess.run(
        [
            sys.executable,
            "-m",
            "cookiecutter",
            "--no-input",
            str(NODE_TEMPLATE),
            "--output-dir",
            str(tmp_path),
            "changelog=false",
            "devcontainer=no",
        ],
        check=True,
        capture_output=True,
    )
    project = tmp_path / "example-project"
    assert not (project / "CHANGELOG.md").exists()
    assert not (project / ".devcontainer").exists()


def test_invalid_boolean(tmp_path):
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "cookiecutter",
            "--no-input",
            str(NODE_TEMPLATE),
            "--output-dir",
            str(tmp_path),
            "changelog=maybe",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode != 0
    assert "ERROR:" in proc.stdout + proc.stderr
    assert not (tmp_path / "example-project").exists()


def test_local_extensions_match_root():
    """Cookiecutter imports extensions from the template folder, so node/ keeps an identical copy."""
    assert (NODE_TEMPLATE / "local_extensions.py").read_bytes() == (ROOT / "local_extensions.py").read_bytes()


@pytest.mark.skipif(shutil.which("pnpm") is None or shutil.which("uvx") is None, reason="needs pnpm and uv")
def test_generated_project_passes_its_checks(cookies, tmp_path):
    """Install, check, test and build a generated project; nothing it generated needs fixing."""
    with run_within_dir(tmp_path):
        project = bake(cookies, publish_to_npm=True, agent_instructions="all")
        with run_within_dir(str(project)):
            subprocess.check_call(shlex.split("git init -q -b main"))
            subprocess.check_call(shlex.split("pnpm install"))
            # cruft and spec-kit write JSON in their own format, which the hooks must leave alone.
            (project / ".cruft.json").write_text('{\n  "a": [\n    1\n  ]\n}')
            (project / ".specify").mkdir()
            (project / ".specify/integration.json").write_text('{\n  "a": [\n    1\n  ]\n}')
            subprocess.check_call(shlex.split("git add -A"))
            for command in ("make check", "make test", "make build"):
                assert subprocess.check_call(shlex.split(command)) == 0, command
            assert (project / "dist/index.js").is_file()
            assert (project / "dist/index.d.ts").is_file()
            changed = subprocess.check_output(shlex.split("git diff --name-only"), text=True)
            assert changed == "", f"checks modified generated files:\n{changed}"
