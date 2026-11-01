#!/usr/bin/env python3
"""Check the slim Jimeng delivery tree and every uploaded image, without modifying files."""
from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path
import re
import sys

from PIL import Image, ImageOps

ROOT_FILES = {"分析说明书.md", "README.md", "shot-list.csv"}
IMAGE_EXTENSIONS = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG"}


def check_image(path: Path) -> dict:
    with Image.open(path) as source:
        if source.format != IMAGE_EXTENSIONS.get(path.suffix.lower()):
            raise ValueError(f"{path.name}: expected a PNG/JPEG matching its extension")
        if getattr(source, "n_frames", 1) != 1:
            raise ValueError(f"{path.name}: animated/multiframe images are not upload references")
        source.verify()
    with Image.open(path) as source:
        source.load()
        width, height = ImageOps.exif_transpose(source).size
    if height < 350 or not (3 * height <= 5 * width <= 8 * height):
        raise ValueError(f"{path.name}: {width}x{height}; require height >=350 and 0.6<=width/height<=1.6")
    return {"file": path.name, "width": width, "height": height,
            "ratio": width / height, "square": width == height}


def check(root: Path) -> dict:
    if root.is_symlink() or not root.is_dir():
        raise ValueError("delivery root must be a real directory")
    entries = {p.name: p for p in root.iterdir()}
    segments = sorted(name for name in entries if re.fullmatch(r"C\d{2}", name))
    if segments not in (["C01"], ["C01", "C02"]):
        raise ValueError("deliver C01 only, or C01 and C02; no empty extra segments")
    if set(entries) != ROOT_FILES | set(segments):
        raise ValueError(f"root must contain only {sorted(ROOT_FILES)} and {segments}")
    for name in ROOT_FILES:
        p = entries[name]
        if p.is_symlink() or not p.is_file() or not p.stat().st_size:
            raise ValueError(f"{name}: expected a nonempty regular file")
        p.read_text(encoding="utf-8-sig")
    raw = (root / "shot-list.csv").read_bytes()
    if not raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("shot-list.csv must use UTF-8 BOM")
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8-sig"))))
    if len(rows) < 2 or not rows[0] or any(len(row) != len(rows[0]) for row in rows[1:]):
        raise ValueError("shot-list.csv must have a header and consistently sized shot rows")
    report = {"segments": {}, "warnings": [],
              "scope": "Checks file scope, per-segment image count and image dimensions only; prompt/shot identity, facts and readability need review."}
    for segment in segments:
        folder = entries[segment]
        if folder.is_symlink() or not folder.is_dir():
            raise ValueError(f"{segment}: expected a real directory")
        prompt = folder / f"{segment}.draft.txt"
        if prompt.is_symlink() or not prompt.is_file() or not prompt.read_text(encoding="utf-8-sig").strip():
            raise ValueError(f"{segment}: missing nonempty {segment}.draft.txt")
        images = []
        numbers = []
        board_roles = []
        for p in sorted(folder.iterdir()):
            if p.is_symlink() or not p.is_file():
                raise ValueError(f"{segment}/{p.name}: nested folders and links are not allowed")
            if p == prompt:
                continue
            match = re.match(r"(\d{2,})-", p.name)
            if p.suffix.lower() not in IMAGE_EXTENSIONS or not match:
                raise ValueError(f"{segment}/{p.name}: only numbered upload PNG/JPEG images and the prompt are allowed")
            numbers.append(int(match[1]))
            board_match = re.fullmatch(r"\d{2,}-(?:(C\d+)-)?(shot-table|storyboard)(?:-\d+)?", p.stem)
            if board_match:
                if board_match[1] and board_match[1] != segment:
                    raise ValueError(f"{segment}/{p.name}: board C-ID does not match its folder")
                board_roles.append(board_match[2])
            info = check_image(p)
            images.append(info)
            if not info["square"]:
                report["warnings"].append(f"{segment}/{p.name}: allowed ratio; prefer 1:1 if legibility permits")
        if len(images) > 9:
            raise ValueError(f"{segment}: at most 9 upload images across all roles; found {len(images)}")
        if sorted(numbers) != list(range(1, len(images) + 1)):
            raise ValueError(f"{segment}: image upload numbers must be unique and contiguous from 01")
        for role in ("shot-table", "storyboard"):
            if role not in board_roles:
                raise ValueError(f"{segment}: missing {role} upload image")
        report["segments"][segment] = images
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    try:
        result = check(args.root)
    except (ValueError, OSError, UnicodeError, csv.Error, Image.DecompressionBombError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
