#!/usr/bin/env python3
"""Render paired upload PNGs from one shot plan. No image generation or video submission."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

from PIL import Image, ImageDraw, ImageOps
from assemble_storyboard import (MAX_CANVAS_PIXELS, choose_font, file_sha256,
                                 finite_number, parse_plan, wrap_text)

# Columns are grouped to keep the detailed table readable at upload size.
GROUPS = (
    (("scene", "场景/构图"), ("purpose", "目的"), ("camera", "相机路径/速度/停留"),
     ("lighting", "灯光")),
    (("states", "起→中→终"), ("action", "主体动作/接触/次数"),
     ("environment", "环境响应"), ("parallax", "空间参照/视差")),
    (("copy", "成片文字/时间/位置"), ("sound", "声音"), ("transition", "转场/接缝"),
     ("reference", "参考文件/事实来源"), ("constraints", "连续性/约束")),
)
FIELDS = {key for group in GROUPS for key, _ in group}


def validate(plan: Path, data: dict):
    title, aspect, panels = parse_plan(plan, data)
    if not isinstance(data.get("revision"), str) or not data["revision"].strip():
        raise ValueError("revision is required")
    if not isinstance(data.get("generation_id"), str) or not re.fullmatch(r"C[0-9]+", data["generation_id"]):
        raise ValueError("generation_id must identify one task, e.g. C01")
    offset = finite_number(data.get("global_offset_s"), "global_offset_s")
    if offset < 0:
        raise ValueError("global_offset_s must be nonnegative")
    for shot in data["shots"]:
        if not re.fullmatch(r"S[0-9]+", shot["id"]):
            raise ValueError("use stable S-IDs, e.g. S05; do not renumber per segment")
        details = shot.get("details")
        if not isinstance(details, dict) or set(details) != FIELDS:
            raise ValueError(f"{shot['id']}: details must contain exactly {sorted(FIELDS)}")
        if any(not isinstance(value, str) or not value.strip() for value in details.values()):
            raise ValueError(f"{shot['id']}: details values must be nonempty text; use an explicit none when appropriate")
        for frame in shot["frames"]:
            if not isinstance(frame.get("summary"), str) or not frame["summary"].strip():
                raise ValueError(f"{shot['id']}/{frame['state']}: summary is required below every frame")
    return title, aspect, panels


def build(plan: Path, output_dir: Path, *, font: str | None = None,
          columns: int = 3, grid_page_size: int = 6, table_page_size: int = 3):
    if columns not in (2, 3) or grid_page_size < 1 or table_page_size < 1:
        raise ValueError("columns must be 2 or 3; page sizes must be positive")
    raw = plan.read_bytes()
    data = json.loads(raw)
    title, aspect, panels = validate(plan, data)
    # Validate the complete package before creating output files.
    for panel in panels:
        with Image.open(panel.file) as source:
            source.verify()
    if output_dir.exists():
        raise ValueError("output directory already exists; choose a new revision directory")
    body_font = choose_font(font, 26)
    heading_font = choose_font(font, 32)
    line_height = max(36, body_font.getbbox("Ag国")[3] - body_font.getbbox("Ag国")[1] + 10)
    cell_width, gutter, header = 640, 24, 132
    image_height = round(cell_width * aspect[1] / aspect[0])
    if image_height < 1 or cell_width * image_height > MAX_CANVAS_PIXELS:
        raise ValueError("unsupported image aspect/size")
    states = {"start": "起态", "key": "中间关键态", "end": "终态"}
    offset = data["global_offset_s"]

    def lines(text, width):
        # Never ellipsize execution instructions; page guard asks the caller to split.
        return wrap_text(text, body_font, width, max(1, len(text) + 1))[0]

    def label(shot):
        start, end = shot["start_s"], shot["start_s"] + shot["duration_s"]
        return (f"{shot['id']} | {data['generation_id']} | {shot['duration_s']:g}秒\n"
                f"本段 {start:g}–{end:g}秒\n全片 {start + offset:g}–{end + offset:g}秒")

    specs = []
    frame_entries = [(shot, frame) for shot in data["shots"] for frame in shot["frames"]]
    for begin in range(0, len(frame_entries), grid_page_size):
        entries = frame_entries[begin:begin + grid_page_size]
        rows = []
        for row_begin in range(0, len(entries), columns):
            cells = []
            for shot, frame in entries[row_begin:row_begin + columns]:
                text = label(shot) + f"\n{shot['id']}/{frame['state']} · {states[frame['state']]}\n" + frame["summary"]
                cells.append((shot, frame, lines(text, cell_width - 24)))
            height = image_height + 24 + max(len(cell[2]) for cell in cells) * line_height
            rows.append((height, cells))
        specs.append(("storyboard", rows, columns * (cell_width + gutter) + gutter))
    for begin in range(0, len(data["shots"]), table_page_size):
        rows = []
        for shot in data["shots"][begin:begin + table_page_size]:
            texts = [lines(label(shot) + "\n对应格号：\n" + "\n".join(
                f"{shot['id']}/{frame['state']}" for frame in shot["frames"]), 300)]
            for group in GROUPS:
                texts.append(lines("\n".join(f"{name}：{shot['details'][key]}" for key, name in group), 600))
            rows.append((max(map(len, texts)) * line_height + 32, [(shot, texts)]))
        specs.append(("shot-table", rows, 2 * gutter + 324 + 3 * 624))
    for kind, rows, width in specs:
        height = header + sum(row[0] + gutter for row in rows) + gutter
        # A very tall single row should be rewritten or given a separate readable page.
        if width * height > MAX_CANVAS_PIXELS or height > 12000:
            raise ValueError(f"{kind}: page too large; reduce page size or shorten redundant detail")

    output_dir.mkdir(parents=True)
    pages, counts = [], {"storyboard": 0, "shot-table": 0}
    for kind, rows, width in specs:
        counts[kind] += 1
        height = header + sum(row[0] + gutter for row in rows) + gutter
        board = Image.new("RGB", (width, height), "#edf1f3")
        draw = ImageDraw.Draw(board)
        heading = f"{data['generation_id']} · {data['revision']} · {'宫格故事板' if kind == 'storyboard' else '详细分镜表'} · {counts[kind]:02d}"
        draw.text((gutter, 12), heading, font=heading_font, fill="#142b3b")
        draw.text((gutter, 58), f"本段 {data['total_duration_s']:g}秒 | 全片偏移 {offset:g}秒 | 说明/镜号不进入成片", font=body_font, fill="#142b3b")
        records = []
        y = header
        for row_height, cells in rows:
            if kind == "storyboard":
                for col, (shot, frame, text_lines) in enumerate(cells):
                    x = gutter + col * (cell_width + gutter)
                    draw.rectangle((x, y, x + cell_width, y + row_height), fill="white")
                    source_path = (plan.parent / frame["file"]).resolve()
                    with Image.open(source_path) as source:
                        source_image = ImageOps.exif_transpose(source).convert("RGBA")
                        fitted = ImageOps.contain(source_image, (cell_width, image_height), Image.Resampling.LANCZOS)
                        board.paste(fitted, (x + (cell_width - fitted.width) // 2,
                                             y + (image_height - fitted.height) // 2), fitted)
                    for index, line in enumerate(text_lines):
                        draw.text((x + 12, y + image_height + 12 + index * line_height), line, font=body_font, fill="#142b3b")
                    records.append({"shot_id": shot["id"], "timeline_label": label(shot), "state": frame["state"], "summary": frame["summary"],
                                    "source": frame["file"], "source_sha256": file_sha256(source_path),
                                    "image_box": [x, y, cell_width, image_height],
                                    "caption_box": [x, y + image_height, cell_width, row_height - image_height]})
            else:
                shot, texts = cells[0]
                x = gutter
                for col_width, text_lines in zip((324, 624, 624, 624), texts):
                    draw.rectangle((x, y, x + col_width, y + row_height), fill="white", outline="#a5b6c0", width=2)
                    for index, line in enumerate(text_lines):
                        draw.text((x + 12, y + 16 + index * line_height), line, font=body_font, fill="#142b3b")
                    x += col_width
                records.append({"shot_id": shot["id"], "timeline_label": label(shot), "frame_ids": [f"{shot['id']}/{f['state']}" for f in shot["frames"]],
                                "details": shot["details"], "row_box": [gutter, y, width - 2 * gutter, row_height]})
            y += row_height + gutter
        filename = f"{data['generation_id']}-{kind}-{counts[kind]:02d}.png"
        board.save(output_dir / filename)
        pages.append({"kind": kind, "file": filename, "sha256": file_sha256(output_dir / filename),
                      "size": [width, height], "records": records})
    manifest = {"schema_version": 1, "title": title, "revision": data["revision"],
                "generation_id": data["generation_id"], "plan_sha256": hashlib.sha256(raw).hexdigest(),
                "plan_snapshot": data, "pages": pages,
                "scope": "Shared plan ensures paired IDs, times and revision; visual review, prompt alignment and product truth still require review."}
    (output_dir / "boards-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--font")
    parser.add_argument("--columns", type=int, default=3)
    parser.add_argument("--grid-page-size", type=int, default=6)
    parser.add_argument("--table-page-size", type=int, default=3)
    args = parser.parse_args()
    try:
        result = build(args.plan, args.output_dir, font=args.font, columns=args.columns,
                       grid_page_size=args.grid_page_size, table_page_size=args.table_page_size)
    except (ValueError, OSError, Image.DecompressionBombError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"output_dir": str(args.output_dir), "pages": [page["file"] for page in result["pages"]]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
