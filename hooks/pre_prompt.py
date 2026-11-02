"""Pre-prompt hook to set dynamic defaults based on OS username.

This hook runs before cookiecutter prompts the user and rewrites
cookiecutter.json with defaults based on the current OS user.
"""

from __future__ import annotations

import getpass
import json
import os
import re
import subprocess
from pathlib import Path


def get_display_name(username: str) -> str:
    """Convert username to a display name.

    Handles common patterns:
    - john.doe -> John Doe
    - john_doe -> John Doe
    - jdoe -> Jdoe (single word, just capitalize)
    """
    # Replace common separators with spaces
    name = re.sub(r"[._-]", " ", username)
    # Title case each word
    return name.title()


def get_git_email() -> str:
    """Return the email from git config, or an empty string if there is none."""
    try:
        result = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)  # noqa: S607
    except OSError:
        return ""
    return result.stdout.strip()


def main() -> None:
    """Rewrite cookiecutter.json with dynamic defaults."""
    username = getpass.getuser()

    # Try to get a nicer name from environment variables first
    full_name = os.environ.get("USER_FULLNAME") or os.environ.get("DISPLAY_NAME")
    if not full_name:
        full_name = get_display_name(username)

    # Read current cookiecutter.json
    cookiecutter_path = Path("cookiecutter.json")
    with open(cookiecutter_path) as f:
        config = json.load(f)

    # Update defaults with user-specific values
    config["author"] = full_name
    config["email"] = get_git_email() or config["email"]
    config["author_github_handle"] = username

    # Write back
    with open(cookiecutter_path, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
