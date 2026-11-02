"""Regression tests for boolean options passed as strings, e.g. ``cookiecutter . --no-input changelog=false``.

Before cookiecutter 2.7, command-line overrides of boolean variables reach the templates and hooks as strings. That
made the post-generation hook crash (``if not false:`` is a NameError) and made template conditionals such as
``{% if cookiecutter.dvc %}`` treat ``"False"`` or ``"0"`` as true, silently generating the wrong project.
"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

import pytest

from tests.utils import run_within_dir

REPO_ROOT = Path(__file__).resolve().parent.parent

FALSE_SPELLINGS = ["false", "False", "FALSE", "no", "n", "0", "off"]
TRUE_SPELLINGS = ["true", "True", "yes", "y", "1", "on"]
BOOLEAN_OPTIONS = ["changelog", "dvc", "mkdocs", "dockerfile", "codecov", "include_github_actions", "publish_to_pypi"]


@pytest.fixture(scope="session")
def template_dir(tmp_path_factory) -> Path:
    """A copy of the template holding only the files that ship with it (see MANIFEST.in).

    Baking from the repository root makes the pre_prompt hook copy the whole checkout, ``.venv`` included.
    """
    target = tmp_path_factory.mktemp("template") / "project-kit-cookiecutter"
    target.mkdir()
    for name in ("cookiecutter.json", "local_extensions.py"):
        shutil.copy2(REPO_ROOT / name, target / name)
    for name in ("hooks", "{{cookiecutter.project_name}}"):
        shutil.copytree(REPO_ROOT / name, target / name, ignore=shutil.ignore_patterns("__pycache__"))
    return target


def _snapshot(project_path: Path) -> dict[str, str]:
    """Map every generated file to a hash of its content."""
    return {
        str(path.relative_to(project_path)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(project_path.rglob("*"))
        if path.is_file()
    }


def _bake_snapshot(cookies, template_dir: Path, extra_context: dict[str, object]) -> dict[str, str]:
    result = cookies.bake(extra_context=extra_context, template=str(template_dir))
    assert result.exit_code == 0, result.exception
    assert result.exception is None
    return _snapshot(result.project_path)


@pytest.mark.parametrize("option", BOOLEAN_OPTIONS)
@pytest.mark.parametrize(
    ("spelling", "expected"),
    [(spelling, False) for spelling in FALSE_SPELLINGS] + [(spelling, True) for spelling in TRUE_SPELLINGS],
)
def test_string_boolean_override_matches_json_boolean(cookies, tmp_path, template_dir, option, spelling, expected):
    """A string override such as ``dvc=false`` generates exactly the project that a JSON ``false`` generates"""
    with run_within_dir(tmp_path):
        reference = _bake_snapshot(cookies, template_dir, {option: expected})
        actual = _bake_snapshot(cookies, template_dir, {option: spelling})
    assert sorted(actual) == sorted(reference), "the generated file set differs"
    changed = [path for path in reference if actual[path] != reference[path]]
    assert changed == [], "these files are rendered differently"


def test_all_booleans_off_as_strings(cookies, tmp_path, template_dir):
    """Every boolean turned off with a lowercase string at once matches the JSON-boolean bake"""
    options = ["include_py_typed", "include_github_actions", "codecov", "publish_to_pypi", "deptry"]
    options += ["dockerfile", "devcontainer", "mkdocs", "dvc", "changelog"]
    with run_within_dir(tmp_path):
        reference = _bake_snapshot(cookies, template_dir, dict.fromkeys(options, False))
        actual = _bake_snapshot(cookies, template_dir, dict.fromkeys(options, "false"))
    assert actual == reference
    assert "CHANGELOG.md" not in actual
    assert "mkdocs.yml" not in actual
    assert "dvc.yaml" not in actual


def test_invalid_boolean_override_fails_clearly(cookies, tmp_path, template_dir, capfd):
    """An unrecognised value such as ``dvc=maybe`` stops generation instead of being treated as true"""
    with run_within_dir(tmp_path):
        result = cookies.bake(extra_context={"dvc": "maybe"}, template=str(template_dir))
    assert result.exit_code != 0
    out = capfd.readouterr().out
    # cookiecutter >= 2.7 rejects the value itself; older versions leave it to pre_gen_project.py.
    assert "is not a valid value for the boolean option dvc" in out or "could not be converted to a boolean" in str(
        result.exception
    )
    assert not (tmp_path / "example-project").exists()


@pytest.mark.parametrize(("value", "expected"), [("false", False), (" No ", False), ("TRUE", True), ("on", True)])
def test_normalise_booleans(value, expected):
    from local_extensions import normalise_booleans

    context = {"dvc": value, "project_name": "no", "layout": "src"}
    normalise_booleans(context)
    assert context == {"dvc": expected, "project_name": "no", "layout": "src"}


def test_normalise_booleans_leaves_unknown_values():
    from local_extensions import normalise_booleans

    context = {"dvc": "maybe", "mkdocs": True}
    normalise_booleans(context)
    assert context == {"dvc": "maybe", "mkdocs": True}
