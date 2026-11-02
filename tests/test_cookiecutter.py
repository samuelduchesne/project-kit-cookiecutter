from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path

import pytest

from tests.utils import file_contains_text, is_valid_yaml, run_within_dir


def test_bake_project(cookies):
    result = cookies.bake(extra_context={"project_name": "my-project"})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "my-project"
    assert result.project_path.is_dir()


def test_using_pytest(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()

        # Assert that project was created.
        assert result.exit_code == 0
        assert result.exception is None
        assert result.project_path.name == "example-project"
        assert result.project_path.is_dir()
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")

        # Install the uv environment and run the tests.
        with run_within_dir(str(result.project_path)):
            assert subprocess.check_call(shlex.split("uv sync")) == 0
            assert subprocess.check_call(shlex.split("uv run make test")) == 0


def test_src_layout_using_pytest(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"layout": "src"})

        # Assert that project was created.
        assert result.exit_code == 0
        assert result.exception is None
        assert result.project_path.name == "example-project"
        assert result.project_path.is_dir()
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")

        # Install the uv environment and run the tests.
        with run_within_dir(str(result.project_path)):
            assert subprocess.check_call(shlex.split("uv sync")) == 0
            assert subprocess.check_call(shlex.split("uv run make test")) == 0


def test_devcontainer(cookies, tmp_path):
    """Test that the devcontainer files are created when devcontainer=y"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"devcontainer": True})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/.devcontainer/devcontainer.json")
        assert os.path.isfile(f"{result.project_path}/.devcontainer/postCreateCommand.sh")


def test_not_devcontainer(cookies, tmp_path):
    """Test that the devcontainer files are not created when devcontainer=n"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"devcontainer": False})
        assert result.exit_code == 0
        assert not os.path.isfile(f"{result.project_path}/.devcontainer/devcontainer.json")
        assert not os.path.isfile(f"{result.project_path}/.devcontainer/postCreateCommand.sh")


def test_cicd_contains_pypi_secrets(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"publish_to_pypi": True})
        assert result.exit_code == 0
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "on-release-main.yml")
        assert file_contains_text(f"{result.project_path}/.github/workflows/on-release-main.yml", "UV_PUBLISH_TOKEN")
        assert file_contains_text(f"{result.project_path}/Makefile", "build-and-publish")


def test_dont_publish(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"publish_to_pypi": False})
        assert result.exit_code == 0
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "on-release-main.yml")
        assert not file_contains_text(
            f"{result.project_path}/.github/workflows/on-release-main.yml", "make build-and-publish"
        )


def test_mkdocs(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"mkdocs": True})
        assert result.exit_code == 0
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "on-release-main.yml")
        assert file_contains_text(f"{result.project_path}/.github/workflows/on-release-main.yml", "mkdocs gh-deploy")
        assert file_contains_text(f"{result.project_path}/Makefile", "docs:")
        assert os.path.isdir(f"{result.project_path}/docs")


def test_not_mkdocs(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"mkdocs": False, "publish_to_pypi": True})
        assert result.exit_code == 0
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "on-release-main.yml")
        assert not file_contains_text(
            f"{result.project_path}/.github/workflows/on-release-main.yml", "mkdocs gh-deploy"
        )
        assert not file_contains_text(f"{result.project_path}/Makefile", "docs:")
        assert not os.path.isdir(f"{result.project_path}/docs")


def test_tox(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/tox.ini")
        assert file_contains_text(f"{result.project_path}/tox.ini", "[tox]")


def test_dockerfile(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"dockerfile": True})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/Dockerfile")


def test_not_dockerfile(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"dockerfile": False})
        assert result.exit_code == 0
        assert not os.path.isfile(f"{result.project_path}/Dockerfile")


def test_codecov(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake()
        assert result.exit_code == 0
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")
        assert os.path.isfile(f"{result.project_path}/codecov.yaml")
        assert os.path.isfile(f"{result.project_path}/.github/workflows/validate-codecov-config.yml")


def test_not_codecov(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"codecov": False})
        assert result.exit_code == 0
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")
        assert not os.path.isfile(f"{result.project_path}/codecov.yaml")
        assert not os.path.isfile(f"{result.project_path}/.github/workflows/validate-codecov-config.yml")


