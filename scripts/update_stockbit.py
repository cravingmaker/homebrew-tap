"""Use Homebrew to update Stockbit's version and checksum without Git mutations."""

import json
import os
from pathlib import Path
import re
import subprocess


CASK = "cravingmaker/tap/stockbit"


def newer_version(results):
    """Fail closed on malformed or skipped livecheck results; never downgrade."""
    if not isinstance(results, list) or len(results) != 1:
        raise ValueError("Expected exactly one Stockbit livecheck result")
    result = results[0]
    if not isinstance(result, dict) or result.get("cask") not in ("stockbit", CASK):
        raise ValueError("Livecheck result does not identify Stockbit")
    versions = result.get("version")
    if "status" in result or not isinstance(versions, dict):
        raise ValueError("Livecheck did not return a usable release version")
    for key in ("current", "latest"):
        value = versions.get(key)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9]+(?:\.[0-9]+)+", value):
            raise ValueError(f"Unsupported Stockbit {key} version: {value!r}")
    if type(versions.get("outdated")) is not bool:
        raise ValueError("Livecheck must report an explicit outdated boolean")
    if not versions["outdated"]:
        return None
    current = tuple(map(int, versions["current"].split(".")))
    latest = tuple(map(int, versions["latest"].split(".")))
    width = max(len(current), len(latest))
    if latest + (0,) * (width - len(latest)) <= current + (0,) * (width - len(current)):
        raise ValueError("Livecheck's proposed update is not newer")
    return versions["latest"]


def main():
    result = subprocess.run(
        ["brew", "livecheck", "--cask", "--json", CASK],
        check=True, stdout=subprocess.PIPE, text=True,
    )
    print(result.stdout, end="")
    version = newer_version(json.loads(result.stdout))
    if version:
        subprocess.run(
            ["brew", "bump-cask-pr", "--write-only", "--no-audit", "--no-style",
             f"--version={version}", CASK],
            check=True,
        )
    else:
        print("Stockbit is current; no update PR needed.")
    if output := os.environ.get("GITHUB_OUTPUT"):
        with Path(output).open("a", encoding="utf-8") as stream:
            stream.write(f"updated={str(version is not None).lower()}\n")
            if version:
                stream.write(f"version={version}\n")


if __name__ == "__main__":
    main()
