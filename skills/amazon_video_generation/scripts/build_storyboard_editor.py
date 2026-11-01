"""Build a standalone, offline storyboard review/editor from actual images.

Edits export as revision-bound requests. This tool never generates/edits product
pixels or writes changes back to the source plan. Python 3.10+, Pillow.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import math
from pathlib import Path
import re

from PIL import Image, ImageOps


def local_file(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError("Image paths must be nonempty project-relative paths")
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"Missing or outside-project image: {value}")
    return path


def positive(value, name):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite")
    return float(value)


def embed_image(path: Path, region=None) -> str:
    with Image.open(path) as source:
        im = ImageOps.exif_transpose(source).convert("RGB")
        if region is not None:
            if not isinstance(region, list) or len(region) != 4 or any(type(v) is not int for v in region):
                raise ValueError("region_px must be integer [x,y,width,height]")
            x, y, w, h = region
            if min(x, y) < 0 or min(w, h) <= 0 or x + w > im.width or y + h > im.height:
                raise ValueError("Panel region is outside the actual board")
            # Read-only review thumbnail; not a clean generation reference.
            im = im.crop((x, y, x + w, y + h))
        im.thumbnail((1920, 1920) if region is None else (960, 960))
        buffer = io.BytesIO()
        im.save(buffer, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def build_payload(plan_path: Path) -> dict:
    raw = plan_path.read_bytes()
    plan = json.loads(raw.decode("utf-8-sig"))
    root = plan_path.parent
    shots = plan.get("shots")
    if not isinstance(shots, list) or not shots:
        raise ValueError("A nonempty shots list is required")
    revision = plan.get("revision")
    if not isinstance(revision, str) or not revision.strip():
        raise ValueError("A nonempty revision is required")
    clips = plan.get("clips")
    if not isinstance(clips, list) or not clips:
        raise ValueError("Explicit clips with id and duration_s are required")
    expected, clip_ranges, cursor = {}, {}, 0.0
    for clip in clips:
        cid = clip.get("id")
        if not isinstance(cid, str) or not re.fullmatch(r"C\d+", cid) or cid in expected:
            raise ValueError("Clip IDs must be unique C-number strings")
        duration = positive(clip.get("duration_s"), f"{cid} duration")
        expected[cid] = duration
        clip_ranges[cid] = (cursor, cursor + duration)
        cursor += duration
    total = positive(plan.get("total_duration_s"), "total_duration_s")
    if abs(cursor - total) > .001:
        raise ValueError("Clip durations do not sum to the total")
    if plan.get("delivery_mode") == "connected-clips" and plan.get("default_contract", True):
        if list(expected) != ["C01", "C02", "C03"] or any(abs(v - 15) > .001 for v in expected.values()):
            raise ValueError("Default connected-clips contract requires C01/C02/C03 at 15s each; use default_contract:false for explicit overrides")
    board = plan.get("board")
    board_path = local_file(root, board["file"]) if board else None
    selected, seen, cursor, image_hashes = [], set(), 0.0, {}
    for shot in shots:
        sid = shot.get("id")
        if not isinstance(sid, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*", sid) or sid in seen:
            raise ValueError("Shot IDs must be unique stable identifiers")
        seen.add(sid)
        start = shot.get("start_s")
        if isinstance(start, bool) or not isinstance(start, (int, float)) or not math.isfinite(start) or abs(start - cursor) > .001:
            raise ValueError(f"{sid}: shots must be ordered and continuous from zero")
        duration = positive(shot.get("duration_s"), f"{sid} duration")
        cid = shot.get("clip_id")
        if cid not in clip_ranges:
            raise ValueError(f"{sid}: unknown clip_id")
        lo, hi = clip_ranges[cid]
        if start < lo - .001 or start + duration > hi + .001:
            raise ValueError(f"{sid}: crosses a clip boundary")
        frames = shot.get("frames", [])
        if frames:
            frame_path = local_file(root, frames[0]["file"])
            thumbnail = embed_image(frame_path)
            image_hashes[frame_path.relative_to(root.resolve()).as_posix()] = hashlib.sha256(frame_path.read_bytes()).hexdigest()
        elif board_path and "region_px" in shot:
            thumbnail = embed_image(board_path, shot["region_px"])
        elif board_path:
            thumbnail = None  # Full board remains visible; never invent a panel mapping.
        else:
            raise ValueError(f"{sid}: an actual frame or actual board is required")
        caption = shot.get("caption", {})
        if not isinstance(caption, dict):
            raise ValueError("caption must be an object")
        fields = {key: caption.get(key, "") for key in ("purpose", "action", "camera", "notes")}
        fields["scene_id"] = shot.get("scene_id", "")
        if any(not isinstance(v, str) for v in fields.values()):
            raise ValueError("Editable fields must be strings")
        selected.append({"id": sid, "clip_id": cid, "start_s": start, "local_start_s": start-lo,
                         "duration_s": duration, "fields": fields, "image": thumbnail,
                         "status": shot.get("status", "not-reviewed")})
        cursor += duration
    if abs(cursor - total) > .001:
        raise ValueError("Shot durations do not sum to the total")
    if board_path:
        image_hashes[board["file"]] = hashlib.sha256(board_path.read_bytes()).hexdigest()
    return {"schema_version": 1, "title": str(plan.get("title", "故事板审阅")),
            "revision": revision, "plan_sha256": hashlib.sha256(raw).hexdigest(),
            "image_hashes": image_hashes, "total_duration_s": total, "clips": clips,
            "identity_lock": plan.get("identity_lock", "商品事实以原始参考和brief为准"),
            "board": embed_image(board_path) if board_path else None,
            "shots": selected, "source_note": str(plan.get("source_note", "项目故事板；生成图不作为商品事实证据"))}


def build_editor(plan_path: Path, output: Path):
    plan_path, output = plan_path.resolve(), output.resolve()
    if output.exists():
        raise ValueError("Output already exists; choose a new version")
    payload = build_payload(plan_path)
    template = Path(__file__).resolve().parent / "templates/storyboard-editor.html"
    data = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    html = template.read_text(encoding="utf-8").replace("__STORYBOARD_DATA__", data)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        print(build_editor(args.plan, args.output))
    except (ValueError, KeyError, OSError, TypeError) as exc:
        parser.exit(2, f"Cannot build editor: {exc}\n")