def test_remove_release_workflow(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"publish_to_pypi": False, "mkdocs": True})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/.github/workflows/on-release-main.yml")

        result = cookies.bake(extra_context={"publish_to_pypi": False, "mkdocs": False})
        assert result.exit_code == 0
        assert not os.path.isfile(f"{result.project_path}/.github/workflows/on-release-main.yml")


def test_license_mit(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"open_source_license": "MIT license"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/LICENSE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_BSD")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_ISC")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_APACHE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_GPL")
        with open(f"{result.project_path}/LICENSE", encoding="utf8") as licfile:
            content = licfile.readlines()
            assert len(content) == 21


def test_license_bsd(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"open_source_license": "BSD license"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/LICENSE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_MIT")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_ISC")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_APACHE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_GPL")
        with open(f"{result.project_path}/LICENSE", encoding="utf8") as licfile:
            content = licfile.readlines()
            assert len(content) == 28


def test_license_isc(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"open_source_license": "ISC license"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/LICENSE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_MIT")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_BSD")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_APACHE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_GPL")
        with open(f"{result.project_path}/LICENSE", encoding="utf8") as licfile:
            content = licfile.readlines()
            assert len(content) == 7


def test_license_apache(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"open_source_license": "Apache Software License 2.0"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/LICENSE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_MIT")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_BSD")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_ISC")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_GPL")
        with open(f"{result.project_path}/LICENSE", encoding="utf8") as licfile:
            content = licfile.readlines()
            assert len(content) == 202


def test_license_gplv3(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"open_source_license": "GNU General Public License v3"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/LICENSE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_MIT")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_BSD")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_ISC")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_APACHE")
        with open(f"{result.project_path}/LICENSE", encoding="utf8") as licfile:
            content = licfile.readlines()
            assert len(content) == 674


def test_license_no_license(cookies, tmp_path):
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"open_source_license": "Not open source"})
        assert result.exit_code == 0
        assert not os.path.isfile(f"{result.project_path}/LICENSE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_MIT")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_BSD")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_ISC")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_APACHE")
        assert not os.path.isfile(f"{result.project_path}/LICENSE_GPL")


def test_agent_instructions_suggested(cookies, tmp_path):
    """Test that suggested option creates AGENTS.md and copilot files"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"agent_instructions": "suggested"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/AGENTS.md")
        assert os.path.isfile(f"{result.project_path}/.github/copilot-instructions.md")
        assert not os.path.isfile(f"{result.project_path}/CLAUDE.md")
        assert not os.path.isfile(f"{result.project_path}/.cursorrules")


def test_agent_instructions_codex(cookies, tmp_path):
    """Test that codex option creates only AGENTS.md"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"agent_instructions": "codex"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/AGENTS.md")
        assert not os.path.isfile(f"{result.project_path}/CLAUDE.md")
        assert not os.path.isfile(f"{result.project_path}/.github/copilot-instructions.md")
        assert not os.path.isfile(f"{result.project_path}/.cursorrules")


def test_agent_instructions_claude(cookies, tmp_path):
    """Test that claude option creates only CLAUDE.md"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"agent_instructions": "claude"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/CLAUDE.md")
        assert not os.path.isfile(f"{result.project_path}/AGENTS.md")
        assert not os.path.isfile(f"{result.project_path}/.github/copilot-instructions.md")
        assert not os.path.isfile(f"{result.project_path}/.cursorrules")


def test_agent_instructions_copilot(cookies, tmp_path):
    """Test that copilot option creates only copilot files"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"agent_instructions": "copilot"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/.github/copilot-instructions.md")
        assert not os.path.isfile(f"{result.project_path}/AGENTS.md")
        assert not os.path.isfile(f"{result.project_path}/CLAUDE.md")
        assert not os.path.isfile(f"{result.project_path}/.cursorrules")


def test_agent_instructions_cursor(cookies, tmp_path):
    """Test that cursor option creates only .cursorrules"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"agent_instructions": "cursor"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/.cursorrules")
        assert not os.path.isfile(f"{result.project_path}/AGENTS.md")
        assert not os.path.isfile(f"{result.project_path}/CLAUDE.md")
        assert not os.path.isfile(f"{result.project_path}/.github/copilot-instructions.md")


def test_agent_instructions_all(cookies, tmp_path):
    """Test that all option creates all agent files"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"agent_instructions": "all"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/AGENTS.md")
        assert os.path.isfile(f"{result.project_path}/CLAUDE.md")
        assert os.path.isfile(f"{result.project_path}/.github/copilot-instructions.md")
        assert os.path.isfile(f"{result.project_path}/.cursorrules")


