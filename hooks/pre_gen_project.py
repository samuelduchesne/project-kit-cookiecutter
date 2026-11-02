from __future__ import annotations

import re
import sys

PROJECT_NAME_REGEX = r"^[-a-zA-Z][-a-zA-Z0-9]+$"
project_name = "{{cookiecutter.project_name}}"
if not re.match(PROJECT_NAME_REGEX, project_name):
    print(
        f"ERROR: The project name {project_name} is not a valid Python module name. Please do not use a _ and use - instead"
    )
    sys.exit(1)

PROJECT_SLUG_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
project_slug = "{{cookiecutter.project_slug}}"
if not re.match(PROJECT_SLUG_REGEX, project_slug):
    print(
        f"ERROR: The project slug {project_slug} is not a valid Python module name. Please do not use a - and use _ instead"
    )
    # Exit to cancel project
    sys.exit(1)

minimum_python_version = "{{cookiecutter.minimum_python_version}}"
development_python_version = "{{cookiecutter.development_python_version}}"
if tuple(map(int, development_python_version.split("."))) < tuple(map(int, minimum_python_version.split("."))):
    print(
        f"ERROR: The development Python version {development_python_version} is lower than the minimum Python "
        f"version {minimum_python_version}. Please choose a development version >= {minimum_python_version}"
    )
    sys.exit(1)

# Boolean options are rendered as strings (never as Python literals) and validated here, before any file is generated.
# Cookiecutter < 2.7 keeps command-line overrides such as ``dvc=false`` as strings; ``local_extensions.py`` converts the
# recognised spellings to real booleans for the templates, so anything still unrecognised here would render wrongly.
TRUE_STRINGS = frozenset({"1", "true", "t", "yes", "y", "on"})
FALSE_STRINGS = frozenset({"0", "false", "f", "no", "n", "off"})
BOOLEAN_OPTIONS = {
    "include_py_typed": "{{ cookiecutter.include_py_typed }}",
    "include_github_actions": "{{ cookiecutter.include_github_actions }}",
    "codecov": "{{ cookiecutter.codecov }}",
    "publish_to_pypi": "{{ cookiecutter.publish_to_pypi }}",
    "deptry": "{{ cookiecutter.deptry }}",
    "dockerfile": "{{ cookiecutter.dockerfile }}",
    "devcontainer": "{{ cookiecutter.devcontainer }}",
    "mkdocs": "{{ cookiecutter.mkdocs }}",
    "dvc": "{{ cookiecutter.dvc }}",
    "changelog": "{{ cookiecutter.changelog }}",
}
for option, value in BOOLEAN_OPTIONS.items():
    if value.strip().lower() not in TRUE_STRINGS | FALSE_STRINGS:
        print(
            f"ERROR: {value!r} is not a valid value for the boolean option {option}. "
            f"Use true or false (or one of: {', '.join(sorted(TRUE_STRINGS | FALSE_STRINGS))})."
        )
        sys.exit(1)
