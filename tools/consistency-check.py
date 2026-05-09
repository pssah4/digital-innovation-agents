#!/usr/bin/env python3
"""
Consistency-check Mode A (syntactic) for projects that follow the
Digital Innovation Agents (DIA) V-Model artefact conventions.

This script is project-agnostic. Auto-detects the repository root via
`git rev-parse --show-toplevel`. Expects the standard DIA layout:

    <root>/
      _devprocess/
        analysis/        BAs, EXPLOREs, RESEARCHs, AUDITs
        architecture/    ADR-NN-*.md, arc42.md
        requirements/
          epics/         EPIC-NN-*.md
          features/      FEAT-EE-FF-*.md
          fixes/         FIX-EE-FF-NN-*.md
          improvements/  IMP-EE-FF-NN-*.md
        implementation/
          plans/         PLAN-NN-*.md
        context/
          BACKLOG.md     single source of truth for status
          HANDOFFS.md    append-only phase-transition log (optional)
          METRICS.md     signal layer (optional)
        rules/           technical.md, design.md, domain.md (optional)
      src/               source code (optional, code projects only)
        ARCHITECTURE.map concept -> entry-file -> ADR map (optional)

Modes:
  --check        run all invariants, print findings, exit 1 on findings
  --fix          run all invariants, auto-fix safe drift, write
                 .git/consistency-check.last-run.json with remaining findings,
                 exit 1 only if non-auto-fixable findings remain.
  (default)      same as --check

Findings are written as JSON to .git/consistency-check.last-run.json so
Mode C (interactive fix-loop, in the consistency-check skill) can resume
them.

This script is the syntactic layer (Mode A). It does not call an LLM.
Mode B (semantic, agent-based) and Mode C (interactive fix loop) are
orchestrated by the consistency-check skill in Claude Code.

Optional configuration in <root>/dia.config.json:
    {
        "devprocess_dir": "_devprocess",   // default
        "src_dir": "src",                  // default; null to disable ADR-map check
        "skip_dead_link_paths": []         // glob-style, optional allowlist
    }
"""
from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Iterable

DEFAULTS = {
    "devprocess_dir": "_devprocess",
    "src_dir": "src",
    "skip_dead_link_paths": [],
}


def find_repo_root() -> Path:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
        return Path(out)
    except Exception:
        return Path.cwd()


def load_config(root: Path) -> dict:
    cfg_path = root / "dia.config.json"
    cfg = dict(DEFAULTS)
    if cfg_path.exists():
        try:
            cfg.update(json.loads(cfg_path.read_text(encoding="utf-8")))
        except Exception:
            pass
    return cfg


ROOT = find_repo_root()
CONFIG = load_config(ROOT)
DEV = ROOT / CONFIG["devprocess_dir"]
ARCHITECTURE = DEV / "architecture"
REQUIREMENTS = DEV / "requirements"
FEATURES = REQUIREMENTS / "features"
EPICS = REQUIREMENTS / "epics"
FIXES = REQUIREMENTS / "fixes"
IMPROVEMENTS = REQUIREMENTS / "improvements"
PLANS = DEV / "implementation" / "plans"
ANALYSIS = DEV / "analysis"
HANDOFF_DIR = REQUIREMENTS / "handoff"
ARCHITECT_HANDOFF = HANDOFF_DIR / "architect-handoff.md"
CONTEXT = DEV / "context"
BACKLOG = CONTEXT / "BACKLOG.md"
ARCH_MAP = (ROOT / CONFIG["src_dir"] / "ARCHITECTURE.map") if CONFIG.get("src_dir") else None
LAST_RUN = ROOT / ".git" / "consistency-check.last-run.json"

SEVERITY_HIGH = "high"
SEVERITY_MEDIUM = "medium"
SEVERITY_LOW = "low"


@dataclass
class Finding:
    type: str
    severity: str
    file: str
    line: int | None
    message: str
    suggestions: list[str] = field(default_factory=list)
    status: str = "unresolved"  # unresolved | fixed | skipped


def md_files(*dirs: Path) -> list[Path]:
    out: list[Path] = []
    for d in dirs:
        if d.exists():
            out.extend(sorted(d.rglob("*.md")))
    return out


# ---------- Auto-fixers ----------------------------------------------------

PURE_STATUS = re.compile(
    r"^>\s*\*\*Status\*\*:\s*"
    r"(Implemented|Implementiert|Geplant|Released|Done|"
    r"In Arbeit|Zur[uü]eckgestellt|Vollst[aä]ndig\s+implementiert)"
    r"\s*(\([^)]*\))?\s*$"
)
ANY_STATUS = re.compile(r"^>\s*\*\*Status\*\*:\s*(.*)$")
YAML_STATUS = re.compile(r"^(status|phase)\s*:\s*(.+)$", re.IGNORECASE)

