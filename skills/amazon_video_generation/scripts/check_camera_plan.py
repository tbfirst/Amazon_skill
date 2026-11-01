#!/usr/bin/env python3
"""Check camera/length structure by direction, not product truth or footage quality.

CLI: check_camera_plan.py shot-list.csv --profile flowers --strict
general: product-specific camera/actions, with no botanical opening requirement.
flowers: F01 defaults to a 5s orbit; F02-F07 use the selected structure; total <=30s.
foliage: project-selected camera movements; total <=30s.
Generation capacity is supplied by --max-generation-seconds, not inferred from a model name.
legacy: earlier length budget for existing projects; no positional camera restrictions.
"""

from __future__ import annotations

import argparse
import csv
import io
import math
import re
import sys
from pathlib import Path

MOVES = {
    "M00": "固定",
    "M01": "慢推",
    "M02": "慢拉",
    "M03": "横移",
    "M04": "短弧环绕",
    "M05": "升降",
    "M06": "俯仰",
    "M07": "水平摇",
    "M08": "遮挡上升",
    "M09": "前景掠过",
    "M10": "转焦",
    "M11": "跟随",
    "M12": "甩镜",
    "M13": "滚转",
    "M14": "变焦",
    "M15": "推拉变焦",
    "M16": "手持",
    "M17": "贴面掠移",
    "M18": "完整环绕",
    "M19": "主体自转",
}

COMBOS = {
    "K01": "推→停→拉",
    "K02": "环绕+推进",
    "K03": "横移+微升",
    "K04": "推进+前景遮挡",
    "K05": "环绕+后拉",
    "K06": "升降+俯仰补偿",
}

STAGED_ALLOWED = {"M00", "M01"}
MAX_SHOT_S = 15
MIN_CLIP_S = 4
MAX_CLIP_S = 15
VAGUE_WORDS = ("电影感", "大片感", "高级感", "丝滑", "炫技", "氛围感")
COMPENSATION_WORDS = ("补偿", "辅助", "轻微", "保持构图", "跟焦", "为保持")
TERMINAL_HINTS = ("起", "终", "停", "落幅", "起幅")
CLAUSE_SPLIT = re.compile(r"[；;，,、]")
ID_PATTERN = re.compile(r"([MK])(\d{2})(?!\d)")
SEGMENT_PATTERN = re.compile(r"C(\d{2})(?!\d)")
NEGATIONS = ("无", "不", "禁", "勿", "非")


class Finding:
    __slots__ = ("level", "shot", "message")

    def __init__(self, level: str, shot: str, message: str) -> None:
        self.level = level
        self.shot = shot
        self.message = message

    def render(self) -> str:
        return f"{self.level:<5} {self.shot}: {self.message}"


def ids_in(cell: str) -> list[str]:
    return [f"{prefix}{number}" for prefix, number in ID_PATTERN.findall(cell)]


def compensation_ids(cell: str) -> set[str]:
    found: set[str] = set()
    for clause in CLAUSE_SPLIT.split(cell):
        if any(word in clause for word in COMPENSATION_WORDS):
            found.update(ids_in(clause))
    return found


def negated(cell: str, word: str) -> bool:
    """True when the word is absent, or every occurrence is negated nearby."""
    occurrences = [match.start() for match in re.finditer(re.escape(word), cell)]
    if not occurrences:
        return True
    for start in occurrences:
        window = cell[max(0, start - 3) : start]
        if not any(neg in window for neg in NEGATIONS):
            return False
    return True


def segment_of(cell: str) -> str | None:
    match = SEGMENT_PATTERN.search(cell)
    return f"C{match.group(1)}" if match else None


def find_column(header: list[str], *keywords: str) -> int | None:
    for index, name in enumerate(header):
        if any(keyword in name for keyword in keywords):
            return index
    return None


def parse_table(text: str) -> tuple[list[str], list[list[str]]]:
    """Parse a CSV or a Markdown pipe table into header + rows."""
    stripped = text.lstrip()
    if stripped.startswith("|"):
        header: list[str] = []
        rows: list[list[str]] = []
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells if cell):
                continue
            if not header:
                header = cells
            else:
                rows.append(cells)
        return header, rows

    reader = csv.reader(io.StringIO(text))
    raw = [row for row in reader if any(cell.strip() for cell in row)]
    if not raw:
        return [], []
    return raw[0], raw[1:]