def test_agent_instructions_none(cookies, tmp_path):
    """Test that none option creates no agent files"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"agent_instructions": "none"})
        assert result.exit_code == 0
        assert not os.path.isfile(f"{result.project_path}/AGENTS.md")
        assert not os.path.isfile(f"{result.project_path}/CLAUDE.md")
        assert not os.path.isfile(f"{result.project_path}/.github/copilot-instructions.md")
        assert not os.path.isfile(f"{result.project_path}/.cursorrules")


def test_py_typed(cookies, tmp_path):
    """Test that py.typed is created when include_py_typed=True"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"include_py_typed": True})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/example_project/py.typed")


def test_py_typed_src_layout(cookies, tmp_path):
    """Test that py.typed is in correct location for src layout"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"include_py_typed": True, "layout": "src"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/src/example_project/py.typed")


def test_not_py_typed(cookies, tmp_path):
    """Test that py.typed is not created when include_py_typed=False"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"include_py_typed": False})
        assert result.exit_code == 0
        assert not os.path.isfile(f"{result.project_path}/example_project/py.typed")


def test_not_py_typed_src_layout(cookies, tmp_path):
    """Test that py.typed is not created when include_py_typed=False with src layout"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"include_py_typed": False, "layout": "src"})
        assert result.exit_code == 0
        assert not os.path.isfile(f"{result.project_path}/src/example_project/py.typed")


def test_deptry(cookies, tmp_path):
    """Test that deptry is included in Makefile when deptry=True"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"deptry": True})
        assert result.exit_code == 0
        assert file_contains_text(f"{result.project_path}/Makefile", "deptry")


def test_not_deptry(cookies, tmp_path):
    """Test that deptry is not included in Makefile when deptry=False"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"deptry": False})
        assert result.exit_code == 0
        assert not file_contains_text(f"{result.project_path}/Makefile", "deptry")


def test_agent_profile_minimal(cookies, tmp_path):
    """Test that minimal agent profile creates shorter AGENTS.md"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"agent_instructions": "codex", "agent_profile": "minimal"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/AGENTS.md")
        # Minimal profile should not include detailed sections
        assert not file_contains_text(f"{result.project_path}/AGENTS.md", "Common Tasks for AI Agents")


def test_agent_profile_full(cookies, tmp_path):
    """Test that full agent profile creates comprehensive AGENTS.md"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"agent_instructions": "codex", "agent_profile": "full"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/AGENTS.md")
        # Full profile should include detailed sections
        assert file_contains_text(f"{result.project_path}/AGENTS.md", "Common Tasks for AI Agents")
        assert file_contains_text(f"{result.project_path}/AGENTS.md", "Testing Guidelines")


AGENT_FILES = ("AGENTS.md", "CLAUDE.md", ".github/copilot-instructions.md", ".cursorrules")
CHANGELOG_RULE = "Add an entry under `## [Unreleased]` in `CHANGELOG.md`"


def test_changelog(cookies, tmp_path):
    """Test that the default bake includes a Keep a Changelog CHANGELOG.md"""
    with run_within_dir(tmp_path):
        result = cookies.bake()
        assert result.exit_code == 0
        changelog = result.project_path / "CHANGELOG.md"
        assert changelog.is_file()
        content = changelog.read_text()
        assert "## [Unreleased]" in content
        assert "### Added" in content
        assert "https://keepachangelog.com/en/1.1.0/" in content
        assert "[Unreleased]: https://github.com/" in content
        assert "/example-project/commits/main" in content
        assert "{{" not in content
        assert "{%" not in content
        assert content.endswith("\n")
        assert not content.endswith("\n\n")
        assert file_contains_text(f"{result.project_path}/CONTRIBUTING.md", "Update CHANGELOG.md under [Unreleased]")


def test_changelog_in_mkdocs_nav(cookies, tmp_path):
    """Test that the changelog is included in the docs nav when mkdocs=True"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"changelog": True, "mkdocs": True})
        assert result.exit_code == 0
        assert is_valid_yaml(result.project_path / "mkdocs.yml")
        assert file_contains_text(f"{result.project_path}/mkdocs.yml", "Changelog: changelog.md")
        assert file_contains_text(f"{result.project_path}/mkdocs.yml", "pymdownx.snippets")
        assert file_contains_text(f"{result.project_path}/docs/changelog.md", "CHANGELOG.md")


