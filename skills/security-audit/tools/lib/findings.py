"""Shared finding model + baseline IO for the security-audit scripts.

stdlib-only. Three concerns:

  * Finding      -- the one finding record every scanner emits.
  * fingerprint  -- stable identity for a finding, INDEPENDENT of line
                    number and timestamp, so a finding survives
                    renumbering and two runs over the same code produce
                    identical ids. This is what makes the re-audit delta
                    reliable instead of eyeballed.
  * redact       -- never let a secret's plaintext reach a report, a log,
                    or stderr. Only a 4-char preview + length + short hash.
  * baseline IO  -- write/read/rotate .git/security-audit/{last,prev}-run.json.
                    A diff-scope run (commit/branch/...) must NOT clobber
                    the full-tree baseline, or the delta would be meaningless.

The baseline lives under .git/ (never committed, ephemeral per clone),
matching tools/consistency-check.py's LAST_RUN convention.
"""
from __future__ import annotations
import hashlib
import json
import re
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Iterable, Optional

BASELINE_SCHEMA = 1
_WS_RE = re.compile(r"\s+")


@dataclass
class Finding:
    """One security finding. `fp` is the stable fingerprint; `line` is a
    display coordinate only and never enters the fingerprint.
    """
    fp: str
    phase: str          # detect | surface | sast | secrets | sca
    cwe: str            # e.g. "CWE-79", or "" when not CWE-mappable
    severity: str       # critical | high | medium | low | info
    file: str
    line: Optional[int]
    engine: str         # semgrep | codeql | grep-fallback | gitleaks | npm-audit | ...
    message: str
    status: str = "unconfirmed"  # unconfirmed | confirmed | false-positive | resolved
    evidence: str = ""
    cvss: str = ""
    suggestions: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def fingerprint(cwe: str, relpath: str, snippet: str) -> str:
    """Stable 8-hex identity from (cwe, path, normalized snippet).

    Normalization collapses all whitespace to single spaces and
    lowercases, so reformatting or case changes do not spawn a new
    fingerprint. Line number and timestamp are deliberately excluded --
    a finding that moves down the file is the SAME finding.
    """
    norm = _WS_RE.sub(" ", snippet).strip().lower()
    raw = f"{cwe}|{relpath}|{norm}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:8]


def redact(match: str) -> dict:
    """Return a non-reversible descriptor of a secret match. Never
    include the plaintext (not the full string, not the tail). Only a
    4-char prefix preview, the length, and a short sha1.
    """
    preview = match[:4]
    return {
        "preview": preview,
        "len": len(match),
        "sha1": hashlib.sha1(match.encode("utf-8")).hexdigest()[:8],
    }


# ---------- baseline IO ----------------------------------------------------

def _baseline_dir(root: Path) -> Path:
    return root / ".git" / "security-audit"


def _last_path(root: Path) -> Path:
    return _baseline_dir(root) / "last-run.json"


def _prev_path(root: Path) -> Path:
    return _baseline_dir(root) / "prev-run.json"


def read_baseline(root: Path, which: str = "last") -> Optional[dict]:
    """Read the last or prev baseline. Returns None if absent or unreadable."""
    path = _last_path(root) if which == "last" else _prev_path(root)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_baseline(
    root: Path,
    findings: Iterable[Finding],
    scope: str,
    taxonomy: dict,
) -> None:
    """Persist findings as the new last-run baseline.

    Rotation rule (guards the delta):
      * A `full` run rotates the existing last-run into prev-run, then
        writes the fresh full baseline. This is the only scope allowed to
        advance the reference point for diffs.
      * A diff-scope run (commit/branch/working/staged/range) must NOT
        overwrite a `full` baseline -- otherwise the next full delta would
        compare against a partial scan and mislabel resolved/new. Such a
        run is a no-op against the persisted full baseline.
    """
    bdir = _baseline_dir(root)
    bdir.mkdir(parents=True, exist_ok=True)
    findings = list(findings)

    if scope != "full":
        existing = read_baseline(root, which="last")
        if existing is not None and existing.get("scope") == "full":
            # Do not clobber the full-tree reference point.
            return

    # full run (or first run of any scope): rotate then write.
    last = _last_path(root)
    if last.exists():
        try:
            _prev_path(root).write_text(
                last.read_text(encoding="utf-8"), encoding="utf-8"
            )
        except Exception:
            pass

    payload = {
        "schema": BASELINE_SCHEMA,
        "scope": scope,
        "taxonomy": taxonomy,
        "findings": [f.to_dict() for f in findings],
    }
    last.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def delta(before_fps: Iterable[str], after_fps: Iterable[str]) -> dict:
    """Set difference over fingerprints. resolved = in before not after,
    new = in after not before, persisted = in both.
    """
    b = set(before_fps)
    a = set(after_fps)
    return {
        "resolved": sorted(b - a),
        "new": sorted(a - b),
        "persisted": sorted(a & b),
    }