def check_rows(header: list[str], rows: list[list[str]], strict: bool = False, profile: str = "legacy", flower_format: str = "F01", max_generation_seconds: float = 15) -> list[Finding]:
    if (type(max_generation_seconds) not in (int, float)
            or not math.isfinite(max_generation_seconds) or max_generation_seconds <= 0):
        raise ValueError("max_generation_seconds must be a positive finite number")
    if profile not in {"general", "flowers", "foliage", "legacy"}:
        raise ValueError(f"Unknown profile: {profile}")
    if flower_format not in {"F01", "F02", "F03", "F04", "F05", "F06", "F07"}:
        raise ValueError(f"Unknown flower format: {flower_format}")
    is_f01 = profile == "flowers" and flower_format == "F01"
    findings: list[Finding] = []

    shot_col = find_column(header, "镜号", "S-ID", "shot")
    clip_col = find_column(header, "片段", "C-ID", "clip")
    move_col = find_column(header, "运镜", "camera")
    duration_col = find_column(header, "出镜时长", "时长", "duration")
    generation_col = find_column(header, "生成任务长度", "generation_duration")
    generated: dict[str, float] = {}

    if move_col is None:
        return [Finding("ERROR", "-", "找不到“运镜”列，无法检查")]

    durations: dict[str, float] = {}
    total_duration = 0.0
    valid_durations = 0
    if profile != "legacy" and duration_col is None:
        findings.append(Finding("ERROR", "-", "缺少出镜时长列，不能核对30秒预算"))

    order: list[str] = []
    for row in rows:
        clip_cell = row[clip_col] if clip_col is not None and clip_col < len(row) else ""
        move_cell = row[move_col] if move_col is not None and move_col < len(row) else ""
        found_seg = segment_of(clip_cell) or segment_of(move_cell)
        if found_seg and found_seg not in order:
            order.append(found_seg)
    first_seg = order[0] if order else None
    last_seg = order[-1] if order else None

    for index, row in enumerate(rows, start=1):
        def cell(col: int | None) -> str:
            if col is None or col >= len(row):
                return ""
            return row[col].strip()

        shot = cell(shot_col) or f"row{index}"
        movement = cell(move_col)
        segment = segment_of(cell(clip_col)) or segment_of(movement)

        if generation_col is not None and segment:
            try:
                generation_length = float(cell(generation_col))
                if not math.isfinite(generation_length) or generation_length <= 0 or generation_length > max_generation_seconds:
                    raise ValueError
                if segment in generated and generated[segment] != generation_length:
                    findings.append(Finding("ERROR", shot, "同C-ID生成任务长度不一致"))
                generated[segment] = generation_length
            except ValueError:
                findings.append(Finding("ERROR", shot, f"生成任务长度须为0到{max_generation_seconds:g}秒之间的有限正数；入口能力须另核"))

        if not movement:
            findings.append(Finding("ERROR", shot, "运镜栏为空，未说明镜头怎么动"))
            continue

        found = ids_in(movement)
        unknown = [item for item in found if item not in MOVES and item not in COMBOS]
        for item in unknown:
            findings.append(Finding("ERROR", shot, f"未知运镜编号 {item}，请对照 M00–M19 / K01–K06"))

        singles = [item for item in found if item in MOVES]
        combos = [item for item in found if item in COMBOS]
        compensation = compensation_ids(movement)
        primary = [item for item in dict.fromkeys(singles) if item not in compensation]

        if not found:
            for word in VAGUE_WORDS:
                if word in movement:
                    findings.append(
                        Finding("WARN", shot, f"“{word}”不是可执行描述，补 M/K 编号、起终点与速度")
                    )
                    break

        if "两倍环绕" in movement and "2×" not in movement and "2x" not in movement:
            findings.append(Finding("WARN", shot, "“两倍环绕”含义未定，先判定 2×取景/两倍速/绕两圈"))

        if is_f01 and index == 1:
            if combos or len(primary) != 1 or primary[0] not in {"M04", "M18"}:
                findings.append(Finding("ERROR", shot, "花卉首镜必须为M04短弧环绕（默认60–90°）或另经选择的M18全周；其他方向按项目选镜"))

        if len(combos) > 1:
            findings.append(Finding("ERROR", shot, "一个镜头只能用一个 K 类组合"))
        if combos and primary:
            findings.append(Finding("WARN", shot, "组合镜里又写了单运动，若不是辅助请标“辅助”或改用 K 编号"))

        staged = "→" in movement or "->" in movement
        if len(primary) > 1:
            if "或" in movement:
                findings.append(Finding("WARN", shot, f"候选未定（{'/'.join(primary)}），交付前需定一条"))
            elif staged and set(primary) <= STAGED_ALLOWED:
                pass
            else:
                findings.append(
                    Finding("ERROR", shot, f"一镜出现多个主要运动（{'、'.join(primary)}），保留一个主路径")
                )

        if found and not any(hint in movement for hint in TERMINAL_HINTS):
            findings.append(Finding("WARN", shot, "未写起幅/终点/停稳，路径无法验收"))

        if duration_col is not None:
            raw_duration = cell(duration_col).replace("s", "").replace("秒", "").strip()
            try:
                value = float(raw_duration)
            except ValueError:
                value = None
            if profile != "legacy" and (value is None or not math.isfinite(value)):
                findings.append(Finding("ERROR", shot, "出镜时长必须为有限数字"))
                value = None
            if value is not None:
                if math.isfinite(value):
                    total_duration += value
                    valid_durations += 1
                if is_f01 and index == 1 and value != 5:
                    findings.append(Finding("ERROR", shot, "花卉前5秒须为完整环绕首镜；调整需求应在计划中明确"))
                if value <= 0 or value > max_generation_seconds:
                    findings.append(Finding("ERROR", shot, f"出镜时长 {value:g}s 超出单镜上限 {max_generation_seconds:g}s"))
                if segment:
                    durations[segment] = durations.get(segment, 0.0) + value

    for segment, retained in sorted(durations.items()):
        total = generated.get(segment, retained)
        if retained > total:
            findings.append(Finding("ERROR", segment, "保留镜长超过生成任务长度"))
        if total <= 0 or total > max_generation_seconds:
            findings.append(
                Finding(
                    "WARN",
                    segment,
                    f"该段合计 {total:g}s，按所填入口单次最长{max_generation_seconds:g}s；入口档位另核",
                )
            )

    if profile != "legacy" and valid_durations == len(rows) and total_duration > 30:
        findings.append(Finding("INFO", "-", f"总时长 {total_duration:g}s：复核约30秒预算的信息增量及版位；不是模型总片硬上限"))
    if is_f01 and valid_durations == len(rows) and total_duration <= 5:
        findings.append(Finding("ERROR", "-", "只有环绕，没有后续插花时间"))

    if strict:
        for finding in findings:
            if finding.level == "WARN":
                finding.level = "ERROR"

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", type=Path, help="shot-list.csv or shot-list.md")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--profile", choices=["general", "flowers", "foliage", "legacy"], default="general", help="direction; legacy preserves pre-v4 contracts")
    parser.add_argument("--flower-format", choices=["F01", "F02", "F03", "F04", "F05", "F06", "F07"], default="F01", help="selected flower structure; F01 preserves the 5s orbit contract; ignored for other profiles")
    parser.add_argument("--max-generation-seconds", type=float, default=15, help="verified capacity of the selected entry; default 15, not a model-wide claim")
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_generation_seconds) or args.max_generation_seconds <= 0:
        parser.error("--max-generation-seconds must be a positive finite number")

    try:
        text = args.path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        print(f"ERROR 无法读取 {args.path}: {exc}", file=sys.stderr)
        return 2

    header, rows = parse_table(text)
    if not header:
        print("ERROR 文件里没有可识别的表格", file=sys.stderr)
        return 2

    findings = check_rows(header, rows, strict=args.strict, profile=args.profile, flower_format=args.flower_format, max_generation_seconds=args.max_generation_seconds)
    errors = sum(1 for finding in findings if finding.level == "ERROR")
    warnings = len(findings) - errors

    for finding in findings:
        print(finding.render())

    print(f"\n{len(rows)} 个镜头：{errors} error / {warnings} warning")
    if errors:
        print("结构未通过。结构检查不涉及画面质量与生成结果。")
        return 1
    print("结构通过。仍需按执行卡验收成片运动与商品保真。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