@pytest.mark.parametrize("agent_profile", ["minimal", "full"])
def test_not_changelog(cookies, tmp_path, agent_profile):
    """Test that changelog=False removes CHANGELOG.md and every changelog rule"""
    with run_within_dir(tmp_path):
        result = cookies.bake(
            extra_context={"changelog": False, "agent_instructions": "all", "agent_profile": agent_profile}
        )
        assert result.exit_code == 0
        assert not os.path.isfile(f"{result.project_path}/CHANGELOG.md")
        assert not os.path.isfile(f"{result.project_path}/docs/changelog.md")
        assert not file_contains_text(f"{result.project_path}/mkdocs.yml", "changelog")
        assert not file_contains_text(f"{result.project_path}/mkdocs.yml", "CHANGELOG")
        assert not file_contains_text(f"{result.project_path}/mkdocs.yml", "pymdownx.snippets")
        assert not file_contains_text(f"{result.project_path}/CONTRIBUTING.md", "CHANGELOG")
        for agent_file in AGENT_FILES:
            assert os.path.isfile(f"{result.project_path}/{agent_file}")
            assert not file_contains_text(f"{result.project_path}/{agent_file}", "CHANGELOG"), agent_file


@pytest.mark.parametrize("agent_profile", ["minimal", "full"])
def test_changelog_agent_instructions_all(cookies, tmp_path, agent_profile):
    """Test that changelog=True with agent_instructions=all adds the rule to every agent file"""
    with run_within_dir(tmp_path):
        result = cookies.bake(
            extra_context={"changelog": True, "agent_instructions": "all", "agent_profile": agent_profile}
        )
        assert result.exit_code == 0
        for agent_file in AGENT_FILES:
            assert file_contains_text(f"{result.project_path}/{agent_file}", CHANGELOG_RULE), agent_file
            assert file_contains_text(
                f"{result.project_path}/{agent_file}", "Added, Changed, Deprecated, Removed, Fixed, Security"
            ), agent_file


def test_type_checker_mypy(cookies, tmp_path):
    """Test that mypy is configured when type_checker=mypy"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"type_checker": "mypy"})
        assert result.exit_code == 0
        assert file_contains_text(f"{result.project_path}/Makefile", "mypy")
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "[tool.mypy]")


def test_type_checker_ty(cookies, tmp_path):
    """Test that ty is configured when type_checker=ty"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"type_checker": "ty"})
        assert result.exit_code == 0
        assert file_contains_text(f"{result.project_path}/Makefile", "ty check")
        assert not file_contains_text(f"{result.project_path}/pyproject.toml", "[tool.mypy]")


def test_type_checker_ty_is_pinned(cookies, tmp_path):
    """Test that pre-1.0 ty is pinned and fails on warnings"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"type_checker": "ty"})
        assert result.exit_code == 0
        assert file_contains_text(f"{result.project_path}/pyproject.toml", '"ty==')
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "error-on-warning = true")


def test_type_checker_pyrefly(cookies, tmp_path):
    """Test that pyrefly is configured with the strict preset when type_checker=pyrefly"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"type_checker": "pyrefly"})
        assert result.exit_code == 0
        assert file_contains_text(f"{result.project_path}/Makefile", "pyrefly check")
        assert file_contains_text(f"{result.project_path}/tox.ini", "pyrefly check")
        assert file_contains_text(f"{result.project_path}/.github/workflows/main.yml", "uv run pyrefly check")
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "[tool.pyrefly]")
        assert file_contains_text(f"{result.project_path}/pyproject.toml", 'preset = "strict"')
        assert file_contains_text(f"{result.project_path}/pyproject.toml", '"pyrefly>=')
        assert not file_contains_text(f"{result.project_path}/pyproject.toml", "[tool.mypy]")


def test_type_checker_pyrefly_src_layout(cookies, tmp_path):
    """Test that pyrefly includes the src directory in src layout"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"type_checker": "pyrefly", "layout": "src"})
        assert result.exit_code == 0
        assert file_contains_text(f"{result.project_path}/pyproject.toml", 'project-includes = ["src", "tests"]')


def test_pytest_strict_mode(cookies, tmp_path):
    """Test that pytest 9's strict mode is used when the minimum Python allows pytest 9"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"minimum_python_version": "3.10"})
        assert result.exit_code == 0
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "strict = true")
        assert file_contains_text(f"{result.project_path}/pyproject.toml", '"pytest>=9.0.0"')


