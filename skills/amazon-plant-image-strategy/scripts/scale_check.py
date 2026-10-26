"""Arithmetic checks for explicitly supplied scale plans; never image verification."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def _number(data, key, errors, *, default=None, required=False, allow_zero=False):
    value = data.get(key, default)
    if key not in data and value is None and not required:
        return None
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or value < 0 or (value == 0 and not allow_zero)):
        errors.append(f"{key}: expected a finite {'nonnegative' if allow_zero else 'positive'} number")
        return None
    return value


def _stem_geometry(raw, errors, warnings):
    """Straight stem, resting at a stated support, decorative body above the rim."""
    if not isinstance(raw, dict):
        errors.append("stem_geometry must be an object")
        return None
    start = len(errors)
    values = {key: _number(raw, key, errors, required=True) for key in
              ("total_cm", "body_cm", "container_height_cm", "usable_depth_cm")}
    trim = _number(raw, "trim_cm", errors, default=0, allow_zero=True)
    tilt = _number(raw, "tilt_degrees", errors, default=0, allow_zero=True)
    supplied_bare = _number(raw, "bare_cm", errors, allow_zero=True)
    for key in ("total_basis", "body_basis"):
        if raw.get(key) not in {"measured", "user_confirmed"}:
            errors.append(f"{key} must be measured or user_confirmed; product segments are not design assumptions")
    if raw.get("container_basis") not in {"measured", "user_confirmed", "design_assumption"}:
        errors.append("container_basis must be measured, user_confirmed or design_assumption")
    elif raw["container_basis"] == "design_assumption":
        warnings.append("Container height/depth are design assumptions, not measured product facts.")
    if tilt is not None and tilt >= 90:
        errors.append("tilt_degrees must be below 90 from vertical")
    if trim is not None and trim > 0:
        if raw.get("trim_allowed") is not True:
            errors.append("A positive trim requires trim_allowed=true backed by this SKU's evidence")
        if raw.get("trim_decision") not in {"confirmed", "delegated"}:
            errors.append("A positive trim requires a confirmed or explicitly delegated trim_decision")
    if len(errors) != start:
        return None
    total, body = values["total_cm"], values["body_cm"]
    height, depth = values["container_height_cm"], values["usable_depth_cm"]
    bare = total - body
    if body > total:
        errors.append("body_cm cannot exceed total_cm on the same measurement axis")
    if supplied_bare is not None and not math.isclose(supplied_bare, bare, rel_tol=1e-6, abs_tol=1e-6):
        errors.append("bare_cm conflicts with total_cm minus body_cm")
    if depth > height:
        errors.append("usable_depth_cm cannot exceed external container_height_cm")
    if trim > bare:
        errors.append("trim_cm removes more than the available lower bare stem")
    if len(errors) != start:
        return None
    cosine = math.cos(math.radians(tilt))
    insertion = depth / cosine
    exposed_bare = bare - trim - insertion
    if exposed_bare < -1e-6:
        errors.append("Insertion exceeds the remaining bare stem; the decorative body would be buried below the rim")
        return None
    exposed_bare = max(0, exposed_bare)
    body_vertical = body * cosine
    bare_vertical = exposed_bare * cosine
    above_rim = (total - trim - insertion) * cosine
    warnings.append("Straight-stem arithmetic only: opening/wall clearance, support, stability and pictured endpoints are not verified.")
    return {
        "total_cm": total, "body_cm": body, "bare_cm": bare,
        "trim_cm": trim, "trimmed_total_cm": total - trim,
        "remaining_bare_cm": bare - trim, "tilt_degrees": tilt,
        "container_height_cm": height, "usable_depth_cm": depth,
        "support_height_cm": height - depth, "insertion_cm": insertion,
        "exposed_bare_cm": exposed_bare, "exposed_bare_vertical_cm": bare_vertical,
        "body_vertical_cm": body_vertical, "above_rim_vertical_cm": above_rim,
        "arrangement_height_cm": height + above_rim,
    }


def _assess_instances(plan, result):
    raw = plan["instances"]
    if not isinstance(raw, list) or not raw or not all(isinstance(p, dict) for p in raw):
        result["errors"].append("instances must be a nonempty list of scale-plan objects")
        return result
    if any(key in plan for key in ("product_cm", "reference_cm", "stem_geometry")):
        result["errors"].append("Put all scale inputs inside instances; do not mix parent and instance geometry")
    seen, containers, reports = set(), {}, []
    for item in raw:
        instance = item.get("instance_id")
        if not isinstance(instance, str) or not instance.strip() or instance in seen:
            result["errors"].append("Each instance_id must be a unique nonempty string within its asset")
            continue
        seen.add(instance)
        if "instances" in item or "asset_id" in item:
            result["errors"].append(f"{instance}: nested instances and instance-level asset_id are not allowed")
            continue
        if any(not isinstance(item.get(key), str) or not item[key].strip()
               for key in ("product_id", "container_id")):
            result["errors"].append(f"{instance}: product_id and container_id are required")
            continue
        report = assess(dict(item, asset_id=plan.get("asset_id")))
        report.update({key: item[key] for key in ("instance_id", "product_id", "container_id")})
        reports.append(report)
        result["errors"].extend(f"{instance}: {e}" for e in report["errors"])
        result["warnings"].extend(f"{instance}: {w}" for w in report["warnings"])
        geometry = report.get("stem_geometry")
        if geometry:
            dims = (geometry["container_height_cm"], geometry["usable_depth_cm"])
            previous = containers.setdefault(item["container_id"], dims)
            if any(not math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-6) for a, b in zip(previous, dims)):
                result["errors"].append(f"{instance}: the same container_id has conflicting external height or usable depth")
    result.update(instances=reports, visual_check="per_instance", segment_visual_check="per_instance")
    result["warnings"].append("Per-instance geometry does not verify sale contents, quantity conservation or user composition choices.")
    return result


def assess(plan: dict) -> dict:
    result = {"asset_id": plan.get("asset_id"), "errors": [], "warnings": [],
              "visual_check": "not_provided", "segment_visual_check": "not_provided",
              "geometry_check": "not_provided", "scope": "supplied arithmetic only"}
    errors, warnings = result["errors"], result["warnings"]
    if not isinstance(plan.get("asset_id"), str) or not plan["asset_id"].strip():
        errors.append("asset_id must be a nonempty string")
    if not isinstance(plan.get("asset_id"), str) or not plan["asset_id"].strip():
        errors.append("asset_id must be a nonempty string")

    if "instances" in plan:
        return _assess_instances(plan, result)

    def positive(key, required=False, fraction=False):
        value = plan.get(key)
        if value is None and not required:
            return None
        if (isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value) or value <= 0 or (fraction and value > 1)):
            errors.append(f"{key}: expected a finite positive {'fraction <= 1' if fraction else 'number'}")
            return None
        return value

    geometry = None
    if "stem_geometry" in plan:
        geometry = _stem_geometry(plan["stem_geometry"], errors, warnings)
        result["geometry_check"] = "calculated" if geometry else "invalid_input"
        if geometry:
            result["stem_geometry"] = geometry
    product = positive("product_cm", required="stem_geometry" not in plan)
    if geometry:
        expected_height = geometry["arrangement_height_cm"]
        if product is not None and not math.isclose(product, expected_height, rel_tol=1e-6, abs_tol=1e-6):
            errors.append("product_cm conflicts with the derived tabletop-to-tip arrangement height")
        product = expected_height
    reference = positive("reference_cm", required=True)
    if geometry and plan.get("reference_role") == "container" and reference is not None:
        if not math.isclose(reference, geometry["container_height_cm"], rel_tol=1e-6, abs_tol=1e-6):
            errors.append("reference_cm must equal external container height when reference_role is container")
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
    segment_inputs = {}
    for name in ("body", "exposed_bare"):
        frame_key, pixel_key = f"{name}_frame_fraction", f"observed_{name}_px"
        frame = _number(plan, frame_key, errors, allow_zero=name == "exposed_bare")
        pixels = _number(plan, pixel_key, errors, allow_zero=name == "exposed_bare")
        if frame is not None and frame > 1:
            errors.append(f"{frame_key}: expected a fraction <= 1")
        if frame_key in plan or pixel_key in plan:
            if not geometry:
                errors.append("Segment framing/observations require valid stem_geometry")
        segment_inputs[name] = (frame, pixels)
    any_observed = observed_product is not None or any(p is not None for _, p in segment_inputs.values())
    if any_observed != (observed_reference is not None):
        errors.append("Observed product or segment pixels must be paired with observed_reference_px.")
    if errors:
        return result
    ratio = product / reference
    result["world_ratio"] = ratio
    if factor is None:
        result["visual_check"] = "perspective_unresolved"
        if geometry:
            result["segment_visual_check"] = "perspective_unresolved"
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
    if geometry:
        segment_checks = []
        for name, length in (("body", geometry["body_vertical_cm"]),
                             ("exposed_bare", geometry["exposed_bare_vertical_cm"])):
            expected_ratio = length / reference * factor
            result[f"expected_{name}_projected_ratio"] = expected_ratio
            frame, pixels = segment_inputs[name]
            if reference_frame is not None:
                expected_frame = expected_ratio * reference_frame
                result[f"expected_{name}_frame_fraction"] = expected_frame
                if frame is not None:
                    drift = abs(frame / expected_frame - 1) if expected_frame else (0 if frame == 0 else math.inf)
                    if drift > tolerance:
                        errors.append(f"Planned {name} frame coverage conflicts with the segment geometry.")
            elif frame is not None:
                warnings.append(f"No reference frame fraction: {name} coverage cannot be cross-checked.")
            if pixels is not None:
                observed = pixels / observed_reference
                drift = abs(observed / expected_ratio - 1) if expected_ratio else (0 if observed == 0 else math.inf)
                result[f"observed_{name}_projected_ratio"] = observed
                result[f"observed_{name}_relative_drift"] = drift if math.isfinite(drift) else None
                segment_checks.append(drift <= tolerance)
                if drift > tolerance:
                    errors.append(f"Supplied observed {name} pixel ratio is outside the diagnostic threshold.")
        if segment_checks:
            result["segment_visual_check"] = ("within_supplied_threshold" if all(segment_checks)
                                               else "outside_supplied_threshold")
            warnings.append("Segment pixel endpoints and the single-stem body identity are reviewer-supplied, not detected.")
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
