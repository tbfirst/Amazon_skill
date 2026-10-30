"""Validate a local campaign manifest and compile exact prompt text into MD/TXT.

Usage: python build_prompt_summary.py PROJECT_DIRECTORY
No browsing, generation, claim validation or external writes.
"""

import json
import re
import sys
from pathlib import Path


DEFAULT_IDS = ["DIM01", "DETAIL01"] + [f"SCENE{i:02}" for i in range(1, 5)] + [
    f"APLUS{i:02}" for i in range(1, 6)
]
STATUSES = {"READY", "PROVISIONAL", "BLOCKED"}
REVIEW_STATES = {"verified", "pending", "not-applicable"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def string_list(value, label):
    require(isinstance(value, list) and all(nonempty(x) for x in value),
            f"{label}: expected a list of nonempty strings")
    return value


def read_exact(path):
    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


def load_campaign(project):
    project = project.resolve()
    manifest = json.loads(read_exact(project / "prompt-manifest.json"))
    require(isinstance(manifest, dict), "manifest must be an object")
    require(manifest.get("schemaVersion") == 1, "schemaVersion must be 1")
    mode = manifest.get("campaignMode")
    require(mode in {"new-set", "set-refresh"}, "unknown campaignMode")
    ids = string_list(manifest.get("targetAssetIds"), "targetAssetIds")
    require(ids and len(ids) == len(set(ids)), "targetAssetIds must be nonempty and unique")
    require(all(re.fullmatch(r"[A-Z][A-Z0-9_-]{1,31}", x) for x in ids), "invalid asset ID")
    if mode == "new-set" and ids != DEFAULT_IDS:
        require(nonempty(manifest.get("scopeOverrideReason")),
                "new-set must use the default 11 IDs or document the explicit scope override")
    assets = manifest.get("assets")
    require(isinstance(assets, list) and all(isinstance(a, dict) for a in assets),
            "assets must be a list of objects")
    asset_ids = [a.get("id") for a in assets]
    require(all(isinstance(x, str) for x in asset_ids), "every asset needs an ID")
    require(len(asset_ids) == len(set(asset_ids)), "duplicate asset ID")
    require(set(asset_ids) == set(ids), "assets do not match targetAssetIds")
    by_id = {a["id"]: a for a in assets}
    used_files = set()
    result = []
    for asset_id in ids:
        a = by_id[asset_id]
        status = a.get("status")
        require(status in STATUSES, f"{asset_id}: invalid status")
        conditions = string_list(a.get("conditions"), f"{asset_id}.conditions")
        gaps = string_list(a.get("gaps"), f"{asset_id}.gaps")
        require(status != "PROVISIONAL" or conditions, f"{asset_id}: PROVISIONAL needs conditions")
        require(status != "BLOCKED" or gaps, f"{asset_id}: BLOCKED needs gaps")
        require(status == "BLOCKED" or not gaps, f"{asset_id}: executable asset cannot retain gaps")
        require(status != "READY" or not conditions, f"{asset_id}: READY cannot retain conditions")
        for key in ("policyReview", "uploadReview"):
            require(a.get(key) in REVIEW_STATES, f"{asset_id}: invalid {key}")
            require(status != "READY" or a[key] != "pending", f"{asset_id}: pending {key} cannot be READY")
        canvas = a.get("canvas", {})
        require(isinstance(canvas, dict), f"{asset_id}: canvas must be an object")
        require(all(type(canvas.get(k)) is int and canvas[k] > 0 for k in ("width", "height")),
                f"{asset_id}: canvas needs positive integer width/height")
        if asset_id.startswith("SCENE") and canvas["width"] != canvas["height"]:
            require(nonempty(a.get("canvasOverrideReason")), f"{asset_id}: non-square SCENE needs explicit override")
        relative = a.get("file")
        require(nonempty(relative) and not Path(relative).is_absolute(), f"{asset_id}: prompt path must be relative")
        path = (project / relative).resolve()
        prompt_root = (project / "prompts").resolve()
        blocked_root = (project / "prompts" / "blocked").resolve()
        require(path.is_relative_to(project) and path.is_relative_to(prompt_root),
                f"{asset_id}: prompt must stay inside project/prompts")
        require(path.suffix.lower() == ".txt", f"{asset_id}: prompt must be TXT")
        require(path.is_relative_to(blocked_root) == (status == "BLOCKED"),
                f"{asset_id}: blocked/executable prompt path mismatch")
        require(path not in used_files, f"{asset_id}: prompt file reused")
        used_files.add(path)
        require(path.is_file(), f"{asset_id}: prompt file missing: {relative}")
        body = read_exact(path)
        require(nonempty(body), f"{asset_id}: prompt is empty")
        refs = a.get("references")
        require(isinstance(refs, list), f"{asset_id}: references must be an ordered list")
        seen_names = set()
        for ref in refs:
            require(isinstance(ref, dict) and all(nonempty(ref.get(k)) for k in ("filename", "role", "path")),
                    f"{asset_id}: reference needs filename, role, path")
            require(ref["filename"] not in seen_names, f"{asset_id}: ambiguous duplicate reference filename")
            seen_names.add(ref["filename"])
            ref_path = Path(ref["path"])
            if not ref_path.is_absolute():
                ref_path = project / ref_path
            require(ref_path.is_file(), f"{asset_id}: reference file missing: {ref['filename']}")
        if status != "BLOCKED":
            require(any(r["role"] == "identity" for r in refs), f"{asset_id}: executable prompt needs identity input")
        result.append((a, body))
    return result


def compile_campaign(project):
    project = Path(project).resolve()
    records = load_campaign(project)  # Validate every asset before touching either output.
    intro = "Upload each asset's references in the listed order before copying its prompt.\n"
    md = ["# Complete prompts\n\n", intro, "\n"]
    txt = ["COMPLETE PROMPTS\n\n", intro, "\n"]
    for a, body in records:
        label = f"{a['id']} — {a['status']}"
        md.append(f"## {label}\n\n")
        txt.append(f"=== {label} ===\n")
        if a["status"] == "BLOCKED":
            missing = "Missing: " + "; ".join(a["gaps"]) + "\n\n"
            md.append(missing)
            txt.append(missing)
            continue
        canvas = a["canvas"]
        meta = f"Canvas: {canvas['width']} × {canvas['height']} px\n"
        meta += "Upload order:\n"
        for index, ref in enumerate(a["references"], 1):
            meta += f"{index}. {ref['filename']} — {ref['role']}\n"
        if a["conditions"]:
            meta += "Conditions: " + "; ".join(a["conditions"]) + "\n"
        md.extend([meta, "\n"])
        txt.extend([meta, "\nBEGIN PROMPT\n", body, "\nEND PROMPT\n\n"])
        longest = max((len(m.group()) for m in re.finditer(r"`+", body)), default=0)
        fence = "`" * max(3, longest + 1)
        md.extend([fence + "text\n", body, "\n" + fence + "\n\n"])
    outputs = {"all-prompts.md": "".join(md), "all-prompts.txt": "".join(txt)}
    for name, contents in outputs.items():
        with (project / name).open("w", encoding="utf-8", newline="") as stream:
            stream.write(contents)
    counts = {s: sum(a["status"] == s for a, _ in records) for s in sorted(STATUSES)}
    print(json.dumps({"assets": len(records), "counts": counts, "outputs": list(outputs)}, ensure_ascii=False))
    return outputs


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python build_prompt_summary.py PROJECT_DIRECTORY")
    try:
        compile_campaign(sys.argv[1])
    except (ValueError, OSError) as exc:
        sys.exit(f"ERROR: {exc}")