def test_pytest_strict_mode_python_39(cookies, tmp_path):
    """Test that Python 3.9 projects get pytest 8 compatible strict options"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"minimum_python_version": "3.9"})
        assert result.exit_code == 0
        assert file_contains_text(f"{result.project_path}/pyproject.toml", '"--strict-markers", "--strict-config"')
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "xfail_strict = true")
        assert not file_contains_text(f"{result.project_path}/pyproject.toml", "\nstrict = true")
        assert file_contains_text(f"{result.project_path}/pyproject.toml", '"pytest>=8.0.0"')


def test_ruff_rules(cookies, tmp_path):
    """Test that the expanded Ruff rule set and future-annotations are configured"""
    with run_within_dir(tmp_path):
        result = cookies.bake()
        assert result.exit_code == 0
        for rule in ("DTZ", "LOG", "PIE", "PT", "RET", "TC", "PTH", "PERF", "FURB"):
            assert file_contains_text(f"{result.project_path}/pyproject.toml", f'"{rule}",')
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "future-annotations = true")


def test_type_checker_pyright(cookies, tmp_path):
    """Test that pyright is configured when type_checker=pyright"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"type_checker": "pyright"})
        assert result.exit_code == 0
        assert file_contains_text(f"{result.project_path}/Makefile", "pyright")
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "[tool.pyright]")
        assert not file_contains_text(f"{result.project_path}/pyproject.toml", "[tool.mypy]")


def test_dvc(cookies, tmp_path):
    """Test that DVC files are created when dvc=True"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"dvc": True})
        assert result.exit_code == 0

        # Check DVC configuration files
        assert os.path.isdir(f"{result.project_path}/.dvc")
        assert os.path.isfile(f"{result.project_path}/.dvc/.gitignore")
        assert os.path.isfile(f"{result.project_path}/.dvc/config")
        assert os.path.isfile(f"{result.project_path}/.dvcignore")

        # Check pipeline files
        assert os.path.isfile(f"{result.project_path}/dvc.yaml")
        assert os.path.isfile(f"{result.project_path}/params.yaml")
        assert is_valid_yaml(result.project_path / "dvc.yaml")
        assert is_valid_yaml(result.project_path / "params.yaml")

        # Check data directories
        assert os.path.isdir(f"{result.project_path}/data/raw")
        assert os.path.isdir(f"{result.project_path}/data/processed")

        # Check pipeline scripts
        assert os.path.isfile(f"{result.project_path}/example_project/prepare.py")
        assert os.path.isfile(f"{result.project_path}/example_project/train.py")
        assert os.path.isfile(f"{result.project_path}/example_project/evaluate.py")

        # Check schemas directory (inside the package)
        assert os.path.isdir(f"{result.project_path}/example_project/schemas")
        assert os.path.isfile(f"{result.project_path}/example_project/schemas/__init__.py")
        assert os.path.isfile(f"{result.project_path}/example_project/schemas/params.py")
        assert os.path.isfile(f"{result.project_path}/example_project/schemas/params.schema.json")

        # Check Makefile has DVC targets
        assert file_contains_text(f"{result.project_path}/Makefile", "dvc-repro")
        assert file_contains_text(f"{result.project_path}/Makefile", "dvc-push")
        assert file_contains_text(f"{result.project_path}/Makefile", "dvc-pull")

        # Check pyproject.toml has DVC dependency
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "dvc>=")


def _pyproject_sections(project_path) -> tuple[str, str]:
    """Split a generated pyproject.toml into its [project] table and its [dependency-groups] table."""
    text = (project_path / "pyproject.toml").read_text()
    project = text.split("[project]", 1)[1].split("\n[", 1)[0]
    dependency_groups = text.split("[dependency-groups]", 1)[1].split("\n[", 1)[0]
    return project, dependency_groups


def test_dvc_runtime_dependencies(cookies, tmp_path):
    """Test that the DVC pipeline's runtime imports are project dependencies, not dev-only"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"dvc": True})
        assert result.exit_code == 0

        project, dependency_groups = _pyproject_sections(result.project_path)
        assert '"pydantic>=' in project
        assert '"pyyaml>=' in project
        assert '"pydantic>=' not in dependency_groups
        assert '"pyyaml>=' not in dependency_groups
        assert '"dvc>=' in dependency_groups
        assert "types-PyYAML" not in dependency_groups


