#!/usr/bin/env python3
"""Validate a shot timeline and assemble existing keyframes; never generate imagery.

Requires Python 3.10+ and Pillow. Files are resolved relative to the plan.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import re
import sys

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError as exc:
    raise SystemExit("Pillow is required; use an environment with Pillow installed.") from exc


TOLERANCE = 0.001
STATE_ORDER = {"start": 0, "key": 1, "end": 2}
MAX_CANVAS_PIXELS = 60_000_000
CAPTION_FIELDS = {
    "purpose": ("目的：", 3),
    "shot_size": ("景别：", 1),
    "camera": ("相机：", 2),
    "action": ("动作：", 3),
    "copy": ("文字/声音：", 3),
    "notes": ("备注：", 2),
}


@dataclass(frozen=True)
class Panel:
    shot_id: str
    start_s: float
    duration_s: float
    state: str
    file: Path
    caption: tuple[tuple[str, str], ...] = ()


def finite_number(value: object, label: str, *, positive: bool = False) -> float:
    if type(value) not in (int, float):
        raise ValueError(f"{label}: expected a finite number")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{label}: number is too large") from exc
    if not math.isfinite(result) or (positive and result <= 0):
        raise ValueError(f"{label}: expected a {'positive ' if positive else ''}finite number")
    return result


def load_plan(path: Path) -> tuple[str, tuple[int, int], list[Panel]]:
    return parse_plan(path, json.loads(path.read_text(encoding="utf-8")))


def parse_plan(path: Path, data: object) -> tuple[str, tuple[int, int], list[Panel]]:
    if not isinstance(data, dict):
        raise ValueError("plan must be an object")
    ratio = data.get("aspect_ratio")
    if not isinstance(ratio, str) or not re.fullmatch(r"[1-9][0-9]{0,5}:[1-9][0-9]{0,5}", ratio):
        raise ValueError("aspect_ratio must be a positive integer ratio, e.g. 16:9")
    aspect = tuple(map(int, ratio.split(":")))
    total = finite_number(data.get("total_duration_s"), "total_duration_s", positive=True)
    title = data.get("title", "Storyboard")
    if not isinstance(title, str):
        raise ValueError("title must be text")
    revision = data.get("revision")
    if revision is not None and (not isinstance(revision, str) or not revision.strip()):
        raise ValueError("revision must be non-empty text when provided")
    shots = data.get("shots")
    if not isinstance(shots, list) or not shots:
        raise ValueError("shots must be a non-empty list")
    root = path.resolve().parent
    ids: set[str] = set()
    cursor = 0.0
    panels: list[Panel] = []
    for shot in shots:
        if not isinstance(shot, dict):
            raise ValueError("each shot must be an object")
        shot_id = shot.get("id")
        if not isinstance(shot_id, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", shot_id):
            raise ValueError("shot id must start with a letter and contain letters/digits/_/-")
        if shot_id in ids:
            raise ValueError(f"duplicate shot id: {shot_id}")
        ids.add(shot_id)
        start = finite_number(shot.get("start_s"), f"{shot_id}.start_s")
        duration = finite_number(shot.get("duration_s"), f"{shot_id}.duration_s", positive=True)
        if start < 0 or abs(start - cursor) > TOLERANCE:
            raise ValueError(f"{shot_id}: non-contiguous timeline; expected start {cursor:g}")
        cursor += duration
        caption_data = shot.get("caption", {})
        if not isinstance(caption_data, dict) or set(caption_data) - CAPTION_FIELDS.keys():
            raise ValueError(f"{shot_id}: caption must contain supported caption fields")
        if any(not isinstance(value, str) for value in caption_data.values()):
            raise ValueError(f"{shot_id}: caption values must be text")
        caption = tuple((key, caption_data[key].strip()) for key in CAPTION_FIELDS
                        if caption_data.get(key, "").strip())
        frames = shot.get("frames")
        if not isinstance(frames, list) or not frames:
            raise ValueError(f"{shot_id}: at least one actual frame is required")
        states: list[int] = []
        for frame in frames:
            if (not isinstance(frame, dict) or not isinstance(frame.get("state"), str)
                    or frame["state"] not in STATE_ORDER):
                raise ValueError(f"{shot_id}: frame state must be start, key or end")
            states.append(STATE_ORDER[frame["state"]])
            filename = frame.get("file")
            if not isinstance(filename, str) or not filename.strip() or Path(filename).is_absolute():
                raise ValueError(f"{shot_id}: frame file must be a project-relative path")
            source = (root / filename).resolve()
            if not source.is_relative_to(root):
                raise ValueError(f"{shot_id}: frame file escapes the project directory")
            if not source.is_file():
                raise ValueError(f"{shot_id}: missing frame: {filename}")
            panels.append(Panel(shot_id, start, duration, frame["state"], source, caption))
        if states != sorted(set(states)):
            raise ValueError(f"{shot_id}: frame states must be unique and ordered start/key/end")
    if abs(cursor - total) > TOLERANCE:
        raise ValueError(f"timeline totals {cursor:g}s, expected {total:g}s")
    return title, aspect, panels


def choose_font(filename: str | None, size: int) -> ImageFont.ImageFont:
    if filename:
        return ImageFont.truetype(filename, size)
    for candidate in (
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "C:/Windows/Fonts/msyh.ttc",
    ):
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.ImageFont, width: int, max_lines: int) -> tuple[list[str], bool]:
    """Wrap by measured glyph width, including CJK text without spaces."""
    lines: list[str] = []
    for paragraph in text.replace("\t", " ").splitlines() or [""]:
        line = ""
        for char in paragraph:
            if line and font.getlength(line + char) > width:
                lines.append(line)
                line = char
            else:
                line += char
        lines.append(line)
    truncated = len(lines) > max_lines
    lines = lines[:max_lines]
    if truncated:
        last = lines[-1]
        while last and font.getlength(last + "…") > width:
            last = last[:-1]
        lines[-1] = last + "…"
    return lines, truncated


def file_sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def assemble(
    plan: Path,
    output: Path,
    *,
    columns: int = 3,
    cell_width: int = 640,
    page_size: int | None = None,
    font: str | None = None,
    overwrite: bool = False,
    manifest: Path | None = None,
) -> dict:
    plan_bytes = plan.read_bytes()
    snapshot = json.loads(plan_bytes)
    title, aspect, panels = parse_plan(plan, snapshot)
    if columns < 1 or cell_width < 80 or (page_size is not None and page_size < 1):
        raise ValueError("columns/page-size must be positive and cell-width at least 80")
    if output.suffix.lower() != ".png":
        raise ValueError("output must have the .png extension")
    per_page = page_size or len(panels)
    pages = [panels[i : i + per_page] for i in range(0, len(panels), per_page)]
    outputs = [
        output if len(pages) == 1 else output.with_name(f"{output.stem}-{i + 1:02d}.png")
        for i in range(len(pages))
    ]
    if manifest is not None and manifest.suffix.lower() != ".json":
        raise ValueError("manifest must have the .json extension")
    destinations = outputs + ([manifest] if manifest is not None else [])
    resolved_destinations = [p.resolve() for p in destinations]
    if len(set(resolved_destinations)) != len(destinations):
        raise ValueError("outputs and manifest must use distinct paths")
    for destination in resolved_destinations:
        if any(other in destination.parents for other in resolved_destinations):
            raise ValueError("output paths cannot be ancestors of one another")
        if destination.exists() and not destination.is_file():
            raise ValueError(f"output target must be a regular file: {destination}")
        if any(parent.exists() and not parent.is_dir() for parent in destination.parents):
            raise ValueError(f"output parent must be a directory: {destination}")
    for destination in destinations:
        if destination.exists() and not overwrite:
            raise ValueError(f"output already exists; use a new name or --overwrite: {destination}")
        if destination.resolve() in {p.file for p in panels} or destination.resolve() == plan.resolve():
            raise ValueError("output cannot overwrite an input file")
    cell_height = max(1, round(cell_width * aspect[1] / aspect[0]))
    gutter, header = 20, 64
    label_font = choose_font(font, 19)
    title_font = choose_font(font, 25)
    rich_captions = any(panel.caption for panel in panels)
    caption_font = choose_font(font, 17)
    line_height = max(24, caption_font.getbbox("Ag国")[3] - caption_font.getbbox("Ag国")[1] + 6)
    warnings = []
    panel_lines: dict[Panel, list[str]] = {}
    for panel in panels:
        label = f"{panel.shot_id} | {panel.start_s:g}-{panel.start_s + panel.duration_s:g}s | {panel.state}"
        if rich_captions:
            lines, truncated = wrap_text(label, caption_font, cell_width - 16, 3)
            if truncated:
                warnings.append(f"{panel.shot_id}/{panel.state}: display label truncated; use the plan for full text")
            for key, value in panel.caption:
                prefix, limit = CAPTION_FIELDS[key]
                extra, truncated = wrap_text(prefix + value, caption_font, cell_width - 16, limit)
                lines.extend(extra)
                if truncated:
                    warnings.append(f"{panel.shot_id}/{panel.state}: caption.{key} truncated; full text remains in the plan")
            panel_lines[panel] = lines
        else:
            panel_lines[panel] = [label]
    dimensions = []
    page_row_heights = []
    for page in pages:
        cols = min(columns, len(page))
        rows = math.ceil(len(page) / cols)
        row_heights = [
            max(40, 16 + max(len(panel_lines[p]) for p in page[r * cols:(r + 1) * cols]) * line_height)
            if rich_captions else 40
            for r in range(rows)
        ]
        page_row_heights.append(row_heights)
        width = cols * cell_width + (cols + 1) * gutter
        height = header + rows * (cell_height + gutter) + sum(row_heights) + gutter
        if width * height > MAX_CANVAS_PIXELS:
            raise ValueError("board exceeds 60 megapixels; reduce cell-width or use --page-size")
        dimensions.append((width, height))
    # Check every source before writing any output page.
    for panel in panels:
        with Image.open(panel.file) as source:
            source.verify()
    manifest_pages = []
    source_hashes = {p.file: file_sha256(p.file) for p in panels} if manifest is not None else {}
    for page_index, page in enumerate(pages):
        board = Image.new("RGB", dimensions[page_index], "#eceff1")
        draw = ImageDraw.Draw(board)
        heading = title + (f" · {snapshot['revision']}" if snapshot.get("revision") else "")
        heading += f" ({page_index + 1}/{len(pages)})" if len(pages) > 1 else ""
        heading = wrap_text(heading, title_font, dimensions[page_index][0] - 2 * gutter, 1)[0][0]
        draw.text((gutter, 18), heading, fill="#172027", font=title_font)
        cols = min(columns, len(page))
        row_heights = page_row_heights[page_index]
        row_tops = [header]
        for height in row_heights[:-1]:
            row_tops.append(row_tops[-1] + cell_height + height + gutter)
        cells = []
        for index, panel in enumerate(page):
            x = gutter + (index % cols) * (cell_width + gutter)
            y = row_tops[index // cols]
            with Image.open(panel.file) as source:
                frame = ImageOps.exif_transpose(source).convert("RGBA")
                actual_ratio = frame.width / frame.height
                if abs(actual_ratio / (aspect[0] / aspect[1]) - 1) > 0.01:
                    warnings.append(f"{panel.shot_id}/{panel.state}: aspect mismatch; letterboxed, never cropped")
                fitted = ImageOps.contain(frame, (cell_width, cell_height), Image.Resampling.LANCZOS)
            draw.rectangle((x, y, x + cell_width - 1, y + cell_height - 1), fill="white")
            board.paste(fitted, (x + (cell_width - fitted.width) // 2, y + (cell_height - fitted.height) // 2), fitted)
            for line_index, line in enumerate(panel_lines[panel]):
                draw.text((x, y + cell_height + 8 + line_index * line_height), line,
                          fill="#172027", font=caption_font if rich_captions else label_font)
            if manifest is not None:
                cells.append({
                    "slot": index + 1, "shot_id": panel.shot_id, "state": panel.state,
                    "source": panel.file.relative_to(plan.resolve().parent).as_posix(),
                    "source_sha256": source_hashes[panel.file],
                    "image_box": [x, y, cell_width, cell_height],
                    "caption_box": [x, y + cell_height, cell_width, row_heights[index // cols]],
                })
        outputs[page_index].parent.mkdir(parents=True, exist_ok=True)
        board.save(outputs[page_index], format="PNG")
        if manifest is not None:
            manifest_pages.append({"file": str(outputs[page_index].resolve()),
                                   "size": list(dimensions[page_index]), "panels": cells})
    if manifest is not None:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps({
            "schema_version": 1,
            "plan": {"file": plan.name, "sha256": hashlib.sha256(plan_bytes).hexdigest(),
                     "snapshot": snapshot},
            "pages": manifest_pages, "warnings": warnings,
            "scope": "Records selected files and plan text; does not verify product truth or visual consistency.",
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = {
        "outputs": [str(p.resolve()) for p in outputs],
        "panels": len(panels),
        "warnings": warnings,
        "scope": "Layout and timeline checks only; product truth and rendered content require visual review.",
    }
    if manifest is not None:
        result["manifest"] = str(manifest.resolve())
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--columns", type=int, default=3)
    parser.add_argument("--cell-width", type=int, default=640)
    parser.add_argument("--page-size", type=int)
    parser.add_argument("--font")
    parser.add_argument("--manifest", type=Path, help="Optional JSON with the plan snapshot and selected-frame provenance")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        result = assemble(args.plan, args.output, columns=args.columns, cell_width=args.cell_width,
                          page_size=args.page_size, font=args.font, overwrite=args.overwrite, manifest=args.manifest)
    except (ValueError, OSError, Image.DecompressionBombError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
