"""Jinja extensions loaded by cookiecutter through ``_extensions`` in ``cookiecutter.json``.

Cookiecutter imports this module from the template folder, so it must stay at the top level of each template: the
repository root, and ``node/``, which keeps an identical copy.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, MutableMapping
from pathlib import Path
from typing import Any

from jinja2 import Environment
from jinja2.ext import Extension

TRUE_STRINGS = frozenset({"1", "true", "t", "yes", "y", "on"})
FALSE_STRINGS = frozenset({"0", "false", "f", "no", "n", "off"})
BOOLEAN_STRINGS = TRUE_STRINGS | FALSE_STRINGS


def _boolean_options(template_dir: Path) -> frozenset[str] | None:
    """Return the names of the variables whose default in the template's ``cookiecutter.json`` is a JSON boolean.

    ``None`` when the file can't be read.
    """
    try:
        defaults = json.loads((template_dir / "cookiecutter.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(defaults, dict):
        return None
    return frozenset(name for name, value in defaults.items() if isinstance(value, bool))


# Read once at import: cookiecutter may run from a temporary copy of the template that is deleted after the bake,
# while the imported module stays cached in ``sys.modules``. Without the defaults nothing is normalised and
# pre_gen_project.py rejects the string values.
BOOLEAN_OPTIONS = _boolean_options(Path(__file__).parent) or frozenset()


def boolean_options(cookiecutter: Mapping[str, Any]) -> frozenset[str]:
    """Return the boolean options of the template being rendered.

    Python imports this module once per process, under one name, so the copy in use may belong to the other template:
    after a bake of the other template in the same process, or when an editable install puts the repository root on
    ``sys.path``. ``_repo_dir``, which cookiecutter adds to the context before it renders files and hooks, names the
    template actually being rendered. Earlier renders, and every render under cruft (which calls cookiecutter's
    ``generate_files`` without setting ``_repo_dir``), fall back to the imported copy's options.
    """
    repo_dir = cookiecutter.get("_repo_dir")
    options = _boolean_options(Path(repo_dir)) if isinstance(repo_dir, str) and repo_dir else None
    return BOOLEAN_OPTIONS if options is None else options


def normalise_booleans(cookiecutter: MutableMapping[str, Any]) -> None:
    """Convert string values of boolean options (``"false"``, ``"no"``, ``"1"``...) to real booleans, in place.

    Cookiecutter < 2.7 keeps command-line overrides such as ``dvc=false`` as strings, and Jinja treats every
    non-empty string as true. Values that are not recognised are left untouched so that ``pre_gen_project.py``
    can reject them with a clear error.
    """
    pending = {
        name: lowered
        for name, value in cookiecutter.items()
        if isinstance(value, str) and (lowered := value.strip().lower()) in BOOLEAN_STRINGS
    }
    if not pending:
        return
    options = boolean_options(cookiecutter)
    for name, lowered in pending.items():
        if name in options:
            cookiecutter[name] = lowered in TRUE_STRINGS


class BooleanOverridesExtension(Extension):
    """Normalise boolean overrides before any template, path or hook is rendered.

    Jinja builds a new context for every render; the ``cookiecutter`` mapping in it is the same object cookiecutter
    keeps for the whole bake, so normalising it in place on the first render fixes every later render too.
    """

    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        base_context = environment.context_class

        class NormalisingContext(base_context):  # type: ignore[valid-type,misc]
            def __init__(self, environment: Environment, parent: dict[str, Any], *args: Any, **kwargs: Any) -> None:
                cookiecutter = parent.get("cookiecutter")
                if isinstance(cookiecutter, MutableMapping):
                    normalise_booleans(cookiecutter)
                super().__init__(environment, parent, *args, **kwargs)

        environment.context_class = NormalisingContext