def test_dvc_mypy_yaml_stubs(cookies, tmp_path):
    """Test that PyYAML stubs are added for mypy when DVC is enabled"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"dvc": True, "type_checker": "mypy"})
        assert result.exit_code == 0

        _, dependency_groups = _pyproject_sections(result.project_path)
        assert '"types-PyYAML>=' in dependency_groups


def test_not_dvc_no_project_dependencies(cookies, tmp_path):
    """Test that no runtime dependencies are declared when DVC is disabled"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"dvc": False, "type_checker": "mypy"})
        assert result.exit_code == 0

        project, dependency_groups = _pyproject_sections(result.project_path)
        assert "dependencies" not in project
        assert "pydantic" not in dependency_groups
        assert "types-PyYAML" not in dependency_groups


def test_not_dvc(cookies, tmp_path):
    """Test that DVC files are not created when dvc=False"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"dvc": False})
        assert result.exit_code == 0

        # Check DVC files don't exist
        assert not os.path.isdir(f"{result.project_path}/.dvc")
        assert not os.path.isfile(f"{result.project_path}/.dvcignore")
        assert not os.path.isfile(f"{result.project_path}/dvc.yaml")
        assert not os.path.isfile(f"{result.project_path}/params.yaml")
        assert not os.path.isdir(f"{result.project_path}/data")
        assert not os.path.isdir(f"{result.project_path}/example_project/schemas")

        # Check Makefile doesn't have DVC targets
        assert not file_contains_text(f"{result.project_path}/Makefile", "dvc-repro")


def test_dvc_src_layout(cookies, tmp_path):
    """Test that DVC works correctly with src layout"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"dvc": True, "layout": "src"})
        assert result.exit_code == 0

        # Check pipeline scripts are in correct location
        assert os.path.isfile(f"{result.project_path}/src/example_project/prepare.py")
        assert os.path.isfile(f"{result.project_path}/src/example_project/train.py")
        assert os.path.isfile(f"{result.project_path}/src/example_project/evaluate.py")

        # Check dvc.yaml references src layout
        assert file_contains_text(f"{result.project_path}/dvc.yaml", "src/")


def test_dvc_with_github_actions(cookies, tmp_path):
    """Test that DVC CI job is added when both are enabled"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"dvc": True, "include_github_actions": True})
        assert result.exit_code == 0

        # Check GitHub Actions workflow includes DVC job
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")
        assert file_contains_text(f"{result.project_path}/.github/workflows/main.yml", "dvc-pipeline")


def test_minimum_python_version_default(cookies, tmp_path):
    """Test that default minimum Python version (3.9) generates correct configuration"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"minimum_python_version": "3.9"})
        assert result.exit_code == 0

        # Check pyproject.toml
        assert file_contains_text(f"{result.project_path}/pyproject.toml", 'requires-python = ">=3.9,<4.0"')
        assert file_contains_text(f"{result.project_path}/pyproject.toml", 'target-version = "py39"')
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.9")
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.13")
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.14")

        # Check tox.ini
        assert file_contains_text(f"{result.project_path}/tox.ini", "envlist = py39, py310, py311, py312, py313, py314")

        # Check GitHub Actions workflow
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")
        assert file_contains_text(
            f"{result.project_path}/.github/workflows/main.yml", '["3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]'
        )
        # Coverage is uploaded from the newest Python version in the matrix
        assert file_contains_text(
            f"{result.project_path}/.github/workflows/main.yml", "matrix.python-version == '3.14'"
        )


