from __future__ import annotations

import re
import sys

# The project name is also the npm package name and the folder name: npm's rules for an unscoped name
# (lowercase, URL-safe, at most 214 characters), starting with a letter like the Python template's names.
PROJECT_NAME_REGEX = r"[a-z](?:[a-z0-9-]*[a-z0-9])?"
project_name = "{{cookiecutter.project_name}}"
if not re.fullmatch(PROJECT_NAME_REGEX, project_name) or len(project_name) > 214:
    print(
        f"ERROR: The project name {project_name} is not a valid npm package name. Use lowercase letters, digits and -, "
        "starting with a letter and not ending with -"
    )
    sys.exit(1)

# Boolean options are rendered as strings (never as Python literals) and validated here, before any file is generated.
# ``local_extensions.py`` converts the recognised spellings of command-line overrides to real booleans.
TRUE_STRINGS = frozenset({"1", "true", "t", "yes", "y", "on"})
FALSE_STRINGS = frozenset({"0", "false", "f", "no", "n", "off"})
BOOLEAN_OPTIONS = {
    "include_github_actions": "{{ cookiecutter.include_github_actions }}",
    "codecov": "{{ cookiecutter.codecov }}",
    "publish_to_npm": "{{ cookiecutter.publish_to_npm }}",
    "devcontainer": "{{ cookiecutter.devcontainer }}",
    "changelog": "{{ cookiecutter.changelog }}",
}
for option, value in BOOLEAN_OPTIONS.items():
    if value.strip().lower() not in TRUE_STRINGS | FALSE_STRINGS:
        print(
            f"ERROR: {value!r} is not a valid value for the boolean option {option}. "
            f"Use true or false (or one of: {', '.join(sorted(TRUE_STRINGS | FALSE_STRINGS))})."
        )
        sys.exit(1)
