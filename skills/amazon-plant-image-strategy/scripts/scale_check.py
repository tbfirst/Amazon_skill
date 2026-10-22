"""Arithmetic checks for explicitly supplied scale plans; never image verification."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def assess(plan: dict) -> dict:
    result = {"asset_id": plan.get("asset_id"), "errors": [], "warnings": [],
              "visual_check": "not_provided", "scope": "supplied arithmetic only"}
    errors, warnings = result["errors"], result["warnings"]
    if not isinstance(plan.get("asset_id"), str) or not plan["asset_id"].strip():
        errors.append("asset_id must be a nonempty string")
    if not isinstance(plan.get("asset_id"), str) or not plan["asset_id"].strip():
        errors.append("asset_id must be a nonempty string")

    def positive(key, required=False, fraction=False):
        value = plan.get(key)
        if value is None and not required:
            return None
        if (isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value) or value <= 0 or (fraction and value > 1)):
            errors.append(f"{key}: expected a finite positive {'fraction <= 1' if fraction else 'number'}")
            return None
        return value

    product = positive("product_cm", required=True)
    reference = positive("reference_cm", required=True)
    tolerance = positive("relative_tolerance") if "relative_tolerance" in plan else 0.1
    if tolerance is not None and tolerance >= 1:
        errors.append("relative_tolerance must be less than 1")
    basis = plan.get("reference_basis")
    if basis not in {"measured", "user_confirmed", "design_assumption"}:
        errors.append("reference_basis must state measured, user_confirmed or design_assumption")
    elif basis == "design_assumption":
        warnings.append("Reference dimension is a design assumption, not a measured scene fact.")
    result["reference_basis"] = basis
    mode = plan.get("projection_mode")
    if mode == "coplanar_parallel":
        factor = 1
        if "perspective_factor" in plan:
            errors.append("Do not supply a perspective_factor for coplanar_parallel; choose explicit_factor.")
    elif mode == "explicit_factor":
        factor = positive("perspective_factor", required=True)
        warnings.append("Perspective factor is caller-supplied; geometry and comparable axes are not verified.")
    elif mode == "unresolved":
        factor = None
        warnings.append("Perspective unresolved: projected scale remains unverified.")
    else:
        factor = None
        errors.append("projection_mode must be coplanar_parallel, explicit_factor or unresolved")
    product_frame = positive("product_frame_fraction", fraction=True)
    reference_frame = positive("reference_frame_fraction", fraction=True)
    observed_product = positive("observed_product_px")
    observed_reference = positive("observed_reference_px")
    if ("observed_product_px" in plan) != ("observed_reference_px" in plan):
        errors.append("Observed product/reference pixels must be supplied together.")
    if errors:
        return result
    ratio = product / reference
    result["world_ratio"] = ratio
    if factor is None:
        result["visual_check"] = "perspective_unresolved"
        return result
    projected = ratio * factor
    result["expected_projected_ratio"] = projected
    if reference_frame is not None:
        expected_frame = projected * reference_frame
        result["expected_product_frame_fraction"] = expected_frame
        if expected_frame > 1:
            errors.append("Full product cannot fit this framing; revise camera/reference coverage or declare a detail crop.")
        if product_frame is not None:
            drift = abs(product_frame / expected_frame - 1)
            result["planned_relative_drift"] = drift
            if drift > tolerance:
                errors.append("Planned product frame coverage conflicts with physical/projected scale.")
    elif product_frame is not None:
        warnings.append("No reference frame fraction: independent product coverage cannot be cross-checked.")
    if observed_product is not None and observed_reference is not None:
        observed = observed_product / observed_reference
        drift = abs(observed / projected - 1)
        result["observed_projected_ratio"] = observed
        result["observed_relative_drift"] = drift
        result["visual_check"] = "within_supplied_threshold" if drift <= tolerance else "outside_supplied_threshold"
        warnings.append("Observed endpoints/planes and identity are supplied by the reviewer, not checked by this script.")
        if drift > tolerance:
            errors.append("Supplied observed pixel ratio is outside the diagnostic threshold.")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="Optional UTF-8 audit report; parent directory must exist")
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8-sig"))
        plans = data["assets"]
        if not isinstance(plans, list) or not plans or not all(isinstance(p, dict) for p in plans):
            raise ValueError("assets must be a nonempty list of scale-plan objects")
        ids = [p.get("asset_id") for p in plans]
        if any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
            raise ValueError("Every asset_id must be a unique nonempty string")
        if args.output and args.input.resolve() == args.output.resolve():
            raise ValueError("Audit output must not overwrite the input plan")
        ids = [p.get("asset_id") for p in plans]
        if any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
            raise ValueError("Every asset_id must be a unique nonempty string")
        if args.output and args.input.resolve() == args.output.resolve():
            raise ValueError("Audit output must not overwrite the input plan")
        reports = [assess(p) for p in plans]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"Invalid input: {exc}\n")
    payload = json.dumps({"assets": reports, "scope": "arithmetic, not rendered fidelity"}, ensure_ascii=False, indent=2)
    if args.output:
        try:
            args.output.write_text(payload + "\n", encoding="utf-8")
        except OSError as exc:
            parser.exit(2, f"Cannot write report: {exc}\n")
    print(payload)
    return int(any(r["errors"] for r in reports))


if __name__ == "__main__":
    raise SystemExit(main())