def test_minimum_python_version_311(cookies, tmp_path):
    """Test that minimum Python 3.11 excludes older versions"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"minimum_python_version": "3.11"})
        assert result.exit_code == 0

        # Check pyproject.toml
        assert file_contains_text(f"{result.project_path}/pyproject.toml", 'requires-python = ">=3.11,<4.0"')
        assert file_contains_text(f"{result.project_path}/pyproject.toml", 'target-version = "py311"')
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.11")
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.12")
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.13")
        assert not file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.9")
        assert not file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.10")

        # Check tox.ini
        assert file_contains_text(f"{result.project_path}/tox.ini", "py311")
        assert file_contains_text(f"{result.project_path}/tox.ini", "py313")
        assert not file_contains_text(f"{result.project_path}/tox.ini", "py39")
        assert not file_contains_text(f"{result.project_path}/tox.ini", "py310")

        # Check GitHub Actions workflow
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")
        assert file_contains_text(f"{result.project_path}/.github/workflows/main.yml", '"3.11"')
        assert not file_contains_text(f"{result.project_path}/.github/workflows/main.yml", '"3.9"')
        assert not file_contains_text(f"{result.project_path}/.github/workflows/main.yml", '"3.10"')


def test_minimum_python_version_313(cookies, tmp_path):
    """Test that minimum Python 3.13 only includes 3.13"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"minimum_python_version": "3.13"})
        assert result.exit_code == 0

        # Check pyproject.toml
        assert file_contains_text(f"{result.project_path}/pyproject.toml", 'requires-python = ">=3.13,<4.0"')
        assert file_contains_text(f"{result.project_path}/pyproject.toml", 'target-version = "py313"')
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.13")
        assert not file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.9")
        assert not file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.12,")

        # Check tox.ini only has py313 and py314
        assert file_contains_text(f"{result.project_path}/tox.ini", "envlist = py313, py314")

        # Check GitHub Actions workflow only has 3.13 and 3.14
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")
        assert file_contains_text(f"{result.project_path}/.github/workflows/main.yml", '["3.13", "3.14"]')

        # Dockerfile uses the default development Python version
        assert file_contains_text(f"{result.project_path}/Dockerfile", "python:3.14-slim")


def test_minimum_python_version_314(cookies, tmp_path):
    """Test that minimum Python 3.14 only includes 3.14"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"minimum_python_version": "3.14"})
        assert result.exit_code == 0

        # Check pyproject.toml
        assert file_contains_text(f"{result.project_path}/pyproject.toml", 'requires-python = ">=3.14,<4.0"')
        assert file_contains_text(f"{result.project_path}/pyproject.toml", 'target-version = "py314"')
        assert file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.14")
        assert not file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.13")
        assert not file_contains_text(f"{result.project_path}/pyproject.toml", "Python :: 3.9")

        # Check tox.ini only has py314
        assert file_contains_text(f"{result.project_path}/tox.ini", "envlist = py314\n")
        assert file_contains_text(f"{result.project_path}/tox.ini", "3.14: py314")

        # Check GitHub Actions workflow only has 3.14 and still uploads coverage
        assert is_valid_yaml(result.project_path / ".github" / "workflows" / "main.yml")
        assert file_contains_text(f"{result.project_path}/.github/workflows/main.yml", '["3.14"]')
        assert file_contains_text(
            f"{result.project_path}/.github/workflows/main.yml", "matrix.python-version == '3.14'"
        )

        # Check Dockerfile and devcontainer use Python 3.14
        assert file_contains_text(f"{result.project_path}/Dockerfile", "python:3.14-slim")
        assert file_contains_text(
            f"{result.project_path}/.devcontainer/devcontainer.json", "mcr.microsoft.com/devcontainers/python:3.14"
        )


def test_minimum_python_version_type_checker_pyright(cookies, tmp_path):
    """Test that pyright pythonVersion is set correctly"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"minimum_python_version": "3.11", "type_checker": "pyright"})
        assert result.exit_code == 0
        assert file_contains_text(f"{result.project_path}/pyproject.toml", 'pythonVersion = "3.11"')


def test_minimum_python_version_type_checker_ty(cookies, tmp_path):
    """Test that ty python-version is set correctly"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"minimum_python_version": "3.12", "type_checker": "ty"})
        assert result.exit_code == 0
        assert file_contains_text(f"{result.project_path}/pyproject.toml", 'python-version = "3.12"')


def test_python_version_file_default(cookies, tmp_path):
    """Test that .python-version recommends 3.14 by default"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"minimum_python_version": "3.9"})
        assert result.exit_code == 0
        assert os.path.isfile(f"{result.project_path}/.python-version")
        with open(f"{result.project_path}/.python-version") as f:
            assert f.read().strip() == "3.14"