# Reverse-engineering markers that the autofix must keep. When
# /reverse-engineering writes `status: Anticipated (not yet
# validated)` or `status: Observed (not validated)` into Epic /
# Feature frontmatter, that field is allowed by graph-invariants
# N-10/N-11 until /business-analysis validates the artefact. The
# autofix would otherwise silently delete them.
RE_MARKER_RE = re.compile(
    r"^\s*(Anticipated|Observed|Inferred|Draft\s*\(reverse-engineered)\b",
    re.IGNORECASE,
)


def is_reverse_engineering_marker(yaml_status_match: re.Match) -> bool:
    """True when a YAML status/phase line carries a reverse-engineering
    marker that the autofix must preserve.
    """
    value = yaml_status_match.group(2).strip()
    return bool(RE_MARKER_RE.match(value))


def autofix_status_duplicates(files: Iterable[Path]) -> int:
    """Remove `> **Status**: ...` and YAML `status:`/`phase:` duplicates.
    Substantive Status lines (DEPRECATED + reason, Subsumed-by) become
    `> **Note**: ...` so substance survives.
    """
    fixed = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        out: list[str] = []
        in_yaml = False
        changed = False
        for i, line in enumerate(text.splitlines(keepends=True)):
            stripped = line.rstrip("\n")
            if i == 0 and stripped == "---":
                in_yaml = True
                out.append(line)
                continue
            if in_yaml and stripped == "---":
                in_yaml = False
                out.append(line)
                continue
            if in_yaml:
                m_yaml = YAML_STATUS.match(stripped)
                if m_yaml:
                    if is_reverse_engineering_marker(m_yaml):
                        # Preserve RE markers, see graph-invariants N-10/N-11.
                        out.append(line)
                    else:
                        changed = True
                    continue
            if PURE_STATUS.match(stripped):
                changed = True
                continue
            m = ANY_STATUS.match(stripped)
            if m:
                out.append(f"> **Note**: {m.group(1).strip()}\n")
                changed = True
                continue
            out.append(line)
        if changed:
            f.write_text("".join(out), encoding="utf-8")
            fixed += 1
    return fixed


# ---------- Invariant checks -----------------------------------------------

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
SCHEME_RE = re.compile(r"^[a-z][a-z0-9+.-]*:")


def internal_prefixes(cfg: dict) -> tuple[str, ...]:
    parts = [cfg["devprocess_dir"] + "/"]
    if cfg.get("src_dir"):
        parts.append(cfg["src_dir"] + "/")
    parts.extend(("docs/", "scripts/", "tools/"))
    return tuple(parts)


def check_dead_links(files: Iterable[Path]) -> list[Finding]:
    out: list[Finding] = []
    prefixes = internal_prefixes(CONFIG)
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        in_code_block = False
        for ln, line in enumerate(text.splitlines(), start=1):
            stripped = line.lstrip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            for _, target in LINK_RE.findall(line):
                target_clean = target.split("#")[0].strip()
                if not target_clean:
                    continue
                if SCHEME_RE.match(target_clean):
                    continue
                if target_clean.startswith(prefixes):
                    candidate = ROOT / target_clean
                elif target_clean.startswith(("./", "../")):
                    candidate = (f.parent / target_clean).resolve()
                else:
                    continue
                if not candidate.exists():
                    out.append(Finding(
                        type="dead-link",
                        severity=SEVERITY_MEDIUM,
                        file=str(f.relative_to(ROOT)),
                        line=ln,
                        message=f"Link target does not exist: {target_clean}",
                        suggestions=[
                            "Remove the link if the target was never created",
                            "Mark planned with a FEAT-ref if the target is upcoming",
                            "Correct the path if the file was renamed or moved",
                        ],
                    ))
    return out


CODE_PATH_RE_TEMPLATE = r"`({src}/[^`\s]+\.[a-z]+)(?::\d+(?:-\d+)?)?`"
ADR_CORE_HEADERS = ("## Kontext", "## Context", "## Entscheidung", "## Decision",
                    "## Konsequenzen", "## Consequences", "## Begruendung",
                    "## Begründung", "## Considered Options")


def check_adr_abstraction(adr_files: Iterable[Path]) -> list[Finding]:
    """Code paths in ADR core sections are not allowed -- they age fast.
    Skipped entirely if the project has no `src_dir` configured.
    """
    if not CONFIG.get("src_dir"):
        return []
    code_path_re = re.compile(CODE_PATH_RE_TEMPLATE.format(src=re.escape(CONFIG["src_dir"])))
    out: list[Finding] = []
    for f in adr_files:
        text = f.read_text(encoding="utf-8")
        in_core = False
        for ln, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("## "):
                in_core = stripped in ADR_CORE_HEADERS
                continue
            if not in_core:
                continue
            for m in code_path_re.finditer(line):
                out.append(Finding(
                    type="adr-abstraction-violation",
                    severity=SEVERITY_MEDIUM,
                    file=str(f.relative_to(ROOT)),
                    line=ln,
                    message=f"Code path in ADR core section: {m.group(1)}",
                    suggestions=[
                        f"Move '{m.group(1)}' to the '## Implementation Notes (may go stale)' appendix",
                        f"Move the path to {CONFIG['src_dir']}/ARCHITECTURE.map and reference the concept name",
                        "Replace the path with the abstract concept (e.g. 'the pipeline')",
                    ],
                ))
    return out


