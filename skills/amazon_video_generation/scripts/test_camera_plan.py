#!/usr/bin/env python3
"""Tests for check_camera_plan.py."""

from __future__ import annotations

import sys
import io
import contextlib
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_camera_plan import check_rows, parse_table, main  # noqa: E402


GOOD_CSV = """镜号,片段,出镜时长,运镜方式与起终点
S01,C01,10,M00→M01：0-3s起幅静止；3-10s沿光轴缓推至局部近景，最后停稳
S02,C02,5,M03：从左向右横移；起点P3侧前，终点P2，最后停稳
S03,C02,5,M00：切镜后固定展示完整体量；起幅即完整构图，停稳
S04,C03,5,M00：固定观察盆壁纹理；起幅对焦，停稳
S05,C03,5,M10：焦点从前排移到后排；起幅前排清楚，终点后排清楚停稳
S06,C04,10,M00：固定机位，右侧商品左侧留白；起幅即终帧，全程无旋转
"""


def run(text: str, strict: bool = False):
    header, rows = parse_table(text)
    return check_rows(header, rows, strict=strict)


def errors(findings):
    return [item for item in findings if item.level == "ERROR"]


def warnings(findings):
    return [item for item in findings if item.level == "WARN"]


class ParseTests(unittest.TestCase):
    def test_csv_header(self):
        header, rows = parse_table(GOOD_CSV)
        self.assertEqual(header[0], "镜号")
        self.assertEqual(len(rows), 6)
        self.assertEqual(rows[0][1], "C01")

    def test_markdown_table_skips_separator(self):
        text = """| 镜号 | 片段 | 运镜方式与起终点 |
| --- | --- | --- |
| S01 | C01 | M01 缓推，起幅中景，终点近景停稳 |
"""
        header, rows = parse_table(text)
        self.assertEqual(header, ["镜号", "片段", "运镜方式与起终点"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "S01")


class RuleTests(unittest.TestCase):
    def test_good_plan_has_no_errors(self):
        self.assertEqual(errors(run(GOOD_CSV)), [])

    def test_missing_move_column(self):
        findings = run("镜号,片段\nS01,C01\n")
        self.assertTrue(any("找不到“运镜”列" in f.message for f in errors(findings)))

    def test_empty_move_cell(self):
        findings = run("镜号,片段,运镜方式与起终点\nS01,C01,\n")
        self.assertTrue(any("运镜栏为空" in f.message for f in errors(findings)))

    def test_two_primary_moves(self):
        text = "镜号,片段,运镜方式与起终点\nS02,C02,M04 短弧环绕；M05 升降；起点正面，终点停稳\n"
        found = errors(run(text))
        self.assertTrue(any("多个主要运动" in f.message for f in found))

    def test_compensation_is_not_primary(self):
        text = "镜号,片段,运镜方式与起终点\nS02,C02,M01 缓推；轻微俯仰补偿保持构图；起幅中景，终点近景停稳\n"
        self.assertEqual(errors(run(text)), [])

    def test_first_shot_allows_project_orbit(self):
        text = "镜号,片段,运镜方式与起终点\nS01,C01,M04 短弧环绕；起幅正面，终点侧前停稳\nS02,C02,M00 固定；起幅，停稳\n"
        found = errors(run(text))
        self.assertEqual(found, [])

    def test_last_clip_allows_orbit(self):
        text = "镜号,片段,运镜方式与起终点\nS01,C01,M00 固定；起幅，停稳\nS06,C04,M04 短弧环绕；起幅右侧，终点停稳\n"
        found = errors(run(text))
        self.assertEqual(found, [])

    def test_last_segment_allows_pullback(self):
        text = "镜号,片段,运镜方式与起终点\nS01,C01,M00 固定；起幅，停稳\nS04,C03,M02 后拉；起幅近景，终点中景停稳\n"
        found = errors(run(text))
        self.assertEqual(found, [])

    def test_c04_negated_words_pass(self):
        text = "镜号,片段,运镜方式与起终点\nS06,C04,M00 固定；全程无旋转、无横移；起幅即终帧，停稳\n"
        self.assertEqual(errors(run(text)), [])

    def test_unknown_id(self):
        text = "镜号,片段,运镜方式与起终点\nS02,C02,M99 神秘运镜；起点，终点停稳\n"
        found = errors(run(text))
        self.assertTrue(any("未知运镜编号 M99" in f.message for f in found))

    def test_combo_allowed(self):
        text = "镜号,片段,运镜方式与起终点\nS02,C02,K01 推→停→拉；起幅中景，终点中景停稳\n"
        self.assertEqual(errors(run(text)), [])

    def test_two_combos_rejected(self):
        text = "镜号,片段,运镜方式与起终点\nS02,C02,K01 推→停→拉；K03 横移+微升；起幅，终点停稳\n"
        found = errors(run(text))
        self.assertTrue(any("只能用一个 K 类组合" in f.message for f in found))

    def test_alternatives_only_warn(self):
        text = "镜号,片段,运镜方式与起终点\nS02,C02,M03 或 M08；起点，终点停稳\n"
        findings = run(text)
        self.assertEqual(errors(findings), [])
        self.assertTrue(any("候选未定" in f.message for f in warnings(findings)))

    def test_vague_words_warn_when_no_id(self):
        text = "镜号,片段,运镜方式与起终点\nS02,C02,电影感运镜缓缓推进\n"
        findings = run(text)
        self.assertEqual(errors(findings), [])
        self.assertTrue(any("不是可执行描述" in f.message for f in warnings(findings)))

    def test_double_orbit_ambiguity_warns(self):
        text = "镜号,片段,运镜方式与起终点\nS02,C02,M04 两倍环绕；起幅正面，终点侧前停稳\n"
        self.assertTrue(any("含义未定" in f.message for f in warnings(run(text))))

    def test_missing_terminal_hint_warns(self):
        text = "镜号,片段,运镜方式与起终点\nS02,C02,M03 横移\n"
        self.assertTrue(any("未写起幅" in f.message for f in warnings(run(text))))

    def test_duration_out_of_range(self):
        text = "镜号,片段,出镜时长,运镜方式与起终点\nS01,C01,16,M01 缓推；起幅，终点停稳\n"
        self.assertTrue(any("超出单镜上限" in f.message for f in errors(run(text))))

    def test_fifteen_second_shot_passes(self):
        text = "镜号,片段,出镜时长,运镜方式与起终点\nS01,C01,15,M00→M01 缓推；起幅静止，终点停稳\n"
        self.assertEqual(errors(run(text)), [])

    def test_fifteen_second_clip_passes(self):
        text = "镜号,片段,出镜时长,运镜方式与起终点\nS02,C02,8,M02 后拉；起幅近景，终点中景停稳\nS03,C02,7,M00 切镜固定；起幅即构图，停稳\n"
        findings = run(text)
        self.assertEqual(errors(findings), [])
        self.assertFalse(any("合计" in f.message for f in warnings(findings)))

    def test_clip_total_warns(self):
        text = "镜号,片段,出镜时长,运镜方式与起终点\nS02,C02,8,M03 横移；起幅，终点停稳\nS03,C02,8,M00 固定；起幅，停稳\n"
        self.assertTrue(any("合计 16s" in f.message for f in warnings(run(text))))

    def test_strict_promotes_warnings(self):
        text = "镜号,片段,运镜方式与起终点\nS02,C02,M03 横移\n"
        findings = run(text, strict=True)
        self.assertTrue(any(f.level == "ERROR" for f in findings))


class DirectionTests(unittest.TestCase):
    FLOWER = """镜号,片段,出镜时长,运镜方式与起终点
S01,C01,5,M04 短弧环绕；起幅完整花卉，终点侧前停稳
S02,C01,8,M00 固定插花；起幅手握枝，终点插入落稳
S03,C01,2,M00 完成态；起幅到终点固定
"""

    def check(self, text, profile, flower_format="F01"):
        header, rows = parse_table(text)
        return check_rows(header, rows, strict=True, profile=profile, flower_format=flower_format)

    def test_flower_one_task_three_shots(self):
        self.assertEqual(errors(self.check(self.FLOWER, "flowers")), [])

    def test_same_orbit_allowed_for_foliage(self):
        self.assertEqual(errors(self.check(self.FLOWER, "foliage")), [])

    def test_flower_first_five_seconds(self):
        changed = self.FLOWER.replace("C01,5,M04", "C01,4,M04")
        self.assertTrue(any("前5秒" in f.message for f in self.check(changed, "flowers")))

    def test_flower_no_automatic_closing_card(self):
        two_tasks = self.FLOWER.replace("S02,C01", "S02,C02").replace("S03,C01", "S03,C02")
        self.assertEqual(errors(self.check(two_tasks, "flowers")), [])

    def test_flower_push_does_not_replace_orbit(self):
        self.assertTrue(errors(self.check(self.FLOWER.replace("M04", "M01"), "flowers")))

    def test_total_budget_in_foliage_and_legacy(self):
        self.assertTrue(any("30秒" in f.message for f in self.check(GOOD_CSV, "foliage")))
        self.assertEqual(errors(self.check(GOOD_CSV, "legacy")), [])

    def test_flower_cannot_overrun_thirty_seconds(self):
        extra = self.FLOWER + "S04,C02,10,M00 固定；起幅，终点停稳\nS05,C03,10,M00 固定；起幅，终点停稳\n"
        self.assertTrue(any("30秒" in f.message for f in self.check(extra, "flowers")))

    def test_nan_cannot_bypass_budget(self):
        for value in ["nan", "inf", "未定"]:
            self.assertTrue(any("有限数字" in f.message for f in self.check(self.FLOWER.replace("C01,8,", f"C01,{value},"), "flowers")))

    def test_no_action_budget(self):
        text = "\n".join(self.FLOWER.splitlines()[:2])
        self.assertTrue(any("没有后续插花" in f.message for f in self.check(text, "flowers")))

    def test_alternative_formats_allow_short_non_orbit_display(self):
        text = "镜号,片段,出镜时长,运镜方式与起终点\nS01,C01,4,M01 慢推；起幅全貌，终点停稳\n"
        for flower_format in ["F02", "F03", "F04", "F05", "F06", "F07"]:
            with self.subTest(flower_format=flower_format):
                self.assertEqual(errors(self.check(text, "flowers", flower_format)), [])
        self.assertTrue(errors(self.check(text, "flowers", "F01")))

    def test_alternative_format_keeps_total_and_clip_budgets(self):
        self.assertTrue(any("30秒" in f.message for f in self.check(GOOD_CSV, "flowers", "F02")))
        text = self.FLOWER.replace("M04", "M01").replace("C01,8,", "C01,9,")
        self.assertTrue(any("该段合计 16s" in f.message for f in self.check(text, "flowers", "F02")))

    def test_alternative_format_keeps_motion_validation(self):
        text = self.FLOWER.replace("M04", "M01 慢推；M03 横移")
        self.assertTrue(any("多个主要运动" in f.message for f in self.check(text, "flowers", "F02")))

    def test_unknown_flower_format_rejected(self):
        with self.assertRaises(ValueError):
            self.check(self.FLOWER, "flowers", "F99")

    def test_f07_keeps_budget_and_motion_constraints(self):
        plan = """镜号,片段,出镜时长,运镜方式与起终点
S01,C01,4,M01 慢推；起幅完整商品，终点停稳
S02,C01,6,M00 人物放置；起幅已托稳，终点松手停稳
S03,C02,5,M00 第二场景陈列；起幅全貌，终点固定
"""
        self.assertEqual(errors(self.check(plan, "flowers", "F07")), [])
        extra = plan + "S04,C03,10,M00 固定；起幅，终点停稳\nS05,C04,10,M00 固定；起幅，终点停稳\n"
        self.assertTrue(any("30秒" in f.message for f in self.check(extra, "flowers", "F07")))
        conflicting = plan.replace("M01 慢推", "M01 慢推；M03 横移")
        self.assertTrue(any("多个主要运动" in f.message for f in self.check(conflicting, "flowers", "F07")))

    def test_generated_length_distinct_from_retained_length(self):
        text = "镜号,片段,出镜时长,生成任务长度,运镜方式与起终点\nS01,C01,2,5,M00 固定；起幅全貌，终点停稳\n"
        self.assertEqual(errors(self.check(text, "flowers", "F02")), [])
        self.assertTrue(errors(self.check(text.replace(",2,5,", ",2,16,"), "flowers", "F02")))

    def test_around_thirty_seconds_is_not_a_hard_total_limit(self):
        text = "镜号,片段,出镜时长,运镜方式与起终点\n" + "".join(f"S{i:02},C{i:02},8,M00 固定；起幅全貌，终点停稳\n" for i in range(1,5))
        self.assertEqual(errors(self.check(text, "flowers", "F02")), [])


class FullFilmCapacityTests(unittest.TestCase):
    def check(self, text, capacity):
        header, rows = parse_table(text)
        return check_rows(header, rows, strict=True, profile="flowers", flower_format="F07", max_generation_seconds=capacity)

    def test_whole_film_uses_selected_capacity(self):
        text = "镜号,片段,出镜时长,生成任务长度,运镜方式与起终点\n" + "".join(
            f"S{i:02},C01,5,30,M00 固定；起幅全貌，终点停稳\n" for i in range(1, 7))
        self.assertEqual(errors(self.check(text, 30)), [])
        self.assertTrue(errors(self.check(text, 15)))

    def test_two_parts_fit_mini(self):
        text = "镜号,片段,出镜时长,生成任务长度,运镜方式与起终点\n" + "".join(
            f"S{i:02},C{1 if i <= 3 else 2:02},5,15,M00 固定；起幅全貌，终点停稳\n" for i in range(1, 7))
        self.assertEqual(errors(self.check(text, 15)), [])

    def test_invalid_capacity_rejected(self):
        for value in [0, -1, float("nan"), float("inf"), True]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.check(GOOD_CSV, value)

    def test_retained_length_still_cannot_exceed_generated(self):
        text = "镜号,片段,出镜时长,生成任务长度,运镜方式与起终点\nS01,C01,16,15,M00 固定；起幅全貌，终点停稳\n"
        self.assertTrue(errors(self.check(text, 30)))

    def test_long_continuous_shot_supported_only_when_capacity_allows(self):
        text = "镜号,片段,出镜时长,生成任务长度,运镜方式与起终点\nS01,C01,30,30,M04 环绕；起幅正面，终点侧面停稳\n"
        self.assertEqual(errors(self.check(text, 30)), [])
        self.assertTrue(errors(self.check(text, 15)))


class GeneralProductTests(unittest.TestCase):
    PLAN = "镜号,片段,出镜时长,生成任务长度,运镜方式与起终点\nS01,C01,4,8,M00：固定近景；起态完整灯体；灯头转动后停稳\nS02,C01,4,8,M03：从正前起幅横移至右前终点停稳\n"

    def test_generic_mechanism_has_no_botanical_opening_requirement(self):
        header, rows = parse_table(self.PLAN)
        self.assertEqual(errors(check_rows(header, rows, strict=True, profile="general")), [])
        self.assertTrue(errors(check_rows(header, rows, strict=True, profile="flowers", flower_format="F01")))

    def test_general_still_rejects_generation_over_actual_limit(self):
        header, rows = parse_table(self.PLAN.replace(",8,", ",16,"))
        self.assertTrue(errors(check_rows(header, rows, strict=True, profile="general", max_generation_seconds=15)))

    def test_cli_default_accepts_general_product(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "shot-list.csv"
            path.write_text(self.PLAN, encoding="utf-8-sig")
            with contextlib.redirect_stdout(io.StringIO()):
                result = main([str(path), "--strict"])
            self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
