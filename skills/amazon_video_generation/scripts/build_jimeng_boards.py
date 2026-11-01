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

# Stable director columns follow the user's reference table. All execution fields
# remain visible; reference/research notes must already have been separated.
FIELDS = {"scene", "purpose", "camera", "lighting", "states", "action",
          "environment", "parallax", "copy", "sound", "transition", "reference",
          "constraints", "shot_size", "dialogue"}
TABLE_HEADERS = ("时间", "镜头编号", "景别", "摄像机角度与运动", "画面内容",
                 "演员动作", "产品展示重点", "台词/旁白", "音效/音乐", "字幕")
TABLE_WIDTHS = (200, 220, 180, 420, 520, 440, 480, 240, 240, 260)
MAX_UPLOAD_IMAGES = 9


def table_texts(shot, offset):
    d = shot["details"]
    start, end = shot["start_s"], shot["start_s"] + shot["duration_s"]
    return (
        f"本段\n{start:g}–{end:g}秒\n全片\n{start+offset:g}–{end+offset:g}秒",
        shot["id"] + "\n" + "\n".join(f"{shot['id']}/{f['state']}" for f in shot["frames"]),
        d["shot_size"],
        f"{d['camera']}\n空间：{d['parallax']}",
        f"{d['scene']}\n光线：{d['lighting']}\n状态：{d['states']}",
        f"{d['action']}\n环境响应：{d['environment']}",
        f"{d['purpose']}\n连续性：{d['constraints']}\n附件：{d['reference']}\n接镜：{d['transition']}",
        d["dialogue"], d["sound"], d["copy"],
    )


