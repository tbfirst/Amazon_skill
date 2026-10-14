"""Build a self-contained Lovart instruction text from the maintained skill.

Standard library only. This script does not contact Lovart or generate images.
Run with --check to verify that the delivery file is up to date.
"""

import argparse
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "LOVART_INSTRUCTIONS.md"
REFERENCE_LINK = re.compile(r"\[([^\]]+)\]\((references/[a-z-]+\.md)\)")


def render():
    source = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n.*?\n---\n", source, re.DOTALL)
    if match is None:
        raise ValueError("SKILL.md must start with YAML frontmatter")
    body = source[match.end():].strip()
    modules = dict.fromkeys(path for _, path in REFERENCE_LINK.findall(body))
    if not modules:
        raise ValueError("No referenced modules found")

    pieces = [
        "<!-- Generated from SKILL.md and its referenced modules. Edit the sources, then rebuild. -->",
        "These standalone instructions contain the full workflow for a loaded Lovart custom skill. Use only the sections relevant to the current task; no external module files are required.",
        REFERENCE_LINK.sub(lambda item: item.group(1) + " (section below)", body),
    ]
    for relative in modules:
        path = (ROOT / relative).resolve()
        if not path.is_relative_to((ROOT / "references").resolve()):
            raise ValueError(f"Reference is outside references/: {relative}")
        module = path.read_text(encoding="utf-8").strip()
        if not module.startswith("# "):
            raise ValueError(f"Module must have a title: {relative}")
        if REFERENCE_LINK.search(module):
            raise ValueError(f"Nested module links require explicit packaging: {relative}")
        pieces.extend(["---", module])
    return "\n\n".join(pieces) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check without writing")
    args = parser.parse_args()
    try:
        expected = render()
        if args.check:
            if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != expected:
                parser.exit(1, "Lovart delivery is missing or stale; run this script without --check.\n")
            print("Lovart delivery matches all source modules.")
        else:
            OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
            print(f"Built {OUTPUT.name}: {len(expected)} characters.")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Build failed: {error}\n")


if __name__ == "__main__":
    main()