BACKLOG_ROW_RE = re.compile(r"^\|\s*([A-Z]+(?:-\d+){1,3})\s*\|", re.MULTILINE)
BACKLOG_EPIC_HEADER_RE = re.compile(r"^###\s+(EPIC-\d{2})", re.MULTILINE)


def parse_backlog_ids() -> set[str]:
    """All artifact IDs known to the backlog. Epics may live as
    `### EPIC-NN: ...` headings (intentional) or as table rows. Other
    artifacts (FEAT, ADR, PLAN, FIX, IMP) live as table rows.
    """
    if not BACKLOG.exists():
        return set()
    text = BACKLOG.read_text(encoding="utf-8")
    return set(BACKLOG_ROW_RE.findall(text)) | set(BACKLOG_EPIC_HEADER_RE.findall(text))


ID_PATTERNS = [
    ("FIX", re.compile(r"^(FIX-\d{2}-\d{2}-\d{2})(?:-|$)")),
    ("IMP", re.compile(r"^(IMP-\d{2}-\d{2}-\d{2})(?:-|$)")),
    ("FEAT", re.compile(r"^(FEAT-\d{2}-\d{2})(?:-|$)")),
    ("EPIC", re.compile(r"^(EPIC-\d{2})(?:-|$)")),
    ("ADR", re.compile(r"^(ADR-\d{2})(?:-|$)")),
    ("PLAN", re.compile(r"^(PLAN-\d{2})(?:-|$)")),
]


def parse_artifact_id(p: Path) -> str | None:
    stem = p.stem
    for _, rx in ID_PATTERNS:
        m = rx.match(stem)
        if m:
            return m.group(1)
    return None


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
YAML_FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.+?)\s*$", re.MULTILINE)