def validate(plan: Path, data: dict):
    title, aspect, panels = parse_plan(plan, data)
    if not isinstance(data.get("revision"), str) or not data["revision"].strip():
        raise ValueError("revision is required")
    if not isinstance(data.get("generation_id"), str) or data["generation_id"] not in ("C01", "C02"):
        raise ValueError("generation_id must be C01 or C02")
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
          columns: int = 3, grid_page_size: int = 9, table_page_size: int = 3,
          reference_image_count: int = 1):
    if columns != 3 or grid_page_size != 9 or table_page_size < 1:
        raise ValueError("storyboard requires exactly 3 columns and 9 slots; table page size must be positive")
    if isinstance(reference_image_count, bool) or not isinstance(reference_image_count, int) or not 0 <= reference_image_count <= MAX_UPLOAD_IMAGES:
        raise ValueError("reference_image_count must be an integer from 0 to 9")
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
    table_font = choose_font(font, 36)
    table_line_height = max(46, table_font.getbbox("Ag国")[3] - table_font.getbbox("Ag国")[1] + 10)
    line_height = max(36, body_font.getbbox("Ag国")[3] - body_font.getbbox("Ag国")[1] + 10)
    cell_width, gutter, header = 640, 24, 132
    image_height = round(cell_width * aspect[1] / aspect[0])
    if image_height < 1 or cell_width * image_height > MAX_CANVAS_PIXELS:
        raise ValueError("unsupported image aspect/size")
    states = {"start": "起态", "key": "中间关键态", "end": "终态"}
    offset = data["global_offset_s"]

    def lines(text, width, text_font=body_font):
        # Never ellipsize execution instructions; page guard asks the caller to split.
        return wrap_text(text, text_font, width, max(1, len(text) + 1))[0]

    def label(shot):
        start, end = shot["start_s"], shot["start_s"] + shot["duration_s"]
        return (f"{shot['id']} | {data['generation_id']} | {shot['duration_s']:g}秒\n"
                f"本段 {start:g}–{end:g}秒\n全片 {start + offset:g}–{end + offset:g}秒")

    specs = []
    frame_entries = [(shot, frame) for shot in data["shots"] for frame in shot["frames"]]
    for begin in range(0, len(frame_entries), 9):
        entries = frame_entries[begin:begin + 9]
        cells = []
        for shot, frame in entries:
            text = label(shot) + f"\n{shot['id']}/{frame['state']} · {states[frame['state']]}\n" + frame["summary"]
            cells.append((shot, frame, lines(text, cell_width - 24)))
        row_height = image_height + 24 + max(len(cell[2]) for cell in cells) * line_height
        cells.extend([(None, None, [])] * (9 - len(cells)))
        rows = [(row_height, cells[i:i + 3]) for i in range(0, 9, 3)]
        specs.append(("storyboard", rows, 3 * (cell_width + gutter) + gutter))
    def table_heading_height(widths):
        return max(len(lines(name, width - 24, table_font)) for name, width in zip(TABLE_HEADERS, widths)) * table_line_height + 32

    for begin in range(0, len(data["shots"]), table_page_size):
        candidates = []
        for usable in (2200, 2500, 2800, 3200):
            widths = [160, 220, 140]  # Keep S-ID/state labels and shot sizes readable.
            rest = usable - sum(widths)
            widths.extend(round(w * rest / sum(TABLE_WIDTHS[3:])) for w in TABLE_WIDTHS[3:])
            widths[-1] += usable - sum(widths)
            rows = []
            for shot in data["shots"][begin:begin + table_page_size]:
                texts = [lines(text, width - 24, table_font) for text, width in zip(table_texts(shot, offset), widths)]
                rows.append((max(map(len, texts)) * table_line_height + 32, [(shot, texts, widths)]))
            width = usable + 2 * gutter
            height = header + table_heading_height(widths) + sum(row[0] + gutter for row in rows) + gutter
            candidates.append((max(width, height), abs(width-height), rows, width))
        _, _, rows, width = min(candidates, key=lambda c:c[:2])
        specs.append(("shot-table", rows, width))
    if len(specs) + reference_image_count > MAX_UPLOAD_IMAGES:
        raise ValueError(f"upload image budget exceeds 9: {len(specs)} board pages + "
                         f"{reference_image_count} reference images; revise the plan before rendering")
    specs.sort(key=lambda spec: spec[0] != "shot-table")
    for kind, rows, width in specs:
        table_header_height = table_heading_height(rows[0][1][0][2]) if kind == "shot-table" else 0
        height = header + (table_header_height if kind == "shot-table" else 0) + sum(row[0] + gutter for row in rows) + gutter
        # A very tall single row should be rewritten or given a separate readable page.
        if max(width, height, 350) ** 2 > MAX_CANVAS_PIXELS:
            raise ValueError(f"{kind}: page too large; reduce page size or shorten redundant detail")

    output_dir.mkdir(parents=True)
    pages, counts = [], {"storyboard": 0, "shot-table": 0}
    for kind, rows, width in specs:
        counts[kind] += 1
        table_header_height = table_heading_height(rows[0][1][0][2]) if kind == "shot-table" else 0
        height = header + (table_header_height if kind == "shot-table" else 0) + sum(row[0] + gutter for row in rows) + gutter
        side = max(width, height, 350)
        board = Image.new("RGB", (side, side), "#18171a" if kind == "shot-table" else "#edf1f3")
        draw = ImageDraw.Draw(board)
        heading = f"{data['generation_id']} · {data['revision']} · {'宫格故事板' if kind == 'storyboard' else '详细分镜表'} · {counts[kind]:02d}"
        draw.text((gutter, 12), heading, font=heading_font, fill="white" if kind == "shot-table" else "#142b3b")
        draw.text((gutter, 58), f"本段 {data['total_duration_s']:g}秒 | 全片偏移 {offset:g}秒 | 说明/镜号不进入成片", font=body_font, fill="white" if kind == "shot-table" else "#142b3b")
        records, slots = [], []
        y = header
        if kind == "shot-table":
            x = gutter
            for name, col_width in zip(TABLE_HEADERS, rows[0][1][0][2]):
                draw.rectangle((x, y, x + col_width, y + table_header_height), fill="#29282d", outline="#73717a", width=2)
                for index, line in enumerate(lines(name, col_width - 24, table_font)):
                    draw.text((x + 12, y + 16 + index * table_line_height), line, font=table_font, fill="white")
                x += col_width
            y += table_header_height
        for row_height, cells in rows:
            if kind == "storyboard":
                for col, (shot, frame, text_lines) in enumerate(cells):
                    x = gutter + col * (cell_width + gutter)
                    slots.append({"slot": len(slots) + 1, "occupied": shot is not None,
                                  "box": [x, y, cell_width, row_height]})
                    draw.rectangle((x, y, x + cell_width, y + row_height), fill="white", outline="#a5b6c0", width=2)
                    if shot is None:
                        # Blank reserved slot: no invented shot, placeholder image or caption.
                        draw.line((x, y + image_height, x + cell_width, y + image_height), fill="#d4dce1", width=2)
                        continue
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
                shot, texts, widths = cells[0]
                x = gutter
                for col_width, text_lines in zip(widths, texts):
                    draw.rectangle((x, y, x + col_width, y + row_height), fill="#18171a", outline="#73717a", width=2)
                    for index, line in enumerate(text_lines):
                        draw.text((x + 12, y + 16 + index * table_line_height), line, font=table_font, fill="#f4f2f5")
                    x += col_width
                records.append({"shot_id": shot["id"], "timeline_label": label(shot), "frame_ids": [f"{shot['id']}/{f['state']}" for f in shot["frames"]],
                                "details": shot["details"], "columns": dict(zip(TABLE_HEADERS, table_texts(shot, offset))), "row_box": [gutter, y, width - 2 * gutter, row_height]})
            y += row_height + gutter
        filename = f"{len(pages) + 1:02d}-{data['generation_id']}-{kind}-{counts[kind]:02d}.png"
        board.save(output_dir / filename)
        pages.append({"kind": kind, "file": filename, "sha256": file_sha256(output_dir / filename),
                      "size": [side, side], "content_size": [width, height], "records": records,
                      "slots": slots, "headers": list(TABLE_HEADERS) if kind == "shot-table" else []})
    manifest = {"schema_version": 2, "title": title, "revision": data["revision"],
                "generation_id": data["generation_id"],
                "upload_budget": {"board_images": len(pages), "reference_images": reference_image_count,
                                  "total": len(pages) + reference_image_count, "limit": MAX_UPLOAD_IMAGES},
                "plan_sha256": hashlib.sha256(raw).hexdigest(),
                "plan_snapshot": data, "pages": pages,
                "scope": "Shared plan ensures paired IDs, times and revision; visual review, prompt alignment and product truth still require review."}
    # Metadata stays in memory; the delivery directory contains upload PNGs only.
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--font")
    parser.add_argument("--columns", type=int, choices=[3], default=3)
    parser.add_argument("--grid-page-size", type=int, choices=[9], default=9)
    parser.add_argument("--table-page-size", type=int, default=3)
    parser.add_argument("--reference-image-count", type=int, default=1,
                        help="Count all planned product/scene/anchor images besides rendered boards")
    args = parser.parse_args()
    try:
        result = build(args.plan, args.output_dir, font=args.font, columns=args.columns,
                       grid_page_size=args.grid_page_size, table_page_size=args.table_page_size,
                       reference_image_count=args.reference_image_count)
    except (ValueError, OSError, Image.DecompressionBombError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"output_dir": str(args.output_dir), "pages": [page["file"] for page in result["pages"]]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
