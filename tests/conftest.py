from __future__ import annotations

import shutil
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest

# The only parts of the repository cookiecutter reads when it bakes the template.
TEMPLATE_PARTS = ("cookiecutter.json", "local_extensions.py", "hooks", "{{cookiecutter.project_name}}")


@pytest.fixture(scope="session", autouse=True)
def _minimal_template(request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory) -> Iterator[Path]:
    """Point pytest-cookies at a copy of the template that holds only what cookiecutter needs.

    Because the template has a ``pre_prompt`` hook, cookiecutter copies the whole template directory to a
    temporary directory before every bake. By default pytest-cookies uses the repository root as the template,
    so each bake would copy ``.venv``, ``.git``, caches and build output too. Baking from this minimal copy
    renders the same template with the same hooks, so test behavior is unchanged.

    Cookiecutter also leaves the (empty) parent of each temporary copy behind, so ``tempfile`` is pointed at a
    session directory that pytest cleans up, instead of the system temporary directory.
    """
    source = Path(request.config.option.template)
    template = tmp_path_factory.mktemp("template") / source.name
    template.mkdir()
    for part in TEMPLATE_PARTS:
        src = source / part
        if not src.exists():
            continue
        if src.is_dir():
            shutil.copytree(src, template / part, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy2(src, template / part)

    original_template = request.config.option.template
    original_tempdir = tempfile.tempdir
    request.config.option.template = str(template)
    tempfile.tempdir = str(tmp_path_factory.mktemp("cookiecutter-tmp"))
    try:
        yield template
    finally:
        request.config.option.template = original_template
        tempfile.tempdir = original_tempdir