@pytest.mark.parametrize(
    ("minimum_python_version", "development_python_version"),
    [("3.9", None), ("3.13", None), ("3.9", "3.11"), ("3.12", "3.12"), ("3.10", "3.13")],
)
def test_development_python_version(cookies, tmp_path, minimum_python_version, development_python_version):
    """Test that .python-version, Docker and devcontainer images follow development_python_version"""
    extra_context = {"minimum_python_version": minimum_python_version}
    if development_python_version is not None:
        extra_context["development_python_version"] = development_python_version
    expected = development_python_version or "3.14"
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context=extra_context)
        assert result.exit_code == 0
        with open(f"{result.project_path}/.python-version") as f:
            assert f.read().strip() == expected
        assert file_contains_text(f"{result.project_path}/Dockerfile", f"FROM python:{expected}-slim")
        assert file_contains_text(
            f"{result.project_path}/.devcontainer/devcontainer.json",
            f"mcr.microsoft.com/devcontainers/python:{expected}",
        )
        # The minimum still drives requires-python
        assert file_contains_text(
            f"{result.project_path}/pyproject.toml", f'requires-python = ">={minimum_python_version},<4.0"'
        )


def test_development_python_version_below_minimum_fails(cookies, tmp_path):
    """Test that a development version lower than the minimum is rejected"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"minimum_python_version": "3.13", "development_python_version": "3.12"})
        assert result.exit_code != 0
        assert result.project_path is None


def _whitespace_problems(project_path) -> list[str]:
    """Return the text files that pre-commit's end-of-file-fixer or trailing-whitespace hooks would rewrite."""
    problems = []
    for path in sorted(project_path.rglob("*")):
        if not path.is_file() or ".git" in path.relative_to(project_path).parts:
            continue
        data = path.read_bytes()
        if b"\0" in data:
            continue  # binary file
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue  # binary file
        relative = path.relative_to(project_path).as_posix()
        if text and not text.endswith("\n"):
            problems.append(f"{relative}: missing final newline")
        elif text.endswith("\n\n") or text == "\n":
            problems.append(f"{relative}: more than one final newline")
        for number, line in enumerate(text.splitlines(), start=1):
            if line != line.rstrip():
                problems.append(f"{relative}:{number}: trailing whitespace")
    return problems


WHITESPACE_MATRIX = [
    {},
    {"layout": "src"},
    *({"type_checker": checker} for checker in ("pyright", "ty", "mypy", "pyrefly")),
    *(
        {"open_source_license": license_name}
        for license_name in (
            "MIT license",
            "BSD license",
            "ISC license",
            "Apache Software License 2.0",
            "GNU General Public License v3",
            "Not open source",
        )
    ),
    *({"agent_instructions": agents} for agents in ("suggested", "codex", "claude", "copilot", "cursor", "none")),
    *(
        {"agent_instructions": "all", "agent_profile": profile, "changelog": changelog}
        for profile in ("minimal", "full")
        for changelog in (True, False)
    ),
    {"codecov": False},
    {"deptry": False},
    {"dvc": True},
    {"dvc": True, "layout": "src", "type_checker": "mypy"},
    {"mkdocs": False},
    {"mkdocs": False, "publish_to_pypi": True},
    {"publish_to_pypi": True},
    {"include_github_actions": False},
    {"minimum_python_version": "3.13", "type_checker": "ty"},
    {
        "agent_instructions": "all",
        "agent_profile": "full",
        "changelog": False,
        "codecov": False,
        "deptry": False,
        "dockerfile": False,
        "devcontainer": False,
        "include_py_typed": False,
        "mkdocs": False,
        "include_github_actions": False,
        "open_source_license": "Not open source",
    },
    {
        "agent_instructions": "all",
        "agent_profile": "full",
        "layout": "src",
        "dvc": True,
        "publish_to_pypi": True,
        "type_checker": "pyrefly",
    },
]


@pytest.mark.parametrize(
    "extra_context",
    WHITESPACE_MATRIX,
    ids=lambda ctx: ",".join(f"{key}={value}" for key, value in ctx.items()) or "defaults",
)
def test_generated_files_end_with_single_newline(cookies, tmp_path, extra_context):
    """Test that every generated text file passes pre-commit's end-of-file-fixer and trailing-whitespace hooks"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context=extra_context)
        assert result.exit_code == 0
        assert _whitespace_problems(result.project_path) == []


def test_default_emails_are_neutral():
    root = Path(__file__).parent.parent
    for template in (root, root / "node"):
        assert json.loads((template / "cookiecutter.json").read_text())["email"] == "your.name@example.com"
