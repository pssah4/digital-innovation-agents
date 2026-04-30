#!/usr/bin/env python3
"""DIA migration -- Phase 0: detect repo state.

Scans a project root and classifies it as DIA v1, DIA v2, mixed, or
brownfield. Returns a JSON report on stdout that the orchestrating
skill consumes.

Usage:
    python3 detect_state.py [project_root]

Default project_root: cwd.

Idempotent. Read-only. Does not modify any file.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path


def detect(root: Path) -> dict:
    devp = root / "_devprocess"
    src = root / "src"

    findings: dict = {
        "project_root": str(root),
        "has_devprocess": devp.is_dir(),
        "has_src": src.is_dir(),
        "v1_signals": {},
        "v2_signals": {},
        "counts": {},
        "recommendation": "",
    }

    # v1 signals
    findings["v1_signals"]["fixes_under_context"] = (devp / "context/fixes").is_dir()
    findings["v1_signals"]["improvements_under_context"] = (devp / "context/improvements").is_dir()
    findings["v1_signals"]["bug_log_file"] = (devp / "context/20_bugs.md").is_file()
    findings["v1_signals"]["security_subdir"] = (devp / "analysis/security").is_dir()
    findings["v1_signals"]["archive_dirs"] = sorted(
        str(p.relative_to(root)) for p in devp.rglob("archive") if p.is_dir()
    ) if devp.is_dir() else []
    findings["v1_signals"]["legacy_tech_docs"] = (devp / "architecture/legacy-tech-docs").is_dir()

    # v2 signals
    findings["v2_signals"]["rules_dir"] = (devp / "rules").is_dir()
    findings["v2_signals"]["fixes_under_requirements"] = (devp / "requirements/fixes").is_dir()
    findings["v2_signals"]["architecture_map"] = (src / "ARCHITECTURE.map").is_file()
    findings["v2_signals"]["backlog_present"] = (devp / "context/BACKLOG.md").is_file()

    # Pattern counts
    def count_glob(pattern: str) -> int:
        return sum(1 for _ in (devp.glob(pattern) if devp.is_dir() else []))

    findings["counts"]["epic_3digit"] = count_glob("requirements/epics/EPIC-[0-9][0-9][0-9]-*.md")
    findings["counts"]["epic_2digit"] = count_glob("requirements/epics/EPIC-[0-9][0-9]-*.md")
    findings["counts"]["feature_4digit"] = count_glob("requirements/features/FEATURE-*.md")
    findings["counts"]["feat_v2"] = count_glob("requirements/features/FEAT-*.md")
    findings["counts"]["adr_3digit"] = count_glob("architecture/ADR-[0-9][0-9][0-9]-*.md")
    findings["counts"]["adr_2digit"] = count_glob("architecture/ADR-[0-9][0-9]-*.md")
    findings["counts"]["plan_3digit"] = count_glob("implementation/plans/PLAN-[0-9][0-9][0-9]-*.md")
    findings["counts"]["plan_2digit"] = count_glob("implementation/plans/PLAN-[0-9][0-9]-*.md")
    findings["counts"]["fix_v1"] = count_glob("context/fixes/FIX-*.md") + count_glob("context/fixes/BUG-*.md")
    findings["counts"]["fix_v2"] = count_glob("requirements/fixes/FIX-*.md")

    # Status drift in frontmatter
    fm_drift = 0
    body_drift = 0
    if devp.is_dir():
        targets = []
        # Only scan canonical artifact files (prefix-based) so meta-docs
        # like arc42.md or README.md are not flagged as drift.
        artifact_globs = [
            ("requirements/features", "FEAT-*.md"),
            ("requirements/features", "FEATURE-*.md"),
            ("requirements/epics", "EPIC-*.md"),
            ("architecture", "ADR-*.md"),
            ("implementation/plans", "PLAN-*.md"),
            ("requirements/fixes", "FIX-*.md"),
            ("requirements/fixes", "BUG-*.md"),
            ("requirements/improvements", "IMP-*.md"),
            ("context/fixes", "FIX-*.md"),
            ("context/fixes", "BUG-*.md"),
            ("context/improvements", "IMP-*.md"),
        ]
        for sub, glob in artifact_globs:
            d = devp / sub
            if d.is_dir():
                targets.extend(d.glob(glob))
        fm_pat = re.compile(r"^(status|phase|last_updated|last-updated|lastUpdated):", re.M)
        body_pat = re.compile(r"^\*\*Status:\*\*|^Status: |^> \*\*Status:|^\*\*Last\s+Updated:\*\*", re.M)
        for fp in targets:
            try:
                content = fp.read_text(encoding="utf-8")
            except Exception:
                continue
            m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if m and fm_pat.search(m.group(1)):
                fm_drift += 1
            head = "\n".join(content.split("\n")[:25])
            if body_pat.search(head):
                body_drift += 1
    findings["counts"]["frontmatter_status_drift"] = fm_drift
    findings["counts"]["body_status_drift"] = body_drift

    # Recommendation
    if not findings["has_devprocess"] and not findings["has_src"]:
        findings["recommendation"] = "empty-repo"
    elif not findings["has_devprocess"]:
        findings["recommendation"] = "brownfield-call-reverse-engineering-first"
    else:
        v1_total = (
            int(findings["v1_signals"]["fixes_under_context"])
            + int(findings["v1_signals"]["improvements_under_context"])
            + int(findings["v1_signals"]["bug_log_file"])
            + int(findings["v1_signals"]["security_subdir"])
            + int(findings["v1_signals"]["legacy_tech_docs"])
            + len(findings["v1_signals"]["archive_dirs"])
            + findings["counts"]["feature_4digit"]
            + findings["counts"]["epic_3digit"]
            + findings["counts"]["adr_3digit"]
            + findings["counts"]["fix_v1"]
            + fm_drift + body_drift
        )
        if v1_total == 0:
            findings["recommendation"] = "v2-clean-no-migration-needed"
        else:
            findings["recommendation"] = "run-full-migration"
    return findings


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        return 2
    report = detect(root)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
