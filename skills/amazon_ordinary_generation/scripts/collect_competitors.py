#!/usr/bin/env python3
"""Attempt every retained competitor independently; never mark downloads as viewed."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

from collect_competitor import output_root
from research_audit import load_inputs, DOMAINS


def run_batch(inputs, out, *, headed=False, browser_executable=None, runner=subprocess.run):
    rows = load_inputs(inputs)
    root = output_root(out)
    run = root / ("batch-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ"))
    run.mkdir(parents=True, exist_ok=False)
    report = {"inputRegistry": str(Path(inputs).resolve()), "coverage": "capture attempts only; visual/review research separate",
              "competitors": [dict(asin=r["asin"], marketplace=r["marketplace"], url=r["url"], status="queued") for r in rows]}
    file = run / "batch-manifest.json"

    def save():
        file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    save()
    for item in report["competitors"]:
        item["status"] = "running"
        save()
        # Sequential isolated contexts avoid depending on an external scraper's lock contract.
        media = run / item["marketplace"]
        command = [sys.executable, str(Path(__file__).with_name("collect_competitor.py")),
                   item["url"], "--marketplace", DOMAINS[item["marketplace"]], "--out", str(media)]
        if headed:
            command.append("--headed")
        if browser_executable:
            command.extend(["--browser-executable", browser_executable])
        try:
            result = runner(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
            item.update(status="captured-partial" if result.returncode == 0 else "capture-failed",
                        returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)
        except (OSError, subprocess.TimeoutExpired) as exc:
            item.update(status="capture-failed", error=str(exc))
        save()  # Failure for one input never deletes it or skips the remaining inputs.
    report["status"] = "partial" if any(i["status"] == "capture-failed" for i in report["competitors"]) else "captured-partial"
    save()
    return file, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--browser-executable")
    args = parser.parse_args()
    try:
        file, report = run_batch(args.inputs, args.out, headed=args.headed, browser_executable=args.browser_executable)
        print(json.dumps({"manifest": str(file), "competitors": len(report["competitors"]), "status": report["status"]}))
        return 2 if report["status"] == "partial" else 0
    except (OSError, ValueError) as exc:
        print(f"Batch capture unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
