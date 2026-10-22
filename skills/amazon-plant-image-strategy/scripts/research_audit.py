#!/usr/bin/env python3
"""Offline input normalization and research-record audit; never fetches pages."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse, unquote

DOMAINS = {"US": "amazon.com", "UK": "amazon.co.uk", "DE": "amazon.de",
           "FR": "amazon.fr", "IT": "amazon.it", "ES": "amazon.es",
           "CA": "amazon.ca", "JP": "amazon.co.jp", "AU": "amazon.com.au"}
ASIN = re.compile(r"[A-Z0-9]{10}\Z")
SECTIONS = ("gallery", "aplus", "review_photos", "reviews")
STATES = {"pending", "observed", "partial", "text-only", "access-blocked",
          "not-observed", "absent"}
ASSETS = {"DIM01", "DETAIL01", *[f"SCENE{i:02}" for i in range(1, 5)],
          *[f"APLUS{i:02}" for i in range(1, 6)]}


def normalize(inputs, marketplace="US"):
    """Deduplicate by marketplace AND ASIN; no network expansion of short URLs."""
    result = {}
    for raw in inputs:
        value = raw.strip()
        market = marketplace
        if ASIN.fullmatch(value.upper()):
            asin = value.upper()
        else:
            parsed = urlparse(value)
            host = (parsed.hostname or "").lower()
            markets = [m for m, d in DOMAINS.items()
                       if host == d or host in ("www." + d, "m." + d)]
            if parsed.scheme not in ("http", "https") or not markets:
                raise ValueError(f"Unsupported URL; resolve short links in browser first: {raw}")
            if parsed.username or parsed.password or parsed.port:
                raise ValueError("Credential-bearing URLs or custom ports are not product inputs")
            match = re.search(r"/(?:dp|gp/product|gp/aw/d)/([A-Z0-9]{10})(?:/|$)",
                              unquote(parsed.path).upper(), re.I)
            if not match:
                raise ValueError(f"No supported product ASIN in URL: {raw}")
            asin, market = match.group(1).upper(), markets[0]
        key = (market, asin)
        item = result.setdefault(key, {"asin": asin, "marketplace": market,
                    "url": f"https://www.{DOMAINS[market]}/dp/{asin}", "inputs": []})
        if raw not in item["inputs"]:
            item["inputs"].append(raw)
    return list(result.values())


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def audit_record(data):
    """Return errors, warnings and derived counts; consistency is not truth."""
    errors, warnings = [], []
    counts = Counter()
    themes = Counter()
    review_ids = set()
    if not isinstance(data, dict):
        return ["record must be an object"], [], {}, {}, set()
    asin = data.get("asin", "")
    if not isinstance(asin, str) or not ASIN.fullmatch(asin):
        errors.append("asin must be a canonical 10-character identifier")
    if not isinstance(data.get("marketplace"), str) or data.get("marketplace") not in DOMAINS:
        errors.append("unsupported marketplace; keep each marketplace in a separate research folder")
    if type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    identity = data.get("identity", {})
    if not isinstance(identity, dict):
        errors.append("identity must be an object")
        identity = {}
    verified = identity.get("verified") is True
    if type(identity.get("verified")) is not bool:
        errors.append("identity.verified must be a boolean")
    if verified:
        for field in ("title", "variant", "source", "observed_at", "final_asin"):
            if not nonempty(identity.get(field)):
                errors.append(f"verified identity needs {field}")
        if identity.get("final_asin") != asin and not nonempty(identity.get("resolution")):
            errors.append("redirected ASIN needs a documented identity resolution")
        if not isinstance(identity.get("final_asin"), str) or not ASIN.fullmatch(identity["final_asin"]):
            errors.append("final_asin must be a canonical 10-character identifier")
    else:
        warnings.append("identity is not yet verified")
    sections = data.get("sections", {})
    if not isinstance(sections, dict):
        errors.append("sections must be an object")
        sections = {}
    visuals = data.get("visuals", [])
    if not isinstance(visuals, list):
        errors.append("visuals must be an array")
        visuals = []
    visual_ids = set()
    for v in visuals:
        if not isinstance(v, dict):
            errors.append("visual must be an object")
            continue
        vid = v.get("id")
        if not nonempty(vid) or vid in visual_ids:
            errors.append("visual id missing or duplicated")
        if isinstance(vid, str):
            visual_ids.add(vid)
        section = v.get("section")
        if section not in SECTIONS[:3]:
            errors.append(f"{vid}: invalid visual section")
        if v.get("observed") is not True:
            errors.append(f"{vid}: visual evidence requires actual observation; inventory belongs in sections")
        else:
            counts[section if isinstance(section, str) else "invalid"] += 1
        for field in ("source", "locator", "observed_at", "layout", "lighting", "shadow"):
            if not nonempty(v.get(field)):
                errors.append(f"{vid}: missing {field}")
        targets = v.get("transfer_to", [])
        if not isinstance(targets, list) or any(not isinstance(t, str) or t not in ASSETS for t in targets):
            errors.append(f"{vid}: transfer_to contains an asset outside the fixed 11")
    reviews = data.get("reviews", [])
    if not isinstance(reviews, list):
        errors.append("reviews must be an array")
        reviews = []
    for review in reviews:
        if not isinstance(review, dict):
            errors.append("review must be an object")
            continue
        rid = review.get("id")
        if not nonempty(rid) or rid in review_ids:
            errors.append("original review id missing or duplicated")
            continue
        review_ids.add(rid)
        if review.get("kind") != "original":
            errors.append(f"{rid}: AI summaries/ratings/Q&A cannot enter the original review sample")
            continue
        for field in ("source", "summary", "variant_scope"):
            if not nonempty(review.get(field)):
                errors.append(f"{rid}: missing {field}")
        tags = review.get("themes", [])
        if not isinstance(tags, list) or any(not nonempty(t) for t in tags):
            errors.append(f"{rid}: themes must be a string array")
        else:
            themes.update(set(tags))
        counts["reviews"] += 1
    if (visuals or reviews) and not verified:
        errors.append("observations must not be attributed to an unverified product identity")
    for name in SECTIONS:
        section = sections.get(name)
        if (not isinstance(section, dict) or not isinstance(section.get("status"), str)
                or section.get("status") not in STATES):
            errors.append(f"{name}: section missing or invalid status")
            continue
        status = section["status"]
        if status != "observed":
            warnings.append(f"{name}: {status}")
        if status not in ("pending", "observed") and not nonempty(section.get("reason")):
            errors.append(f"{name}: incomplete/absent status needs a reason")
        if status in ("observed", "partial", "text-only", "absent", "access-blocked"):
            if not nonempty(section.get("source")):
                errors.append(f"{name}: status needs a source/locator")
        if name != "reviews":
            total = section.get("inventory_total")
            if total is not None and (type(total) is not int or total < counts[name]):
                errors.append(f"{name}: inventory_total must be null or an integer >= observed count")
            if status == "observed" and (not counts[name] or total != counts[name]):
                errors.append(f"{name}: observed requires an inventoried scope with every unit inspected")
            if status == "absent" and total not in (None, 0):
                errors.append(f"{name}: absent contradicts a nonzero inventory")
        elif status in ("observed", "partial"):
            if not counts[name] or not nonempty(section.get("sampling")):
                errors.append("reviews: observed/partial requires original records and sampling method")
        if status in ("pending", "text-only", "absent", "not-observed", "access-blocked") and counts[name]:
            errors.append(f"{name}: existing observations require partial or observed status")
    attempts = data.get("attempts", [])
    if not isinstance(attempts, list):
        errors.append("attempts must be an array")
        attempts = []
    for attempt in attempts:
        if not isinstance(attempt, dict) or any(not nonempty(attempt.get(k)) for k in ("section", "route", "result")):
            errors.append("recovery attempt needs section, route and result")
    for name in SECTIONS:
        if isinstance(sections.get(name), dict) and sections[name].get("status") == "access-blocked":
            if not any(isinstance(a, dict) and a.get("section") == name for a in attempts):
                errors.append(f"{name}: access-blocked needs an actual attempt record")
    return errors, warnings, dict(counts), dict(themes), review_ids


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def audit_folder(folder):
    files = sorted(folder.glob("*.json"))
    errors, warnings, rows = [], [], []
    seen, review_owners = set(), {}
    for file in files:
        try:
            data = json.loads(file.read_text(encoding="utf-8-sig"))
            errs, warns, counts, themes, ids = audit_record(data)
        except (ValueError, OSError) as exc:
            errors.append(f"{file.name}: {exc}")
            continue
        errors.extend(f"{file.name}: {e}" for e in errs)
        warnings.extend(f"{file.name}: {w}" for w in warns)
        if not isinstance(data, dict):
            continue
        key = (str(data.get("marketplace")), str(data.get("asin")))
        if key in seen:
            errors.append(f"duplicate competitor record: {key}")
        seen.add(key)
        for rid in ids:
            if rid in review_owners:
                warnings.append(f"shared review {rid} in {review_owners[rid]} and {file.name}; deduplicate before cross-ASIN aggregation")
            review_owners[rid] = file.name
        rows.append((key, counts, themes))
    if not files:
        errors.append("no competitor JSON records found")
    if len({key[0] for key in seen}) > 1:
        errors.append("mixed marketplaces: audit each marketplace separately")
    if not 3 <= len(seen) <= 6:
        warnings.append(f"{len(seen)} unique competitors; default project requests 3–6")
    lines = ["# Research record audit", "", "Offline consistency check only; not verification of source truth or research completeness.", "",
             f"Errors: {len(errors)}; gaps/warnings: {len(warnings)}", "",
             "| Competitor | Gallery observed | A+ observed | Buyer-photo observed | Original reviews N | Themes n (sample only) |",
             "| --- | --- | --- | --- | --- | --- |"]
    for key, counts, themes in rows:
        lines.append("| " + " | ".join(map(cell, ["/".join(key), *[counts.get(s, 0) for s in SECTIONS],
                       ", ".join(f"{k}: {v}" for k, v in sorted(themes.items())) or "unknown"])) + " |")
    lines += ["", "## Errors", ""] + ([f"- {e}" for e in errors] or ["None."])
    lines += ["", "## Remaining gaps / warnings", ""] + ([f"- {w}" for w in warnings] or ["None recorded."])
    return "\n".join(lines) + "\n", bool(errors)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    norm = sub.add_parser("normalize")
    norm.add_argument("inputs", nargs="+")
    norm.add_argument("--marketplace", choices=DOMAINS, default="US")
    audit = sub.add_parser("audit")
    audit.add_argument("directory", type=Path, help="Directory containing competitor JSON checkpoints")
    args = parser.parse_args()
    try:
        if args.command == "normalize":
            print(json.dumps(normalize(args.inputs, args.marketplace), ensure_ascii=False, indent=2))
            return 0
        report, failed = audit_folder(args.directory)
        print(report, end="")
        return int(failed)
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