def parse_frontmatter(path: Path) -> dict[str, str]:
    """Minimal YAML frontmatter scanner. Returns flat key->value strings.
    Only top-level scalar fields, no nesting, no lists. Sufficient for
    the handful of fields N-17 looks at (`status`, `ba-ref`,
    `project-ba-ref`).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out: dict[str, str] = {}
    for fm in YAML_FIELD_RE.finditer(m.group(1)):
        key = fm.group(1).strip().lower()
        val = fm.group(2).strip().strip("\"'")
        out[key] = val
    return out


DRAFT_STATUS_RE = re.compile(r"^Draft(?:\s*\(.*\))?$", re.IGNORECASE)


def check_status_coherence() -> list[Finding]:
    """N-17: BA must not stay at Draft once architect-handoff exists.
    Applies to every BA file in analysis/ (Project-BA `BA-{PROJECT}.md`
    and Item-BAs `BA-EPIC-*.md`, `BA-FEAT-*.md`, `BA-IMP-*.md`,
    `BA-FIX-*.md`). Conservative implementation: BA-side only, file-
    existence signal. ADR-side check (Proposed ADR with Building/
    Released Feature) requires backlog phase parsing and is left to
    the skill orchestration layer.
    """
    if not ANALYSIS.exists():
        return []
    handoff_present = ARCHITECT_HANDOFF.exists()
    if not handoff_present:
        return []
    out: list[Finding] = []
    for ba_path in sorted(ANALYSIS.glob("BA-*.md")):
        fm = parse_frontmatter(ba_path)
        status = fm.get("status", "")
        if not DRAFT_STATUS_RE.match(status):
            continue
        out.append(Finding(
            type="status-coherence-breach",
            severity=SEVERITY_LOW,
            file=str(ba_path.relative_to(ROOT)),
            line=None,
            message=(
                f"BA at status '{status}' but architect-handoff.md exists; "
                f"BA was exercised through RE without status promotion."
            ),
            suggestions=[
                "Run /requirements-engineering once more, accept the BA promotion prompt at handoff",
                "Run /business-analysis Validation Mode to walk the BA explicitly",
                "Defer: file as backlog item with Source=CONSISTENCY-CHECK",
            ],
        ))
    return out


ACTIVATION_PATH_HEADER_RE = re.compile(r"^##\s+Activation Path\s*$", re.MULTILINE)
ACTIVATION_TYPE_RE = re.compile(r"^[-*]\s*Type\s*:\s*(.+?)\s*$", re.MULTILINE)
ACTIVATION_ID_RE = re.compile(r"^[-*]\s*Identifier\s*:\s*(.+?)\s*$", re.MULTILINE)


def _backlog_done_features() -> set[str]:
    """FEATURE IDs whose backlog row carries status 'Done'.
    Best-effort parse: a row that contains the FEAT-ID and the literal
    'Done' status token. False positives are bounded because the row
    must lead with the FEAT-ID at the start of a markdown table cell.
    """
    if not BACKLOG.exists():
        return set()
    out: set[str] = set()
    text = BACKLOG.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = re.match(r"^\|\s*(FEAT-\d{2}-\d{2})\s*\|", line)
        if not m:
            continue
        if "Done" in line:
            out.add(m.group(1))
    return out


def check_feature_activation_path() -> list[Finding]:
    """N-18: every FEATURE with backlog status Done has a non-empty
    `## Activation Path` section with Type and Identifier filled.
    FEATUREs without `subtype:` in frontmatter are exempt for backwards
    compatibility.
    """
    if not FEATURES.exists():
        return []
    done_ids = _backlog_done_features()
    if not done_ids:
        return []
    out: list[Finding] = []
    for feat_path in sorted(FEATURES.glob("FEAT-*.md")):
        feat_id = parse_artifact_id(feat_path)
        if feat_id not in done_ids:
            continue
        fm = parse_frontmatter(feat_path)
        if "subtype" not in fm:
            continue  # backwards-compat: pre-N-18 FEATUREs exempt
        try:
            text = feat_path.read_text(encoding="utf-8")
        except Exception:
            continue
        header_m = ACTIVATION_PATH_HEADER_RE.search(text)
        if not header_m:
            out.append(Finding(
                type="feature-activation-path-missing",
                severity=SEVERITY_MEDIUM,
                file=str(feat_path.relative_to(ROOT)),
                line=None,
                message=(
                    f"FEATURE {feat_id} (subtype={fm.get('subtype', 'user-facing')}) "
                    f"is Done in backlog but has no '## Activation Path' section."
                ),
                suggestions=[
                    "Open /requirements-engineering to add the Activation Path entry",
                    "Demote FEATURE backlog status from Done to Active",
                    "Defer: file as backlog item with Source=CONSISTENCY-CHECK",
                ],
            ))
            continue
        section = text[header_m.end():]
        next_h2 = re.search(r"^##\s+\S", section, re.MULTILINE)
        section = section[:next_h2.start()] if next_h2 else section
        type_m = ACTIVATION_TYPE_RE.search(section)
        id_m = ACTIVATION_ID_RE.search(section)
        type_val = (type_m.group(1).strip() if type_m else "").strip("`")
        id_val = (id_m.group(1).strip() if id_m else "").strip("`")
        if not type_val or type_val.startswith("{") or not id_val or id_val.startswith("{"):
            out.append(Finding(
                type="feature-activation-path-missing",
                severity=SEVERITY_MEDIUM,
                file=str(feat_path.relative_to(ROOT)),
                line=header_m.start() and text[:header_m.start()].count("\n") + 1,
                message=(
                    f"FEATURE {feat_id} '## Activation Path' section is present "
                    f"but Type or Identifier is missing or unfilled (placeholder)."
                ),
                suggestions=[
                    "Fill 'Type:' and 'Identifier:' with the concrete activation entry",
                    "Demote FEATURE backlog status from Done to Active",
                    "Skip with reason in Mode C",
                ],
            ))
    return out


FIXME_STUB_RE = re.compile(
    r"(?://|#)\s*FIXME\(stub\)\s*:\s*(.+?)(?:\s+--\s+see\s+(FIX-\d{2}-\d{2}-\d{2}))?\s*$",
    re.MULTILINE,
)


def _backlog_fix_rows_with_stub_notes() -> dict[str, str]:
    """Map FIX-ID -> first matching backlog line for FIX-rows that
    document a stub. Triggered by 'Wiring offen', 'stub', or
    'deferred-stub' anywhere in the row.
    """
    if not BACKLOG.exists():
        return {}
    out: dict[str, str] = {}
    text = BACKLOG.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = re.match(r"^\|\s*(FIX-\d{2}-\d{2}-\d{2})\s*\|", line)
        if not m:
            continue
        low = line.lower()
        if "wiring offen" in low or "stub" in low or "deferred-stub" in low:
            out[m.group(1)] = line
    return out


def _src_files() -> list[Path]:
    if not CONFIG.get("src_dir"):
        return []
    src_root = ROOT / CONFIG["src_dir"]
    if not src_root.is_dir():
        return []
    out: list[Path] = []
    for ext in ("*.ts", "*.tsx", "*.js", "*.jsx", "*.py", "*.go",
                "*.rs", "*.r", "*.R", "*.sh"):
        out.extend(src_root.rglob(ext))
    return sorted(out)


def check_stub_fix_binding() -> list[Finding]:
    """E-14: bidirectional binding between FIXME(stub) markers and FIX
    rows. Two finding types: stub-without-fix-row (marker references
    missing or resolved FIX-ID) and fix-without-stub-evidence (FIX-row
    documents a stub but no marker references it).
    """
    src_files = _src_files()
    backlog_stub_fixes = _backlog_fix_rows_with_stub_notes()
    referenced_fix_ids: set[str] = set()
    backlog_ids = parse_backlog_ids()
    out: list[Finding] = []

    for sf in src_files:
        try:
            text = sf.read_text(encoding="utf-8")
        except Exception:
            continue
        for ln, line in enumerate(text.splitlines(), start=1):
            m = FIXME_STUB_RE.search(line)
            if not m:
                continue
            fix_id = m.group(2)
            if not fix_id:
                out.append(Finding(
                    type="stub-without-fix-row",
                    severity=SEVERITY_LOW,
                    file=str(sf.relative_to(ROOT)),
                    line=ln,
                    message=(
                        "FIXME(stub) marker without 'see FIX-{ee}-{ff}-{nn}' reference; "
                        "every stub MUST point at a backlog FIX row."
                    ),
                    suggestions=[
                        "Open /coding to create the missing FIX-row and embed the ID in the marker",
                        "Remove the marker if the stub has been resolved",
                    ],
                ))
                continue
            referenced_fix_ids.add(fix_id)
            if fix_id not in backlog_ids:
                out.append(Finding(
                    type="stub-without-fix-row",
                    severity=SEVERITY_LOW,
                    file=str(sf.relative_to(ROOT)),
                    line=ln,
                    message=(
                        f"FIXME(stub) marker references {fix_id} but no such FIX exists in backlog."
                    ),
                    suggestions=[
                        f"Add a backlog row for {fix_id}",
                        "Update the marker to reference the correct FIX-ID",
                        "Remove the marker if the stub has been resolved",
                    ],
                ))

    for fix_id in backlog_stub_fixes:
        if fix_id in referenced_fix_ids:
            continue
        out.append(Finding(
            type="fix-without-stub-evidence",
            severity=SEVERITY_LOW,
            file=str(BACKLOG.relative_to(ROOT)),
            line=None,
            message=(
                f"FIX-row {fix_id} documents a stub (notes contain 'Wiring offen' / 'stub' / "
                f"'deferred-stub') but no FIXME(stub) marker in the source tree references it."
            ),
            suggestions=[
                "Open /coding to add the FIXME(stub) marker at the stubbed location",
                "Resolve the FIX-row if the stub is gone (set status Done in the backlog)",
                "Edit the row's notes if 'stub' was a false positive",
            ],
        ))
    return out


ITEM_BA_PATTERNS = {
    "EPIC": (re.compile(r"^BA-EPIC-(\d{2})-(.+)\.md$"), EPICS, "EPIC-{ee:02d}-"),
    "FEAT": (
        re.compile(r"^BA-FEAT-(\d{2})-(\d{2})([a-z]?)-(.+)\.md$"),
        FEATURES,
        "FEAT-{ee:02d}-{ff:02d}{suffix}-",
    ),
    "IMP": (
        re.compile(r"^BA-IMP-(\d{2})-(\d{2})-(\d{2})-(.+)\.md$"),
        IMPROVEMENTS,
        "IMP-{ee:02d}-{ff:02d}-{nn:02d}-",
    ),
    "FIX": (
        re.compile(r"^BA-FIX-(\d{2})-(\d{2})-(\d{2})-(.+)\.md$"),
        FIXES,
        "FIX-{ee:02d}-{ff:02d}-{nn:02d}-",
    ),
}


def check_item_ba_frontmatter() -> list[Finding]:
    """N-8: every Item-BA carries `project-ba-ref:` (path or `null`).
    Persona definitions inside the Item-BA are flagged when
    `project-ba-ref:` is set (the Item-BA must reference, not redefine).
    Conservative: we only enforce the frontmatter field. Persona-
    redefinition detection lives in Mode B.
    """
    if not ANALYSIS.exists():
        return []
    out: list[Finding] = []
    for ba_path in sorted(ANALYSIS.glob("BA-*.md")):
        if ba_path.name == "BA-{PROJECT}.md":
            continue
        if not any(
            ba_path.name.startswith(f"BA-{kind}-") for kind in ITEM_BA_PATTERNS
        ):
            # Project-BA singleton or legacy generic BA: skip N-8.
            continue
        fm = parse_frontmatter(ba_path)
        if "project-ba-ref" not in fm:
            out.append(Finding(
                type="item-ba-missing-project-ba-ref",
                severity=SEVERITY_LOW,
                file=str(ba_path.relative_to(ROOT)),
                line=None,
                message=(
                    "Item-BA frontmatter has no `project-ba-ref:`. "
                    "Set the path to the Project-BA, or `null` if no "
                    "Project-BA exists."
                ),
                suggestions=[
                    "Add `project-ba-ref: ../analysis/BA-{PROJECT}.md` to the frontmatter",
                    "Add `project-ba-ref: null` if this is a single-item project",
                ],
            ))
    return out


def check_ba_ref_bidirectional() -> list[Finding]:
    """N-9: each Item-BA's filename matches a backlog item, and each
    EPIC/FEAT artefact for which an Item-BA exists carries `ba-ref:` in
    its frontmatter pointing at the BA file. IMP/FIX BAs are optional;
    when a BA file exists, the artefact must still link it.
    """
    if not ANALYSIS.exists():
        return []
    out: list[Finding] = []
    for kind, (pattern, target_dir, target_prefix_template) in ITEM_BA_PATTERNS.items():
        if not target_dir.exists():
            continue
        for ba_path in sorted(ANALYSIS.glob(f"BA-{kind}-*.md")):
            m = pattern.match(ba_path.name)
            if not m:
                continue
            if kind == "EPIC":
                ee = int(m.group(1))
                target_glob = f"EPIC-{ee:02d}-*.md"
            elif kind == "FEAT":
                ee, ff = int(m.group(1)), int(m.group(2))
                suffix = m.group(3) or ""
                target_glob = f"FEAT-{ee:02d}-{ff:02d}{suffix}-*.md"
            else:
                ee, ff, nn = (
                    int(m.group(1)),
                    int(m.group(2)),
                    int(m.group(3)),
                )
                target_glob = f"{kind}-{ee:02d}-{ff:02d}-{nn:02d}-*.md"
            matches = list(target_dir.glob(target_glob))
            if not matches:
                out.append(Finding(
                    type="orphan-item-ba",
                    severity=SEVERITY_LOW,
                    file=str(ba_path.relative_to(ROOT)),
                    line=None,
                    message=(
                        f"Item-BA file has no matching {kind} artefact "
                        f"under {target_dir.relative_to(ROOT)}."
                    ),
                    suggestions=[
                        f"Create the {kind} artefact via /requirements-engineering",
                        "Delete the Item-BA if the work was abandoned",
                    ],
                ))
                continue
            target_path = matches[0]
            target_fm = parse_frontmatter(target_path)
            if not target_fm.get("ba-ref"):
                out.append(Finding(
                    type="missing-ba-ref",
                    severity=SEVERITY_LOW,
                    file=str(target_path.relative_to(ROOT)),
                    line=None,
                    message=(
                        f"{kind} artefact has no `ba-ref:` in frontmatter "
                        f"but a matching Item-BA exists at "
                        f"{ba_path.relative_to(ROOT)}."
                    ),
                    suggestions=[
                        f"Add `ba-ref: {os.path.relpath(ba_path, target_path.parent)}` to the frontmatter",
                    ],
                ))
    return out


_STATUS_DONE = {"done", "released", "implemented", "implementiert",
                "vollstaendig implementiert", "vollständig implementiert"}
_STATUS_OPEN = {"backlog", "ready", "in progress", "in review", "open",
                "active", "planned", "geplant", "not started", "draft",
                "in arbeit", "candidates", "candidate"}


def _normalise_status(value: str) -> str:
    """Lowercase + collapse whitespace + strip trailing parenthesis hints."""
    if not value:
        return ""
    cleaned = re.sub(r"\s*\([^)]*\)\s*$", "", value).strip().lower()
    return re.sub(r"\s+", " ", cleaned)


def _status_compatible(backlog_status: str, detail_status: str) -> bool:
    """True when the detail-file status is consistent with the backlog
    Status/Phase pair.

    Compatibility groups:
      - "Done" family: backlog Done <-> detail Done | Released | Implemented
      - "Open" family: everything else from the GitHub-aligned status set
        plus the legacy detail-file phrasing (Geplant, Not Started,
        Implementiert wenn backlog noch offen, etc.).
    """
    bl = _normalise_status(backlog_status)
    df = _normalise_status(detail_status)
    if not bl or not df:
        return True
    if df == bl:
        return True
    if bl in _STATUS_DONE and df in _STATUS_DONE:
        return True
    if bl in _STATUS_OPEN and df in _STATUS_OPEN:
        return True
    return False


def _backlog_status_index() -> dict[str, dict[str, str]]:
    """Map FEAT/IMP/FIX ID -> {status, phase} from the backlog row.

    Best-effort parse: schema follows the BACKLOG-TEMPLATE column order
    (ID | Type | Title | Status | Phase | ...). Rows that do not fit
    the schema are skipped silently.
    """
    if not BACKLOG.exists():
        return {}
    out: dict[str, dict[str, str]] = {}
    for raw in BACKLOG.read_text(encoding="utf-8").splitlines():
        if not raw.startswith("|"):
            continue
        cells = [c.strip() for c in raw.strip("|").split("|")]
        if len(cells) < 5:
            continue
        item_id = cells[0]
        if not re.match(r"^(FEAT|FIX|IMP)-\d{2}(?:-\d{2}){1,2}$", item_id):
            continue
        out[item_id] = {"status": cells[3], "phase": cells[4]}
    return out


_DETAIL_FEATURES_HEADER_RE = re.compile(
    r"^##\s+(MVP\s+Features|Features)\s*$", re.MULTILINE | re.IGNORECASE,
)
_DETAIL_ROW_ID_RE = re.compile(r"^\|\s*((?:FEAT|IMP|FIX)-\d{2}(?:-\d{2}){1,2})\s*\|")


def _iter_detail_status_rows(text: str):
    """Yield (item_id, status_value, line_no) tuples from a detail-file
    Features/MVP-Features table. The Status column is taken as the last
    pipe-cell on the row, matching the convention in the live obsilo-dev
    Epic detail files.
    """
    header = _DETAIL_FEATURES_HEADER_RE.search(text)
    if not header:
        return
    body_start = header.end()
    next_h2 = re.search(r"\n##\s+\S", text[body_start:])
    body_end = body_start + next_h2.start() if next_h2 else len(text)
    base_line = text[:body_start].count("\n")
    for offset, raw in enumerate(text[body_start:body_end].splitlines(), start=1):
        m = _DETAIL_ROW_ID_RE.match(raw)
        if not m:
            continue
        cells = [c.strip() for c in raw.strip("|").split("|")]
        if len(cells) < 2:
            continue
        # Skip header separator rows like "| --- | --- |".
        if all(set(c) <= set("-: ") for c in cells):
            continue
        status_value = cells[-1]
        yield m.group(1), status_value, base_line + offset


def check_detail_file_status_drift() -> list[Finding]:
    """E-15: detail-file Features tables that name a backlog item must
    show a Status compatible with the backlog row's Status. Catches
    the live drift in obsilo-dev (Epic detail says 'Geplant', backlog
    says 'Done | Released').
    """
    if not BACKLOG.exists() or not EPICS.exists():
        return []
    backlog_idx = _backlog_status_index()
    if not backlog_idx:
        return []
    out: list[Finding] = []
    for epic in sorted(EPICS.glob("EPIC-*.md")):
        try:
            text = epic.read_text(encoding="utf-8")
        except Exception:
            continue
        for item_id, detail_status, line_no in _iter_detail_status_rows(text):
            row = backlog_idx.get(item_id)
            if not row:
                continue
            if _status_compatible(row["status"], detail_status):
                continue
            out.append(Finding(
                type="status-drift-detail-vs-backlog",
                severity=SEVERITY_MEDIUM,
                file=str(epic.relative_to(ROOT)),
                line=line_no,
                message=(
                    f"{item_id}: detail-file says '{detail_status}', "
                    f"BACKLOG says '{row['status']}/{row['phase']}'"
                ),
                suggestions=[
                    "Update the detail-file row Status to match the backlog (when backlog is canonical)",
                    "Update the backlog row Status to match the detail file (when work has not started)",
                    "Remove the detail-file row if the feature was moved to a different epic",
                ],
            ))
    return out


BACKLOG_ID_ROW_RE = re.compile(
    r"^\|\s*((?:FEAT|FIX|IMP|ADR|PLAN)-\d{2}(?:-\d{2}){0,2})\s*\|"
)


def check_backlog_id_uniqueness() -> list[Finding]:
    """N-19: every FEAT/FIX/IMP/ADR/PLAN ID appears at most once in
    BACKLOG.md. EPIC is exempt because epic IDs intentionally show up
    both as table rows and as section headings.

    Picks up legacy duplicates that survived migration sweeps because
    no invariant covered the inverse direction of E-12.
    """
    if not BACKLOG.exists():
        return []
    rows: dict[str, list[tuple[int, str]]] = {}
    for line_no, raw in enumerate(
        BACKLOG.read_text(encoding="utf-8").splitlines(), start=1,
    ):
        m = BACKLOG_ID_ROW_RE.match(raw)
        if not m:
            continue
        rows.setdefault(m.group(1), []).append((line_no, raw))
    out: list[Finding] = []
    for item_id, occurrences in rows.items():
        if len(occurrences) <= 1:
            continue
        line_numbers = [ln for ln, _ in occurrences]
        out.append(Finding(
            type="duplicate-backlog-id",
            severity=SEVERITY_HIGH,
            file=str(BACKLOG.relative_to(ROOT)),
            line=occurrences[0][0],
            message=(
                f"Backlog ID {item_id} appears {len(occurrences)}x; "
                f"rows {line_numbers}"
            ),
            suggestions=[
                "Renumber one of the duplicates to the next free ID under the same Epic",
                "Merge the two rows if they describe the same feature",
                "Delete the obsolete row if one of them is stale",
            ],
        ))
    return out


def check_backlog_completeness() -> list[Finding]:
    out: list[Finding] = []
    backlog_ids = parse_backlog_ids()
    artifact_ids: set[str] = set()
    for p in md_files(FEATURES, EPICS, FIXES, IMPROVEMENTS, ARCHITECTURE, PLANS):
        if p.name.lower() == "readme.md":
            continue
        aid = parse_artifact_id(p)
        if not aid:
            continue
        artifact_ids.add(aid)
        if aid not in backlog_ids:
            out.append(Finding(
                type="missing-backlog-row",
                severity=SEVERITY_MEDIUM,
                file=str(p.relative_to(ROOT)),
                line=None,
                message=f"Artifact {aid} has no row in {BACKLOG.relative_to(ROOT)}",
                suggestions=[
                    f"Add backlog row for {aid} with default Status=Ready/Phase=Building",
                    "Delete the artifact file if it is obsolete",
                ],
            ))
    for bid in backlog_ids - artifact_ids:
        out.append(Finding(
            type="orphan-backlog-row",
            severity=SEVERITY_LOW,
            file=str(BACKLOG.relative_to(ROOT)),
            line=None,
            message=f"Backlog row {bid} has no matching artifact file",
            suggestions=[
                f"Create the artifact file for {bid}",
                f"Remove the backlog row for {bid} if it is stale",
            ],
        ))
    return out


# ---------- Orchestration --------------------------------------------------


def run_checks() -> list[Finding]:
    findings: list[Finding] = []
    artifact_dirs = (FEATURES, EPICS, FIXES, IMPROVEMENTS, ARCHITECTURE, PLANS, CONTEXT)
    findings.extend(check_dead_links(md_files(*artifact_dirs)))
    findings.extend(check_adr_abstraction(md_files(ARCHITECTURE)))
    findings.extend(check_backlog_completeness())
    findings.extend(check_backlog_id_uniqueness())
    findings.extend(check_detail_file_status_drift())
    findings.extend(check_status_coherence())
    findings.extend(check_item_ba_frontmatter())
    findings.extend(check_ba_ref_bidirectional())
    findings.extend(check_feature_activation_path())
    findings.extend(check_stub_fix_binding())
    return findings


def write_last_run(findings: list[Finding]) -> None:
    LAST_RUN.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": 1,
        "git_branch": _git_branch(),
        "findings": [asdict(f) for f in findings],
    }
    LAST_RUN.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _git_branch() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=ROOT, text=True,
        ).strip()
    except Exception:
        return "unknown"


def print_summary(findings: list[Finding], fixed_count: int) -> None:
    by_type: dict[str, int] = {}
    by_sev: dict[str, int] = {}
    for f in findings:
        by_type[f.type] = by_type.get(f.type, 0) + 1
        by_sev[f.severity] = by_sev.get(f.severity, 0) + 1
    print(f"[consistency-check Mode A]")
    if fixed_count:
        print(f"  Auto-fixed: {fixed_count} files")
    print(f"  Remaining findings: {len(findings)}")
    for sev in (SEVERITY_HIGH, SEVERITY_MEDIUM, SEVERITY_LOW):
        if sev in by_sev:
            print(f"    {sev}: {by_sev[sev]}")
    for t, n in sorted(by_type.items()):
        print(f"    - {t}: {n}")
    if findings:
        print()
        print("  First findings (max 5):")
        for f in findings[:5]:
            loc = f"{f.file}:{f.line}" if f.line else f.file
            print(f"    [{f.severity}] {f.type}  {loc}")
            print(f"        {f.message}")


def stage_modified() -> None:
    targets = [d for d in (FEATURES, EPICS) if d.exists()]
    if not targets:
        return
    args = ["git", "add", "--"] + [str(t.relative_to(ROOT)) for t in targets]
    try:
        subprocess.check_call(args, cwd=ROOT)
    except Exception:
        pass


def main() -> int:
    ap = argparse.ArgumentParser(
        description="DIA consistency-check Mode A (syntactic) for V-Model artefact graphs.",
    )
    ap.add_argument("--check", action="store_true", help="alias for default")
    ap.add_argument("--fix", action="store_true", help="auto-fix safe drift")
    args = ap.parse_args()

    if not DEV.exists():
        print(f"[consistency-check] No {DEV.relative_to(ROOT)}/ directory found at {ROOT}.")
        print("    Skipping. (Run inside a project that follows DIA conventions.)")
        return 0

    fixed_count = 0
    if args.fix:
        target = list(md_files(FEATURES, EPICS))
        fixed_count = autofix_status_duplicates(target)
        if fixed_count:
            stage_modified()

    findings = run_checks()
    write_last_run(findings)
    print_summary(findings, fixed_count)

    if findings:
        print()
        print(f"  Findings file: {LAST_RUN.relative_to(ROOT)}")
        print(f"  Interactive fix loop: claude /consistency-check --fix-interactive")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
