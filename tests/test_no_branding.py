from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

import pytest

# SHA-256 digests of retired names, as single words or two-word phrases, so this file does not publish them.
RETIRED_NAMES = {
    "0999f6bd2a640c3682255565458764371c3f847bfad2c649cea92930d5c5a22f",
    "3f63b943e1784c8c7f89ee7105e67cde939e30fb877af4f0fffb7215f7194759",
    "b944d5a40ae992df7827066881324beb84be2ba98e25a49681219b3d92ddc0fb",
    "dabfcad0350507fc302dbcaca6e8ff1ad2be9cc549511bab488cb207101070f5",
}


def digest(term: str) -> str:
    return hashlib.sha256(term.encode()).hexdigest()


def retired_terms(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    terms = set(words) | {f"{first} {second}" for first, second in zip(words, words[1:])}
    return {term for term in terms if digest(term) in RETIRED_NAMES}


def test_tracked_files_do_not_contain_retired_names():
    root = Path(__file__).parent.parent
    listing = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True)  # noqa: S607
    if listing.returncode != 0:
        pytest.skip("not a git checkout")

    found = {}
    for name in listing.stdout.splitlines():
        path = root / name
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        terms = retired_terms(f"{name}\n{text}")
        if terms:
            found[name] = sorted(terms)

    assert not found
