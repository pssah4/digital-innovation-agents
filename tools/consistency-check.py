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
YAML_STATUS = re.compile(r"^(status|phase)\s*:\s*.+$", re.IGNORECASE)


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
            if in_yaml and YAML_STATUS.match(stripped):
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
                    f"Add backlog row for {aid} with default Status=Planned/Phase=Building",
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
