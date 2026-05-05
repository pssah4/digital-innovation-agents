#!/usr/bin/env python3
"""
Pre-merge ID renumbering for parallel-developed feature branches.

When two feature branches independently allocate the same EPIC, FEAT,
IMP, or FIX id, merging the second one into dev produces a collision.
This script reads the target branch's BACKLOG.md, computes the maximum
id per class, and renumbers any colliding ids on the current source
branch so that they continue the target's sequence.

Modes
-----

  --target <branch>      target branch (default: dev)
  --source <branch>      source branch (default: HEAD; only used for
                         logging, the script always operates on the
                         current working tree)
  --check-only           exit 1 if any collision exists, else exit 0;
                         no changes
  --list-conflicts       print collisions and the proposed mapping as
                         JSON, no changes
  --dry-run              same as default but no file writes
  default                compute mapping, write a renumber-plan,
                         apply renames and reference updates,
                         print summary

The script touches:

- file names under
  `_devprocess/requirements/{epics,features,fixes,improvements}/`
- file names under `_devprocess/analysis/BA-{EPIC,FEAT,IMP,FIX}-*.md`
- frontmatter fields: `id`, `epic`, `feature`, `ba-ref`, `depends-on`,
  `feature-refs`, `adr-refs`, `supersedes`, `superseded-by`,
  `target-id`, `parent-feat`
- body references in `*.md` under `_devprocess/`
- `src/ARCHITECTURE.map` if present
- `FIXME(stub):` markers in the source tree (see graph-invariants
  E-14)

Skipped: `_devprocess/context/HANDOFFS.md` (append-only audit trail).
ADRs and PLANs are NOT renumbered (their ids are independent of the
EPIC/FEAT graph).

This script is project-agnostic, idempotent (running on an
already-aligned branch is a no-op), and exits non-zero on errors.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


# ---------- Repo and CLI plumbing ----------------------------------------


def find_repo_root() -> Path:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
        return Path(out)
    except Exception:
        return Path.cwd()


ROOT = find_repo_root()
DEV = ROOT / "_devprocess"
ANALYSIS = DEV / "analysis"
EPICS_DIR = DEV / "requirements/epics"
FEATS_DIR = DEV / "requirements/features"
FIXES_DIR = DEV / "requirements/fixes"
IMPS_DIR = DEV / "requirements/improvements"
BACKLOG = DEV / "context/BACKLOG.md"
HANDOFFS = DEV / "context/HANDOFFS.md"
ARCH_MAP = ROOT / "src/ARCHITECTURE.map"


# ---------- ID parsing ---------------------------------------------------


EPIC_RE = re.compile(r"\bEPIC-(\d{2,3})\b")
FEAT_RE = re.compile(r"\bFEAT-(\d{2,3})-(\d{2,3})([a-z]?)\b")
IMP_RE = re.compile(r"\bIMP-(\d{2,3})-(\d{2,3})-(\d{2,3})\b")
FIX_RE = re.compile(r"\bFIX-(\d{2,3})-(\d{2,3})-(\d{2,3})\b")


@dataclass(frozen=True)
class EpicId:
    ee: int

    def __str__(self) -> str:
        return f"EPIC-{self.ee:02d}"


@dataclass(frozen=True)
class FeatId:
    ee: int
    ff: int
    suffix: str = ""

    def __str__(self) -> str:
        return f"FEAT-{self.ee:02d}-{self.ff:02d}{self.suffix}"


@dataclass(frozen=True)
class ImpId:
    ee: int
    ff: int
    nn: int

    def __str__(self) -> str:
        return f"IMP-{self.ee:02d}-{self.ff:02d}-{self.nn:02d}"


@dataclass(frozen=True)
class FixId:
    ee: int
    ff: int
    nn: int

    def __str__(self) -> str:
        return f"FIX-{self.ee:02d}-{self.ff:02d}-{self.nn:02d}"


# ---------- Target branch parsing ---------------------------------------


def git_show(ref: str, path: str) -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "show", f"{ref}:{path}"],
            stderr=subprocess.DEVNULL,
            cwd=ROOT,
            text=True,
        )
        return out
    except subprocess.CalledProcessError:
        return None


def collect_target_ids(target: str) -> dict[str, set]:
    """Read the target branch's BACKLOG.md and collect all ids per
    class. Returns a dict with keys 'EPIC', 'FEAT', 'IMP', 'FIX'."""
    ids: dict[str, set] = {"EPIC": set(), "FEAT": set(), "IMP": set(), "FIX": set()}
    text = git_show(target, "_devprocess/context/BACKLOG.md")
    if text is None:
        return ids
    for m in EPIC_RE.finditer(text):
        ids["EPIC"].add(EpicId(int(m.group(1))))
    for m in FEAT_RE.finditer(text):
        ids["FEAT"].add(FeatId(int(m.group(1)), int(m.group(2)), m.group(3) or ""))
    for m in IMP_RE.finditer(text):
        ids["IMP"].add(ImpId(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    for m in FIX_RE.finditer(text):
        ids["FIX"].add(FixId(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return ids


# ---------- Artefact file parsing ---------------------------------------


def parse_artifact_path(path: str) -> tuple[str, object] | None:
    """Return the graph id carried by an artefact file path."""
    base = path.rsplit("/", 1)[-1]
    if path.startswith("_devprocess/requirements/epics/"):
        if base.endswith("-ba.md"):
            return None
        m = re.match(r"^EPIC-(\d+)-.+\.md$", base)
        if m:
            return ("EPIC", EpicId(int(m.group(1))))
    elif path.startswith("_devprocess/requirements/features/"):
        m = re.match(r"^FEAT-(\d+)-(\d+)([a-z]?)-.+\.md$", base)
        if m:
            return (
                "FEAT",
                FeatId(int(m.group(1)), int(m.group(2)), m.group(3) or ""),
            )
    elif path.startswith("_devprocess/requirements/improvements/"):
        m = re.match(r"^IMP-(\d+)-(\d+)-(\d+)-.+\.md$", base)
        if m:
            return ("IMP", ImpId(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    elif path.startswith("_devprocess/requirements/fixes/"):
        m = re.match(r"^FIX-(\d+)-(\d+)-(\d+)-.+\.md$", base)
        if m:
            return ("FIX", FixId(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    elif path.startswith("_devprocess/analysis/"):
        m = re.match(r"^BA-EPIC-(\d+)-.+\.md$", base)
        if m:
            return ("EPIC", EpicId(int(m.group(1))))
        m = re.match(r"^BA-FEAT-(\d+)-(\d+)([a-z]?)-.+\.md$", base)
        if m:
            return (
                "FEAT",
                FeatId(int(m.group(1)), int(m.group(2)), m.group(3) or ""),
            )
        m = re.match(r"^BA-IMP-(\d+)-(\d+)-(\d+)-.+\.md$", base)
        if m:
            return ("IMP", ImpId(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        m = re.match(r"^BA-FIX-(\d+)-(\d+)-(\d+)-.+\.md$", base)
        if m:
            return ("FIX", FixId(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return None


def empty_path_index() -> dict[str, dict[object, set[str]]]:
    return {"EPIC": {}, "FEAT": {}, "IMP": {}, "FIX": {}}


def add_path_id(
    index: dict[str, dict[object, set[str]]],
    kind: str,
    id_value: object,
    path: str,
) -> None:
    index.setdefault(kind, {}).setdefault(id_value, set()).add(path)


def path_index_to_ids(index: dict[str, dict[object, set[str]]]) -> dict[str, set]:
    return {
        kind: set(index.get(kind, {}).keys())
        for kind in ("EPIC", "FEAT", "IMP", "FIX")
    }


def collect_worktree_id_paths() -> dict[str, dict[object, set[str]]]:
    ids = empty_path_index()
    if not DEV.is_dir():
        return ids
    for fp in DEV.rglob("*.md"):
        try:
            rel = fp.relative_to(ROOT).as_posix()
        except ValueError:
            continue
        parsed = parse_artifact_path(rel)
        if parsed:
            kind, id_value = parsed
            add_path_id(ids, kind, id_value, rel)
    return ids


def collect_id_paths_from_ref(ref: str) -> dict[str, dict[object, set[str]]]:
    ids = empty_path_index()
    try:
        out = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", ref],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return ids
    for name in out.splitlines():
        parsed = parse_artifact_path(name)
        if parsed:
            kind, id_value = parsed
            add_path_id(ids, kind, id_value, name)
    return ids


def collect_source_owned_paths(
    source_index: dict[str, dict[object, set[str]]],
    target_index: dict[str, dict[object, set[str]]],
) -> set[str]:
    """Paths that belong to the source side of the merge.

    A file carrying the same id at the same path on target is an
    existing target artefact, not a new source artefact. The source
    side starts where the source tree has a path that target does not
    have for that same id.
    """
    owned: set[str] = set()
    for kind, by_id in source_index.items():
        target_by_id = target_index.get(kind, {})
        for id_value, paths in by_id.items():
            target_paths = target_by_id.get(id_value, set())
            owned.update(paths - target_paths)
    return owned


def filter_source_index(
    source_index: dict[str, dict[object, set[str]]],
    source_owned_paths: set[str],
) -> dict[str, dict[object, set[str]]]:
    filtered = empty_path_index()
    for kind, by_id in source_index.items():
        for id_value, paths in by_id.items():
            owned_paths = paths & source_owned_paths
            if owned_paths:
                filtered[kind][id_value] = owned_paths
    return filtered


def collect_changed_text_paths(target: str) -> set[str]:
    try:
        out = subprocess.check_output(
            [
                "git",
                "diff",
                "--name-only",
                "--diff-filter=ACMRT",
                f"{target}...HEAD",
            ],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return set()
    return {line for line in out.splitlines() if line}


# ---------- Source branch parsing ---------------------------------------


def collect_source_ids() -> dict[str, set]:
    """Source ids from the working tree filesystem. Used when the script
    runs on a checked-out source branch (the normal pre-merge-via-
    wrapper case).
    """
    return path_index_to_ids(collect_worktree_id_paths())


def collect_source_ids_from_ref(ref: str) -> dict[str, set]:
    """Source ids from a git ref's tree (used in the pre-merge-commit
    hook context, where the working tree already shows the merged
    state and is not a clean source view).

    Uses `git ls-tree` to enumerate files at the ref, then matches the
    same name patterns as `collect_source_ids`.
    """
    return path_index_to_ids(collect_id_paths_from_ref(ref))


# ---------- Mapping computation -----------------------------------------


@dataclass
class RenumberPlan:
    epic: dict[EpicId, EpicId] = field(default_factory=dict)
    feat: dict[FeatId, FeatId] = field(default_factory=dict)
    imp: dict[ImpId, ImpId] = field(default_factory=dict)
    fix: dict[FixId, FixId] = field(default_factory=dict)

    def empty(self) -> bool:
        return not (self.epic or self.feat or self.imp or self.fix)

    def to_json(self) -> dict:
        return {
            "epic": {str(k): str(v) for k, v in self.epic.items()},
            "feat": {str(k): str(v) for k, v in self.feat.items()},
            "imp": {str(k): str(v) for k, v in self.imp.items()},
            "fix": {str(k): str(v) for k, v in self.fix.items()},
        }


def compute_plan(target: dict[str, set], source: dict[str, set]) -> RenumberPlan:
    plan = RenumberPlan()

    # 1) EPIC collisions: any source EPIC id that exists on target
    target_epic_max = max((e.ee for e in target["EPIC"]), default=0)
    target_epics = set(target["EPIC"])
    next_epic = target_epic_max + 1
    sorted_source_epics = sorted(source["EPIC"], key=lambda e: e.ee)
    epic_map_int: dict[int, int] = {}
    for old in sorted_source_epics:
        if old in target_epics:
            new = EpicId(next_epic)
            plan.epic[old] = new
            epic_map_int[old.ee] = next_epic
            next_epic += 1
        else:
            # unchanged but tracked for FEAT/IMP/FIX dependents
            epic_map_int[old.ee] = old.ee

    # 2) FEAT collisions, scoped per epic. After epic remap, new ee
    #    is epic_map_int[old.ee]. Within that epic, find next free ff
    #    by inspecting target FEAT ids under the new ee.
    target_feats_by_epic: dict[int, set] = {}
    for f in target["FEAT"]:
        target_feats_by_epic.setdefault(f.ee, set()).add(f.ff)
    feat_map_int: dict[tuple[int, int, str], tuple[int, int, str]] = {}
    sorted_source_feats = sorted(source["FEAT"], key=lambda f: (f.ee, f.ff))
    for old in sorted_source_feats:
        new_ee = epic_map_int.get(old.ee, old.ee)
        existing_ffs = set(target_feats_by_epic.get(new_ee, set()))
        # also account for already-mapped source feats so we do not
        # collide within the source set itself
        for (mee, mff, _ms), (nee, nff, _ns) in feat_map_int.items():
            if nee == new_ee:
                existing_ffs.add(nff)
        if old.ee == new_ee and old.ff not in existing_ffs:
            # untouched
            feat_map_int[(old.ee, old.ff, old.suffix)] = (new_ee, old.ff, old.suffix)
            existing_ffs.add(old.ff)
            target_feats_by_epic.setdefault(new_ee, set()).add(old.ff)
            continue
        # need to find a new ff in new_ee
        new_ff = old.ff
        while new_ff in existing_ffs:
            new_ff += 1
        feat_map_int[(old.ee, old.ff, old.suffix)] = (new_ee, new_ff, old.suffix)
        target_feats_by_epic.setdefault(new_ee, set()).add(new_ff)
        if (new_ee, new_ff, old.suffix) != (old.ee, old.ff, old.suffix):
            plan.feat[old] = FeatId(new_ee, new_ff, old.suffix)

    # 3) IMP collisions, scoped per (ee, ff). Both ee and ff may have
    #    been remapped via epic_map_int and feat_map_int.
    target_imps_by_feat: dict[tuple[int, int], set] = {}
    for i in target["IMP"]:
        target_imps_by_feat.setdefault((i.ee, i.ff), set()).add(i.nn)
    sorted_source_imps = sorted(source["IMP"], key=lambda i: (i.ee, i.ff, i.nn))
    for old in sorted_source_imps:
        new_ee, new_ff, _ = feat_map_int.get(
            (old.ee, old.ff, ""),
            (epic_map_int.get(old.ee, old.ee), old.ff, ""),
        )
        existing_nns = set(target_imps_by_feat.get((new_ee, new_ff), set()))
        for (mee, mff, mnn), (nee, nff, nnn) in (
            (k, v) for k, v in plan.imp.items()
        ):
            pass  # placeholder, plan.imp uses ImpId keys, see below
        # account for source mappings already produced
        for nv in plan.imp.values():
            if (nv.ee, nv.ff) == (new_ee, new_ff):
                existing_nns.add(nv.nn)
        new_nn = old.nn
        if (old.ee, old.ff, old.nn) != (new_ee, new_ff, new_nn) or new_nn in existing_nns:
            while new_nn in existing_nns:
                new_nn += 1
        target_imps_by_feat.setdefault((new_ee, new_ff), set()).add(new_nn)
        if (new_ee, new_ff, new_nn) != (old.ee, old.ff, old.nn):
            plan.imp[old] = ImpId(new_ee, new_ff, new_nn)

    # 4) FIX collisions, scoped per (ee, ff)
    target_fixes_by_feat: dict[tuple[int, int], set] = {}
    for f in target["FIX"]:
        target_fixes_by_feat.setdefault((f.ee, f.ff), set()).add(f.nn)
    sorted_source_fixes = sorted(source["FIX"], key=lambda f: (f.ee, f.ff, f.nn))
    for old in sorted_source_fixes:
        new_ee, new_ff, _ = feat_map_int.get(
            (old.ee, old.ff, ""),
            (epic_map_int.get(old.ee, old.ee), old.ff, ""),
        )
        existing_nns = set(target_fixes_by_feat.get((new_ee, new_ff), set()))
        for nv in plan.fix.values():
            if (nv.ee, nv.ff) == (new_ee, new_ff):
                existing_nns.add(nv.nn)
        new_nn = old.nn
        if (old.ee, old.ff, old.nn) != (new_ee, new_ff, new_nn) or new_nn in existing_nns:
            while new_nn in existing_nns:
                new_nn += 1
        target_fixes_by_feat.setdefault((new_ee, new_ff), set()).add(new_nn)
        if (new_ee, new_ff, new_nn) != (old.ee, old.ff, old.nn):
            plan.fix[old] = FixId(new_ee, new_ff, new_nn)

    return plan


# ---------- Apply --------------------------------------------------------


def build_id_replacements(plan: RenumberPlan) -> list[tuple[re.Pattern, str]]:
    """Order matters: longer/more-specific patterns first to avoid
    partial matches (FEAT-04-02 must be replaced before EPIC-04)."""
    replacements: list[tuple[re.Pattern, str]] = []
    # FIX (longest)
    for old, new in plan.fix.items():
        replacements.append((re.compile(rf"\b{re.escape(str(old))}\b"), str(new)))
    for old, new in plan.imp.items():
        replacements.append((re.compile(rf"\b{re.escape(str(old))}\b"), str(new)))
    for old, new in plan.feat.items():
        replacements.append((re.compile(rf"\b{re.escape(str(old))}\b"), str(new)))
    for old, new in plan.epic.items():
        replacements.append((re.compile(rf"\b{re.escape(str(old))}\b"), str(new)))
    return replacements


def apply_text_replacements(text: str, replacements: list[tuple[re.Pattern, str]]) -> str:
    out = text
    for pat, rep in replacements:
        out = pat.sub(rep, out)
    return out


SOURCE_SUFFIXES = {
    ".ts", ".tsx", ".js", ".jsx", ".py", ".go",
    ".rs", ".java", ".cs", ".rb", ".swift", ".kt",
    ".sh", ".bash",
}


def path_can_carry_text_ref(path: str) -> bool:
    fp = Path(path)
    if path.startswith("_devprocess/") and fp.suffix.lower() == ".md":
        return True
    if path == "src/ARCHITECTURE.map":
        return True
    if path.startswith("src/") and fp.suffix.lower() in SOURCE_SUFFIXES:
        return True
    return False


def collect_text_targets(scope_paths: set[str] | None = None) -> list[Path]:
    """Files where IDs may appear in text (frontmatter or body)."""
    targets: list[Path] = []
    if scope_paths is not None:
        for rel in sorted(scope_paths):
            if not path_can_carry_text_ref(rel):
                continue
            fp = ROOT / rel
            if fp.is_file():
                targets.append(fp)
        return targets
    if DEV.is_dir():
        for fp in DEV.rglob("*.md"):
            if fp == HANDOFFS:
                continue
            targets.append(fp)
    if ARCH_MAP.is_file():
        targets.append(ARCH_MAP)
    src = ROOT / "src"
    if src.is_dir():
        for fp in src.rglob("*"):
            if fp.suffix.lower() in SOURCE_SUFFIXES and fp.is_file():
                targets.append(fp)
    return targets


def in_scope(fp: Path, scope_paths: set[str] | None) -> bool:
    if scope_paths is None:
        return True
    try:
        return fp.relative_to(ROOT).as_posix() in scope_paths
    except ValueError:
        return False


def collect_file_renames(
    plan: RenumberPlan,
    scope_paths: set[str] | None = None,
) -> list[tuple[Path, Path]]:
    """Build the rename list. Two-phase to avoid mid-rename collisions:
    rename to a temporary name, then to the final name."""
    renames: list[tuple[Path, Path]] = []

    # EPICs
    for old, new in plan.epic.items():
        for fp in EPICS_DIR.glob(f"EPIC-{old.ee:02d}-*.md"):
            if not in_scope(fp, scope_paths):
                continue
            new_name = fp.name.replace(f"EPIC-{old.ee:02d}-", f"EPIC-{new.ee:02d}-", 1)
            renames.append((fp, fp.parent / new_name))
        ba = ANALYSIS / f"BA-EPIC-{old.ee:02d}-*.md"
        for fp in ANALYSIS.glob(f"BA-EPIC-{old.ee:02d}-*.md"):
            if not in_scope(fp, scope_paths):
                continue
            new_name = fp.name.replace(
                f"BA-EPIC-{old.ee:02d}-", f"BA-EPIC-{new.ee:02d}-", 1
            )
            renames.append((fp, fp.parent / new_name))

    # FEATs
    for old, new in plan.feat.items():
        old_pref = f"FEAT-{old.ee:02d}-{old.ff:02d}{old.suffix}-"
        new_pref = f"FEAT-{new.ee:02d}-{new.ff:02d}{new.suffix}-"
        for fp in FEATS_DIR.glob(f"{old_pref}*.md"):
            if not in_scope(fp, scope_paths):
                continue
            renames.append((fp, fp.parent / fp.name.replace(old_pref, new_pref, 1)))
        old_ba = f"BA-FEAT-{old.ee:02d}-{old.ff:02d}{old.suffix}-"
        new_ba = f"BA-FEAT-{new.ee:02d}-{new.ff:02d}{new.suffix}-"
        for fp in ANALYSIS.glob(f"{old_ba}*.md"):
            if not in_scope(fp, scope_paths):
                continue
            renames.append((fp, fp.parent / fp.name.replace(old_ba, new_ba, 1)))

    # IMPs
    for old, new in plan.imp.items():
        old_pref = f"IMP-{old.ee:02d}-{old.ff:02d}-{old.nn:02d}-"
        new_pref = f"IMP-{new.ee:02d}-{new.ff:02d}-{new.nn:02d}-"
        for fp in IMPS_DIR.glob(f"{old_pref}*.md"):
            if not in_scope(fp, scope_paths):
                continue
            renames.append((fp, fp.parent / fp.name.replace(old_pref, new_pref, 1)))
        old_ba = f"BA-IMP-{old.ee:02d}-{old.ff:02d}-{old.nn:02d}-"
        new_ba = f"BA-IMP-{new.ee:02d}-{new.ff:02d}-{new.nn:02d}-"
        for fp in ANALYSIS.glob(f"{old_ba}*.md"):
            if not in_scope(fp, scope_paths):
                continue
            renames.append((fp, fp.parent / fp.name.replace(old_ba, new_ba, 1)))

    # FIXes
    for old, new in plan.fix.items():
        old_pref = f"FIX-{old.ee:02d}-{old.ff:02d}-{old.nn:02d}-"
        new_pref = f"FIX-{new.ee:02d}-{new.ff:02d}-{new.nn:02d}-"
        for fp in FIXES_DIR.glob(f"{old_pref}*.md"):
            if not in_scope(fp, scope_paths):
                continue
            renames.append((fp, fp.parent / fp.name.replace(old_pref, new_pref, 1)))
        old_ba = f"BA-FIX-{old.ee:02d}-{old.ff:02d}-{old.nn:02d}-"
        new_ba = f"BA-FIX-{new.ee:02d}-{new.ff:02d}-{new.nn:02d}-"
        for fp in ANALYSIS.glob(f"{old_ba}*.md"):
            if not in_scope(fp, scope_paths):
                continue
            renames.append((fp, fp.parent / fp.name.replace(old_ba, new_ba, 1)))

    return renames


def two_phase_rename(renames: list[tuple[Path, Path]]) -> None:
    """Phase 1: rename to .renumber-tmp.{idx}. Phase 2: rename to final.
    Avoids the case where two ids swap and the second rename overwrites
    the first."""
    tmp_pairs: list[tuple[Path, Path]] = []
    for idx, (old, _) in enumerate(renames):
        if not old.exists():
            continue
        tmp = old.with_name(old.name + f".renumber-tmp.{idx}")
        old.rename(tmp)
        tmp_pairs.append((tmp, renames[idx][1]))
    for tmp, new in tmp_pairs:
        new.parent.mkdir(parents=True, exist_ok=True)
        tmp.rename(new)


def apply_plan(
    plan: RenumberPlan,
    dry_run: bool = False,
    scope_paths: set[str] | None = None,
) -> dict[str, int]:
    stats = {"text_files_changed": 0, "files_renamed": 0}
    if plan.empty():
        return stats

    replacements = build_id_replacements(plan)

    # 1. text replacements (frontmatter + body + ARCH_MAP + source)
    targets = collect_text_targets(scope_paths)
    for fp in targets:
        try:
            original = fp.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        updated = apply_text_replacements(original, replacements)
        if updated != original:
            stats["text_files_changed"] += 1
            if not dry_run:
                fp.write_text(updated, encoding="utf-8")

    # 2. file renames
    renames = collect_file_renames(plan, scope_paths)
    stats["files_renamed"] = len(renames)
    if not dry_run:
        two_phase_rename(renames)

    return stats


# ---------- Main ---------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default="dev",
                        help="target branch to align with (default: dev)")
    parser.add_argument("--source", default="HEAD",
                        help="source branch label, for logging (default: HEAD)")
    parser.add_argument("--source-ref", default=None,
                        help=(
                            "git ref to read source ids from (default: "
                            "scan the working tree). Pass a ref name "
                            "such as MERGE_HEAD when running inside "
                            "the pre-merge-commit hook."
                        ))
    parser.add_argument("--check-only", action="store_true",
                        help="exit 1 if collisions exist, else 0; no changes")
    parser.add_argument("--list-conflicts", action="store_true",
                        help="print collisions as JSON, no changes")
    parser.add_argument("--dry-run", action="store_true",
                        help="compute and apply replacements in-memory, no writes")
    parser.add_argument("--quiet", action="store_true",
                        help="suppress non-error output (for hooks)")
    parser.add_argument("--check-tree-duplicates", action="store_true",
                        help=(
                            "post-merge sanity: scan the working tree "
                            "and exit 1 if more than one artefact file "
                            "carries the same id (slug differs). "
                            "Used by pre-merge-commit hook because at "
                            "that stage MERGE_HEAD is not reliable."
                        ))
    args = parser.parse_args()

    if not DEV.is_dir():
        if not args.quiet:
            print("No _devprocess/ found; nothing to renumber.")
        return 0

    if args.check_tree_duplicates:
        # Scan the working tree for two files sharing the same id.
        from collections import defaultdict
        seen: dict[str, list[str]] = defaultdict(list)
        scan_dirs = [
            (EPICS_DIR, re.compile(r"^(EPIC-\d+)-(?!ba\.md$).+\.md$")),
            (FEATS_DIR, re.compile(r"^(FEAT-\d+-\d+[a-z]?)-.+\.md$")),
            (IMPS_DIR, re.compile(r"^(IMP-\d+-\d+-\d+)-.+\.md$")),
            (FIXES_DIR, re.compile(r"^(FIX-\d+-\d+-\d+)-.+\.md$")),
        ]
        for d, pat in scan_dirs:
            if not d.is_dir():
                continue
            for fp in d.iterdir():
                m = pat.match(fp.name)
                if m:
                    seen[m.group(1)].append(fp.name)
        duplicates = {k: v for k, v in seen.items() if len(v) > 1}
        if duplicates:
            if not args.quiet:
                print("ID duplicate(s) in working tree:")
                for k, files in duplicates.items():
                    print(f"  {k}: {', '.join(files)}")
            return 1
        return 0

    # --source-ref reads ids from a git tree; it is only safe with
    # check-only / list-conflicts modes since the working tree is not
    # the source view in that scenario.
    if args.source_ref and not (
        args.check_only or args.list_conflicts or args.dry_run
    ):
        print(
            "ERROR: --source-ref is only supported with --check-only, "
            "--list-conflicts, or --dry-run.",
            file=sys.stderr,
        )
        return 2

    target_ids = collect_target_ids(args.target)
    target_index = collect_id_paths_from_ref(args.target)
    if args.source_ref:
        source_index = collect_id_paths_from_ref(args.source_ref)
    else:
        source_index = collect_worktree_id_paths()

    source_owned_paths = collect_source_owned_paths(source_index, target_index)
    source_index = filter_source_index(source_index, source_owned_paths)
    source_ids = path_index_to_ids(source_index)
    plan = compute_plan(target_ids, source_ids)

    if args.check_only:
        return 1 if not plan.empty() else 0

    if args.list_conflicts:
        print(json.dumps({
            "target": args.target,
            "source": args.source,
            "mapping": plan.to_json(),
        }, indent=2))
        return 0

    if plan.empty():
        if not args.quiet:
            print(
                f"No id collisions between {args.source} and {args.target}."
            )
        return 0

    if not args.quiet:
        print(
            f"Renumber plan ({args.source} -> aligned with {args.target}):"
        )
        for cat, mapping in plan.to_json().items():
            for old, new in mapping.items():
                print(f"  {cat}: {old} -> {new}")

    changed_text_paths = set()
    if not args.source_ref:
        changed_text_paths = collect_changed_text_paths(args.target)
    scope_paths = source_owned_paths | changed_text_paths
    stats = apply_plan(plan, dry_run=args.dry_run, scope_paths=scope_paths)
    if not args.quiet:
        action = "would change" if args.dry_run else "changed"
        print(
            f"\n{stats['text_files_changed']} files {action} (text refs), "
            f"{stats['files_renamed']} files renamed."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
