"""Exercise timeline validation and actual image layout with synthetic color tiles.

These fixtures test the helper; they are not product storyboard deliverables.
Run: python -m unittest discover -s scripts -p 'test_*.py'
"""

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from assemble_storyboard import assemble, choose_font, load_plan, wrap_text


class StoryboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "frames").mkdir()
        Image.new("RGB", (160, 90), "red").save(self.root / "frames/a.png")
        Image.new("RGB", (160, 90), "blue").save(self.root / "frames/b.png")
        self.data = {
            "title": "Test board",
            "aspect_ratio": "16:9",
            "total_duration_s": 8,
            "shots": [
                {"id": "S01", "start_s": 0, "duration_s": 4,
                 "frames": [{"state": "key", "file": "frames/a.png"}]},
                {"id": "S02", "start_s": 4, "duration_s": 4,
                 "frames": [{"state": "key", "file": "frames/b.png"}]},
            ],
        }
        self.plan = self.root / "video-plan.json"
        self.output = self.root / "board.png"
        self.write()

    def write(self, data=None):
        self.plan.write_text(json.dumps(self.data if data is None else data), encoding="utf-8")

    def test_load_valid_timeline_and_frames(self):
        title, aspect, panels = load_plan(self.plan)
        self.assertEqual((title, aspect), ("Test board", (16, 9)))
        self.assertEqual([p.shot_id for p in panels], ["S01", "S02"])
        self.assertEqual(panels[-1].start_s + panels[-1].duration_s, 8)

    def test_gap_overlap_and_nonzero_start_rejected(self):
        for index, start in ((0, 1), (1, 3.8), (1, 4.2)):
            with self.subTest(index=index, start=start):
                data = copy.deepcopy(self.data)
                data["shots"][index]["start_s"] = start
                self.write(data)
                with self.assertRaisesRegex(ValueError, "non-contiguous"):
                    load_plan(self.plan)

    def test_total_duration_must_match(self):
        self.data["total_duration_s"] = 9
        self.write()
        with self.assertRaisesRegex(ValueError, "totals"):
            load_plan(self.plan)

    def test_invalid_duration_numbers_rejected(self):
        for value in (True, 0, -1, float("nan"), float("inf"), "4"):
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data["shots"][0]["duration_s"] = value
                self.write(data)
                with self.assertRaises(ValueError):
                    load_plan(self.plan)

    def test_duplicate_shot_id_rejected(self):
        self.data["shots"][1]["id"] = "S01"
        self.write()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            load_plan(self.plan)

    def test_frame_states_unique_ordered_and_valid(self):
        for states in (("end", "start"), ("key", "key"), ("middle",), ([],)):
            with self.subTest(states=states):
                data = copy.deepcopy(self.data)
                data["shots"][0]["frames"] = [{"state": state, "file": "frames/a.png"} for state in states]
                self.write(data)
                with self.assertRaises(ValueError):
                    load_plan(self.plan)

    def test_missing_or_empty_frames_rejected(self):
        for frames in ([], [{"state": "key", "file": "frames/missing.png"}]):
            with self.subTest(frames=frames):
                data = copy.deepcopy(self.data)
                data["shots"][0]["frames"] = frames
                self.write(data)
                with self.assertRaises(ValueError):
                    load_plan(self.plan)

    def test_paths_cannot_escape_project(self):
        for filename in (str(self.root / "frames/a.png"), "../outside.png"):
            with self.subTest(filename=filename):
                data = copy.deepcopy(self.data)
                data["shots"][0]["frames"][0]["file"] = filename
                self.write(data)
                with self.assertRaisesRegex(ValueError, "relative|escapes"):
                    load_plan(self.plan)
        try:
            (self.root / "frames/link.png").symlink_to(self.root.parent / "outside.png")
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest("Windows account cannot create symbolic links; relative path checks above passed")
            raise
        self.data["shots"][0]["frames"][0]["file"] = "frames/link.png"
        self.write()
        with self.assertRaisesRegex(ValueError, "escapes"):
            load_plan(self.plan)

    def test_bad_aspect_rejected(self):
        for ratio in ("0:9", "16:0", "16/9", "-1:1", None):
            with self.subTest(ratio=ratio):
                data = copy.deepcopy(self.data)
                data["aspect_ratio"] = ratio
                self.write(data)
                with self.assertRaises(ValueError):
                    load_plan(self.plan)

    def test_rendered_panels_keep_order_and_pixels(self):
        result = assemble(self.plan, self.output, columns=2, cell_width=160)
        self.assertEqual(result["warnings"], [])
        self.assertEqual(result["panels"], 2)
        with Image.open(self.output) as board:
            self.assertEqual(board.size, (380, 234))
            self.assertEqual(board.getpixel((100, 100)), (255, 0, 0))
            self.assertEqual(board.getpixel((280, 100)), (0, 0, 255))
        with Image.open(self.root / "frames/a.png") as source:
            self.assertEqual(source.size, (160, 90))

    def test_wrong_aspect_letterboxes_without_cropping(self):
        Image.new("RGB", (90, 90), "red").save(self.root / "frames/a.png")
        result = assemble(self.plan, self.output, cell_width=160)
        self.assertEqual(len(result["warnings"]), 1)
        with Image.open(self.output) as board:
            self.assertEqual(board.getpixel((22, 100)), (255, 255, 255))
            self.assertEqual(board.getpixel((100, 100)), (255, 0, 0))

    def test_pagination_and_start_end_frames(self):
        self.data["shots"][0]["frames"] = [
            {"state": "start", "file": "frames/a.png"},
            {"state": "end", "file": "frames/b.png"},
        ]
        self.write()
        result = assemble(self.plan, self.output, page_size=2, cell_width=160)
        self.assertEqual(result["panels"], 3)
        self.assertEqual([Path(p).name for p in result["outputs"]], ["board-01.png", "board-02.png"])
        self.assertTrue(all(Path(p).is_file() for p in result["outputs"]))

    def test_overwrite_and_input_collision_protection(self):
        self.output.write_bytes(b"keep existing file")
        with self.assertRaisesRegex(ValueError, "already exists"):
            assemble(self.plan, self.output)
        self.assertEqual(self.output.read_bytes(), b"keep existing file")
        with self.assertRaisesRegex(ValueError, "input file"):
            assemble(self.plan, self.root / "frames/a.png", overwrite=True)
        result = assemble(self.plan, self.output, overwrite=True, cell_width=160)
        self.assertEqual(len(result["outputs"]), 1)

    def test_bad_image_fails_before_writing_pages(self):
        (self.root / "frames/b.png").write_text("not an image")
        with self.assertRaises(OSError):
            assemble(self.plan, self.output, page_size=1)
        self.assertFalse((self.root / "board-01.png").exists())

    def test_vertical_board_and_resource_guard(self):
        self.data["aspect_ratio"] = "9:16"
        self.write()
        result = assemble(self.plan, self.output, cell_width=90)
        self.assertEqual(len(result["warnings"]), 2)
        with Image.open(self.output) as board:
            self.assertEqual(board.size, (240, 304))
        with self.assertRaisesRegex(ValueError, "megapixels"):
            assemble(self.plan, self.root / "huge.png", cell_width=10000)

    def test_caption_wraps_cjk_and_marks_truncation(self):
        font = choose_font(None, 17)
        lines, truncated = wrap_text("花瓣与叶片的真实纹理以及盆底支撑点" * 5, font, 120, 3)
        self.assertTrue(truncated)
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[-1].endswith("…"))
        self.assertTrue(all(font.getlength(line) <= 120 for line in lines))
        lines, truncated = wrap_text("完整花束\nBlack nursery pot", font, 300, 4)
        self.assertFalse(truncated)
        self.assertEqual(lines, ["完整花束", "Black nursery pot"])

    def test_caption_rows_align_and_never_cover_frames(self):
        self.data["total_duration_s"] = 12
        self.data["shots"][0]["caption"] = {"purpose": "Show overall height", "action": "Keep the tree still"}
        self.data["shots"][1]["caption"] = {"shot_size": "Full shot"}
        self.data["shots"].append({"id": "S03", "start_s": 8, "duration_s": 4,
                                   "caption": {"camera": "Locked camera"},
                                   "frames": [{"state": "key", "file": "frames/a.png"}]})
        self.write()
        before = (self.root / "frames/a.png").read_bytes()
        manifest = self.root / "board-manifest.json"
        assemble(self.plan, self.output, columns=2, cell_width=160, manifest=manifest)
        cells = json.loads(manifest.read_text())["pages"][0]["panels"]
        first, second, third = cells
        self.assertEqual(first["image_box"][1], second["image_box"][1])
        self.assertEqual(first["caption_box"][3], second["caption_box"][3])
        self.assertGreater(third["image_box"][1], first["caption_box"][1] + first["caption_box"][3])
        with Image.open(self.output) as board:
            for cell, color in zip(cells, ((255, 0, 0), (0, 0, 255), (255, 0, 0))):
                x, y, width, height = cell["image_box"]
                self.assertEqual(board.getpixel((x + width // 2, y + height // 2)), color)
                self.assertEqual(cell["caption_box"][1], y + height)
        self.assertEqual((self.root / "frames/a.png").read_bytes(), before)

    def test_manifest_preserves_selected_files_and_plan_snapshot(self):
        self.data["revision"] = "v2"
        self.data["shots"][0]["caption"] = {"purpose": "Original approved meaning"}
        self.write()
        original_plan = self.plan.read_bytes()
        manifest = self.root / "selected-frames.json"
        result = assemble(self.plan, self.output, page_size=1, cell_width=200, manifest=manifest)
        saved = json.loads(manifest.read_text())
        self.assertEqual(result["manifest"], str(manifest))
        self.assertEqual(saved["plan"]["sha256"], hashlib.sha256(original_plan).hexdigest())
        self.assertEqual(saved["plan"]["snapshot"], self.data)
        self.assertEqual([p["panels"][0]["shot_id"] for p in saved["pages"]], ["S01", "S02"])
        self.assertEqual(saved["pages"][0]["panels"][0]["source"], "frames/a.png")
        self.assertEqual(saved["pages"][0]["panels"][0]["source_sha256"],
                         hashlib.sha256((self.root / "frames/a.png").read_bytes()).hexdigest())
        self.data["shots"][0]["caption"]["purpose"] = "A later edit"
        self.write()
        self.assertEqual(json.loads(manifest.read_text())["plan"]["snapshot"]["shots"][0]["caption"]["purpose"],
                         "Original approved meaning")

    def test_manifest_collision_fails_before_any_image_is_written(self):
        manifest = self.root / "board-manifest.json"
        manifest.write_text("keep this manifest")
        with self.assertRaisesRegex(ValueError, "already exists"):
            assemble(self.plan, self.output, manifest=manifest)
        self.assertFalse(self.output.exists())
        self.assertEqual(manifest.read_text(), "keep this manifest")
        with self.assertRaisesRegex(ValueError, "input file"):
            assemble(self.plan, self.output, manifest=self.plan, overwrite=True)
        self.assertFalse(self.output.exists())

    def test_invalid_output_tree_fails_before_any_image_is_written(self):
        directory = self.root / "directory.json"
        directory.mkdir()
        with self.assertRaisesRegex(ValueError, "regular file"):
            assemble(self.plan, self.output, manifest=directory, overwrite=True)
        self.assertFalse(self.output.exists())
        with self.assertRaisesRegex(ValueError, "ancestors"):
            assemble(self.plan, self.output, manifest=self.output / "nested.json")
        self.assertFalse(self.output.exists())
        parent_file = self.root / "parent-file"
        parent_file.write_text("preserve")
        with self.assertRaisesRegex(ValueError, "parent must be a directory"):
            assemble(self.plan, self.output, manifest=parent_file / "nested.json")
        self.assertFalse(self.output.exists())
        self.assertEqual(parent_file.read_text(), "preserve")

    def test_invalid_caption_and_revision_rejected(self):
        for caption in (None, [], {"action": 1}, {"unrecognized": "text"}):
            with self.subTest(caption=caption):
                data = copy.deepcopy(self.data)
                data["shots"][0]["caption"] = caption
                self.write(data)
                with self.assertRaisesRegex(ValueError, "caption"):
                    load_plan(self.plan)
        self.data["revision"] = 2
        self.write()
        with self.assertRaisesRegex(ValueError, "revision"):
            load_plan(self.plan)

    def test_truncated_caption_warns_and_keeps_full_snapshot(self):
        long_action = "Keep the tree still while the camera slowly moves forward. " * 8
        self.data["shots"][0]["caption"] = {"action": long_action}
        self.write()
        manifest = self.root / "board-manifest.json"
        result = assemble(self.plan, self.output, cell_width=160, manifest=manifest)
        self.assertTrue(any("caption.action truncated" in warning for warning in result["warnings"]))
        self.assertEqual(json.loads(manifest.read_text())["plan"]["snapshot"]["shots"][0]["caption"]["action"],
                         long_action)


if __name__ == "__main__":
    unittest.main()
