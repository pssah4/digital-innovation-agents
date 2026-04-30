#!/usr/bin/env python3
"""DIA migration -- Phase 3: filename migration to v2 ID schemas.

Renames artifact files and updates references in `_devprocess/` and
`src/ARCHITECTURE.map`. Two-pass:

Pass 1: file renames + reference replacement using the rename map.
Pass 2: catch-all regex sweep for IDs that have no corresponding file
        (legacy in-prose references like EPIC-023 that was never
        materialized).

Idempotent. Run on a clean v2 repo -> zero changes.

Skips `_devprocess/context/HANDOFFS.md` (append-only audit log)
to preserve historical IDs as written.

Usage:
    python3 migrate_naming.py [project_root]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


def collect_renames(root: Path) -> tuple[list[tuple[Path, Path]], dict[str, str]]:
    renames: list[tuple[Path, Path]] = []
    id_remap: dict[str, str] = {}

    def add(old_fp: Path, new_name: str, old_id: str, new_id: str) -> None:
        renames.append((old_fp, old_fp.parent / new_name))
        id_remap[old_id] = new_id

    devp = root / "_devprocess"
    if not devp.is_dir():
        return renames, id_remap

    # EPICs
    for fp in (devp / "requirements/epics").glob("EPIC-*.md") if (devp / "requirements/epics").is_dir() else []:
        m = re.match(r"^EPIC-(\d+)-(.+)\.md$", fp.name)
        if not m:
            continue
        n = int(m.group(1))
        slug = m.group(2)
        new_name = f"EPIC-{n:02d}-{slug}.md"
        if fp.name != new_name:
            add(fp, new_name, f"EPIC-{m.group(1)}", f"EPIC-{n:02d}")
        id_remap[f"EPIC-{n:03d}"] = f"EPIC-{n:02d}"

    # FEATUREs and FEATs
    feats_dir = devp / "requirements/features"
    if feats_dir.is_dir():
        for fp in feats_dir.glob("FEATURE-*.md"):
            m = re.match(r"^FEATURE-(\d+)([a-z]?)-(.+)\.md$", fp.name)
            if not m:
                continue
            num = m.group(1)
            suffix = m.group(2) or ""
            slug = m.group(3)
            if len(num) == 4:
                ee, ff = int(num[:2]), int(num[2:])
            elif len(num) == 3:
                ee, ff = int(num[0]), int(num[1:])
            else:
                ee, ff = 0, int(num)
            new_name = f"FEAT-{ee:02d}-{ff:02d}{suffix}-{slug}.md"
            add(fp, new_name, f"FEATURE-{num}{suffix}", f"FEAT-{ee:02d}-{ff:02d}{suffix}")

    # FIXes
    fixes_dir = devp / "requirements/fixes"
    if fixes_dir.is_dir():
        for fp in fixes_dir.glob("FIX-*.md"):
            m = re.match(r"^FIX-(\d{4})-(\d{2})-(.+)\.md$", fp.name)
            if not m:
                continue
            eeff, nn, slug = m.group(1), m.group(2), m.group(3)
            new_name = f"FIX-{eeff[:2]}-{eeff[2:]}-{nn}-{slug}.md"
            if fp.name != new_name:
                add(fp, new_name, f"FIX-{eeff}-{nn}", f"FIX-{eeff[:2]}-{eeff[2:]}-{nn}")

    # IMPs
    imps_dir = devp / "requirements/improvements"
    if imps_dir.is_dir():
        for fp in imps_dir.glob("IMP-*.md"):
            m = re.match(r"^IMP-(\d{4})-(\d{2})-(.+)\.md$", fp.name)
            if not m:
                continue
            eeff, nn, slug = m.group(1), m.group(2), m.group(3)
            new_name = f"IMP-{eeff[:2]}-{eeff[2:]}-{nn}-{slug}.md"
            if fp.name != new_name:
                add(fp, new_name, f"IMP-{eeff}-{nn}", f"IMP-{eeff[:2]}-{eeff[2:]}-{nn}")

    # ADRs
    adr_dir = devp / "architecture"
    if adr_dir.is_dir():
        for fp in adr_dir.glob("ADR-*.md"):
            m = re.match(r"^ADR-(\d+)-(.+)\.md$", fp.name)
            if not m:
                continue
            n = int(m.group(1))
            slug = m.group(2)
            new_name = f"ADR-{n:02d}-{slug}.md"
            if fp.name != new_name:
                add(fp, new_name, f"ADR-{m.group(1)}", f"ADR-{n:02d}")
            id_remap[f"ADR-{n:03d}"] = f"ADR-{n:02d}"

    # PLANs
    plan_dir = devp / "implementation/plans"
    if plan_dir.is_dir():
        for fp in plan_dir.glob("PLAN-*.md"):
            m = re.match(r"^PLAN-(\d+)-(.+)\.md$", fp.name)
            if not m:
                continue
            n = int(m.group(1))
            slug = m.group(2)
            new_name = f"PLAN-{n:02d}-{slug}.md"
            if fp.name != new_name:
                add(fp, new_name, f"PLAN-{m.group(1)}", f"PLAN-{n:02d}")
            id_remap[f"PLAN-{n:03d}"] = f"PLAN-{n:02d}"

    # BAs, EXPLOREs, RESEARCHes
    analysis = devp / "analysis"
    if analysis.is_dir():
        for prefix in ("BA", "EXPLORE", "RESEARCH"):
            for fp in analysis.glob(f"{prefix}-*.md"):
                m = re.match(rf"^{prefix}-(\d+)-(.+)\.md$", fp.name)
                if not m:
                    continue
                n = int(m.group(1))
                slug = m.group(2)
                new_name = f"{prefix}-{n:02d}-{slug}.md"
                if fp.name != new_name:
                    add(fp, new_name, f"{prefix}-{m.group(1)}", f"{prefix}-{n:02d}")
                id_remap[f"{prefix}-{n:03d}"] = f"{prefix}-{n:02d}"

    return renames, id_remap


def apply_replacements_pass1(content: str, sorted_remap: list[tuple[str, str]]) -> str:
    for old, new in sorted_remap:
        pattern = re.compile(r"(?<![A-Z0-9-])" + re.escape(old) + r"(?![\dA-Z])")
        content = pattern.sub(new, content)
    return content


def apply_replacements_pass2(content: str) -> str:
    """Catch-all sweep for legacy IDs that have no corresponding file."""
    def feat_4digit(m: re.Match[str]) -> str:
        num = m.group(1)
        suffix = m.group(2) or ""
        if len(num) == 4:
            return f"FEAT-{int(num[:2]):02d}-{int(num[2:]):02d}{suffix}"
        if len(num) == 3:
            return f"FEAT-{int(num[0]):02d}-{int(num[1:]):02d}{suffix}"
        return m.group(0)

    content = re.sub(r"\bFEATURE-(\d{3,4})([a-z]?)\b", feat_4digit, content)
    content = re.sub(r"\bFEATURE-(\d{2,3})-(\d{2,3})\b",
                     lambda m: f"FEAT-{int(m.group(1)):02d}-{int(m.group(2)):02d}",
                     content)
    content = re.sub(r"\bEPIC-(\d{3})\b",
                     lambda m: f"EPIC-{int(m.group(1)):02d}", content)
    content = re.sub(r"\bADR-(\d{3})\b",
                     lambda m: f"ADR-{int(m.group(1)):02d}", content)
    content = re.sub(r"\bPLAN-(\d{3})\b",
                     lambda m: f"PLAN-{int(m.group(1)):02d}", content)
    content = re.sub(r"\bBA-(\d{3})\b",
                     lambda m: f"BA-{int(m.group(1)):02d}", content)
    content = re.sub(r"\bEXPLORE-(\d{3})\b",
                     lambda m: f"EXPLORE-{int(m.group(1)):02d}", content)
    content = re.sub(r"\bRESEARCH-(\d{3})\b",
                     lambda m: f"RESEARCH-{int(m.group(1)):02d}", content)
    return content


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()

    renames, id_remap = collect_renames(root)
    sorted_remap = sorted(id_remap.items(), key=lambda x: -len(x[0]))

    print(f"Rename plan: {len(renames)} files")
    print(f"ID-remap entries: {len(id_remap)}")

    targets = list((root / "_devprocess").rglob("*.md")) if (root / "_devprocess").is_dir() else []
    arch_map = root / "src/ARCHITECTURE.map"
    if arch_map.is_file():
        targets.append(arch_map)

    skip = {root / "_devprocess/context/HANDOFFS.md"}

    pass1_count = 0
    for fp in targets:
        if fp in skip or not fp.is_file():
            continue
        original = fp.read_text(encoding="utf-8")
        updated = apply_replacements_pass1(original, sorted_remap)
        if updated != original:
            fp.write_text(updated, encoding="utf-8")
            pass1_count += 1
    print(f"Pass 1 (file-backed renames) updated {pass1_count} files")

    for old, new in renames:
        if old.exists():
            old.rename(new)
    print(f"Renamed {len(renames)} files")

    pass2_count = 0
    for fp in targets:
        if fp in skip or not fp.is_file():
            continue
        if not fp.exists():  # may have been renamed
            continue
        original = fp.read_text(encoding="utf-8")
        updated = apply_replacements_pass2(original)
        if updated != original:
            fp.write_text(updated, encoding="utf-8")
            pass2_count += 1
    print(f"Pass 2 (catch-all sweep) updated {pass2_count} files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
