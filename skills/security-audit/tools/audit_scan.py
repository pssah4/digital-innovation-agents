#!/usr/bin/env python3
"""Security-audit scan orchestrator (DIA security-audit skill).

Deterministic, reproducible, offline-graceful. Orchestrates project-type
detection, attack-surface enumeration, SAST, secret scanning and SCA, and
emits ONE machine-readable findings envelope that report_assembler.py
turns into the human report.

stdlib-only. External tools (semgrep, gitleaks, osv-scanner, npm) are
OPTIONAL: each is probed via tool_available(); if absent, the scan records
an honest status in the tools[] ledger and continues. Nothing here ever
hard-aborts on a missing tool, and no secret plaintext is ever written to
output or stderr.

Usage:
    audit_scan.py detect  [root] [--json]
    audit_scan.py surface [root] [--json]
    audit_scan.py sast    [root] [--scope S] [--base B] [--range A..B]
    audit_scan.py secrets [root] [--scope S] ...
    audit_scan.py sca     [root]
    audit_scan.py supply-chain [root] [--rebuild] [--release-verify]
                                 [--build-cmd CMD] [--artifact P ...]
                                 [--registry-host H ...]
    audit_scan.py all     [root] [--scope S] [--base B] [--range A..B]
                                 [--taxonomy JSON] [--no-baseline]

`all` stays offline-deterministic: the supply-chain phase runs its static
checks only; the clean-room rebuild (--rebuild) and release attestation
verify (--release-verify) execute external commands and are opt-in on the
supply-chain subcommand, with honest not-run ledger entries otherwise.

Default root: git repo root (via git rev-parse), else cwd.
Exit codes: 0 no findings, 1 findings present, 2 usage error.
"""
# security-audit-scan: skip -- this module stores CWE-detection regexes as
# data literals; scanning it against those same regexes only produces
# self-referential false positives.
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Skill-local lib import (works regardless of cwd).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import findings as F          # noqa: E402
from lib import scope as SCOPE          # noqa: E402
from lib import detectors as DET        # noqa: E402
from lib import codeql_runner as CQ     # noqa: E402
from lib import skip_rules as SKIP      # noqa: E402
from lib import supply_chain as SC      # noqa: E402
from lib import cleanroom as CR         # noqa: E402


def find_repo_root(start: Path | None = None) -> Path:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(start or Path.cwd()), text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return Path(out)
    except Exception:
        return (start or Path.cwd()).resolve()


def tool_available(name: str) -> bool:
    """True if an external executable is on PATH."""
    return shutil.which(name) is not None


def _net_available() -> bool:
    """Best-effort: honour an explicit offline env flag; otherwise assume
    online. We never block on a real network probe (that would add latency
    and its own failure mode); the SCA tools report their own net errors.
    """
    return os.environ.get("SECURITY_AUDIT_OFFLINE", "") not in ("1", "true", "yes")


# ---------- SAST grep fallback ---------------------------------------------

# (cwe, severity, compiled pattern, message). Mirrors references/cwe-patterns.md
# so the grep fallback stays aligned with the checklist. These are heuristics;
# the LLM triages each hit (source->sink) before it becomes Confirmed.
_GREP_RULES = [
    ("CWE-94", "high", re.compile(r"\beval\s*\(|\bnew\s+Function\s*\(|vm\.runIn\w+\s*\("),
     "Dynamic code execution with variable input"),
    ("CWE-78", "high", re.compile(r"\b(execSync|spawnSync|child_process|\.exec\s*\(|execFile\s*\()"),
     "Shell command with possibly unescaped input"),
    ("CWE-79", "medium", re.compile(r"\.(innerHTML|outerHTML)\b|dangerouslySetInnerHTML|document\.write\s*\("),
     "HTML sink; possible XSS if input is untrusted"),
    ("CWE-22", "high", re.compile(r"\.\./|path\.join\([^)]*\breq\b|readFile\w*\([^)]*\+"),
     "Possible path traversal; check normalization + prefix"),
    ("CWE-918", "high", re.compile(r"\b(fetch|requestUrl|axios|http\.get|https\.get)\s*\([^)]*(url|href|endpoint|target)"),
     "Outbound request with variable URL; check allowlist"),
    ("CWE-502", "medium", re.compile(r"\b(yaml\.load\s*\(|pickle\.loads\s*\(|unserialize\s*\()"),
     "Insecure deserialization"),
    ("CWE-1321", "medium", re.compile(r"__proto__|prototype\[|Object\.assign\([^,]*,\s*JSON\.parse"),
     "Possible prototype pollution sink"),
    ("CWE-312", "medium", re.compile(r"console\.(log|debug|info)\s*\([^)]*(token|password|secret|apikey|api_key)", re.IGNORECASE),
     "Credential-shaped value in a log call"),
    ("CWE-367", "low", re.compile(r"existsSync\([^)]*\)[\s\S]{0,80}?(readFileSync|writeFileSync|open\s*\()"),
     "Possible TOCTOU: exists-check then use"),
]

_TEXT_EXT = DET._TEXT_EXT


def grep_sast(root: Path, files) -> list:
    """CWE-pattern grep fallback. One Finding per (rule, file, line).
    Files that match a skip glob or carry the `security-audit-scan: skip`
    header are excluded from the pattern scan (test fixtures, bundled
    assets, detector modules that store the patterns as data)."""
    out: list = []
    for rel in files:
        path = root / rel
        if path.suffix not in _TEXT_EXT:
            continue
        if not SKIP.should_scan(rel, root):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for ln, line in enumerate(text.splitlines(), start=1):
            snippet = line.strip()
            for cwe, sev, rx, msg in _GREP_RULES:
                if rx.search(line):
                    out.append(F.Finding(
                        fp=F.fingerprint(cwe, rel, snippet),
                        phase="sast", cwe=cwe, severity=sev,
                        file=rel, line=ln, engine="grep-fallback",
                        message=msg,
                    ))
    return out


def _semgrep_sast(root: Path, files, rulesets) -> list:
    """Run semgrep --json against the given files, map to Findings.
    Returns [] on any failure (caller records tool status)."""
    if not files:
        return []
    cfg_args = []
    for rs in rulesets:
        cfg_args += ["--config", rs.replace("semgrep:", "")]
    if not cfg_args:
        cfg_args = ["--config", "auto"]
    try:
        cp = subprocess.run(
            ["semgrep", *cfg_args, "--json", "--quiet", *[str(root / f) for f in files]],
            cwd=str(root), text=True, capture_output=True, timeout=600,
        )
        data = json.loads(cp.stdout or "{}")
    except Exception:
        return []
    out: list = []
    for r in data.get("results", []):
        rel = os.path.relpath(r.get("path", ""), str(root))
        line = (r.get("start") or {}).get("line")
        extra = r.get("extra", {})
        meta = extra.get("metadata", {}) or {}
        cwe_field = meta.get("cwe")
        if isinstance(cwe_field, list):
            cwe = (cwe_field[0].split(":")[0].strip() if cwe_field else "")
        else:
            cwe = str(cwe_field or "").split(":")[0].strip()
        sev = {"ERROR": "high", "WARNING": "medium", "INFO": "low"}.get(
            extra.get("severity", "WARNING"), "medium")
        snippet = (extra.get("lines") or "").strip()
        out.append(F.Finding(
            fp=F.fingerprint(cwe or r.get("check_id", ""), rel, snippet or r.get("check_id", "")),
            phase="sast", cwe=cwe, severity=sev,
            file=rel, line=line, engine="semgrep",
            message=extra.get("message", r.get("check_id", "semgrep finding")),
        ))
    return out


def _codeql_db_dir(root: Path, language: str) -> Path:
    """Where the per-language CodeQL DB lives. Kept out of the repo via
    .git/info/exclude on first run (Phase 3)."""
    return root / ".git" / "security-audit" / f"codeql-db-{language}"


def run_sast(root: Path, files, project) -> tuple:
    """SAST cascade: CodeQL (if available and pack present) -> semgrep ->
    grep. All three engines run additively when available; findings are
    deduped by fingerprint. Returns (findings, tools).

    The cascade never breaks: a missing tool is recorded honestly in the
    tools ledger and the next engine takes over. Grep always runs as a
    cheap third layer because it covers CWE patterns (CWE-312, TOCTOU)
    that the higher-tier engines may not include.
    """
    tools: list = []
    findings: list = []
    codeql_langs = project.get("codeql_languages", []) or []

    # Layer 1: CodeQL, if available and at least one language matches.
    if CQ.codeql_available() and codeql_langs:
        for lang in codeql_langs:
            cq_findings, cq_tool = CQ.run_codeql(
                root, lang, _codeql_db_dir(root, lang),
            )
            age = CQ.pack_age_check(f"codeql/{lang}-queries")
            if age is not None:
                cq_tool["pack_version"] = age["pack_version"]
                cq_tool["pack_age_days"] = age["pack_age_days"]
            findings.extend(cq_findings)
            tools.append(cq_tool)
    else:
        reason = ("not on PATH" if not CQ.codeql_available()
                  else "no CodeQL-supported languages detected")
        tools.append({"name": "codeql", "status": "unavailable",
                      "reason": reason})

    # Layer 2: semgrep, if available. Complement to CodeQL, primary when
    # CodeQL is absent.
    rulesets = project.get("applicable_tools", {}).get("sast", [])
    if tool_available("semgrep"):
        sem = _semgrep_sast(root, files, rulesets)
        if sem is not None:
            findings.extend(sem)
            tools.append({"name": "semgrep", "status": "ran",
                          "ruleset": ",".join(rulesets) or "auto"})
    else:
        tools.append({"name": "semgrep", "status": "unavailable",
                      "reason": "not on PATH"})

    # Layer 3: grep. Cheap and always available, covers patterns the
    # higher tiers may not include.
    findings.extend(grep_sast(root, files))

    return _dedupe_findings(findings), tools


# ---------- secret scan ----------------------------------------------------

_SECRET_PATTERNS = [
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("generic-api-key", re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]")),
    ("private-key-block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("slack-token", re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}")),
    ("github-pat", re.compile(r"ghp_[0-9A-Za-z]{36}")),
]


def _entropy_secret_finding(root: Path, rel: str, ln: int, match: str) -> F.Finding:
    red = F.redact(match)
    return F.Finding(
        fp=F.fingerprint("CWE-798", rel, red["sha1"]),
        phase="secrets", cwe="CWE-798", severity="high",
        file=rel, line=ln, engine="entropy-fallback",
        message=f"Possible hardcoded secret (redacted: {red['preview']}..., len {red['len']})",
    )


def run_secrets(root: Path, files) -> tuple:
    """Secret scan. Prefer gitleaks/trufflehog; fall back to a pattern +
    redaction scan. NEVER emits plaintext. Returns (findings, tools)."""
    tools: list = []
    # We keep the built-in redacting scanner as the deterministic baseline
    # even when gitleaks is present, and record which ran.
    if tool_available("gitleaks"):
        tools.append({"name": "gitleaks", "status": "available",
                      "note": "run separately by the skill for git-history depth"})
    else:
        tools.append({"name": "gitleaks", "status": "unavailable",
                      "reason": "not on PATH; used redacting pattern fallback"})

    out: list = []
    for rel in files:
        path = root / rel
        if path.suffix not in _TEXT_EXT and path.suffix not in {".json", ".env", ".yaml", ".yml", ".toml", ".pem", ".txt", ""}:
            continue
        if not SKIP.should_scan(rel, root):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for ln, line in enumerate(text.splitlines(), start=1):
            for _name, rx in _SECRET_PATTERNS:
                mm = rx.search(line)
                if mm:
                    out.append(_entropy_secret_finding(root, rel, ln, mm.group(0)))
    tools.append({"name": "pattern-redact", "status": "ran"})
    return out, tools


# ---------- SCA ------------------------------------------------------------

def run_sca(root: Path) -> tuple:
    """Dependency scan. npm audit + osv-scanner when available and online.
    License extraction is local and always runs. Returns (findings, tools).
    """
    tools: list = []
    out: list = []
    online = _net_available()

    pkg = root / "package.json"
    if pkg.is_file():
        if not tool_available("npm"):
            tools.append({"name": "npm-audit", "status": "unavailable",
                          "reason": "npm not on PATH"})
        elif not online:
            tools.append({"name": "npm-audit", "status": "offline-skipped"})
        else:
            out += _npm_audit(root, tools)
    if tool_available("osv-scanner") and online:
        out += _osv_scanner(root, tools)
    elif not tool_available("osv-scanner"):
        tools.append({"name": "osv-scanner", "status": "unavailable",
                      "reason": "not on PATH"})
    elif not online:
        tools.append({"name": "osv-scanner", "status": "offline-skipped"})

    if not tools:
        tools.append({"name": "sca", "status": "unavailable",
                      "reason": "no supported manifest / tools found"})
    return out, tools


def _npm_audit(root: Path, tools: list) -> list:
    try:
        cp = subprocess.run(["npm", "audit", "--json"], cwd=str(root),
                            text=True, capture_output=True, timeout=300)
        data = json.loads(cp.stdout or "{}")
    except Exception as exc:  # noqa: BLE001
        tools.append({"name": "npm-audit", "status": "error", "reason": str(exc)[:120]})
        return []
    tools.append({"name": "npm-audit", "status": "ran"})
    out: list = []
    for name, adv in (data.get("vulnerabilities", {}) or {}).items():
        sev = adv.get("severity", "low")
        sev = {"critical": "critical", "high": "high",
               "moderate": "medium", "low": "low", "info": "info"}.get(sev, "low")
        out.append(F.Finding(
            fp=F.fingerprint("SCA", name, str(adv.get("range", ""))),
            phase="sca", cwe="", severity=sev,
            file="package.json", line=None, engine="npm-audit",
            message=f"Vulnerable dependency: {name} ({adv.get('range', '?')})",
        ))
    return out


def _osv_scanner(root: Path, tools: list) -> list:
    try:
        cp = subprocess.run(
            ["osv-scanner", "--format", "json", "--recursive", str(root)],
            cwd=str(root), text=True, capture_output=True, timeout=300)
        data = json.loads(cp.stdout or "{}")
    except Exception as exc:  # noqa: BLE001
        tools.append({"name": "osv-scanner", "status": "error", "reason": str(exc)[:120]})
        return []
    tools.append({"name": "osv-scanner", "status": "ran"})
    out: list = []
    for res in data.get("results", []):
        for pkg in res.get("packages", []):
            info = pkg.get("package", {})
            pname = info.get("name", "?")
            for v in pkg.get("vulnerabilities", []):
                out.append(F.Finding(
                    fp=F.fingerprint("SCA", pname, v.get("id", "")),
                    phase="sca", cwe="", severity="medium",
                    file=res.get("source", {}).get("path", "lockfile"),
                    line=None, engine="osv-scanner",
                    message=f"{v.get('id', 'OSV')} in {pname}",
                ))
    return out


# ---------- supply chain ---------------------------------------------------

def run_supply_chain(root: Path, rebuild: bool = False,
                     release_verify: bool = False,
                     cli_cfg: dict | None = None) -> tuple:
    """Supply-chain phase. Stage 1 (static file checks) always runs;
    stage 2 (clean-room rebuild) and stage 3 (release attestation verify)
    execute external commands and only run when explicitly requested.
    The stages that did not run appear in the tools ledger with an
    honest not-run entry. Returns (findings, tools)."""
    cfg = CR.read_supply_chain_config(root, cli_overrides=cli_cfg)
    findings, tools = SC.run_supply_chain_static(root, config=cfg)

    rebuilt_hashes = None
    if rebuild:
        rb_findings, rb_tool = CR.run_cleanroom_rebuild(root, cfg)
        findings.extend(rb_findings)
        rebuilt_hashes = rb_tool.pop("built_hashes", None)
        tools.append(rb_tool)
    else:
        tools.append({"name": "cleanroom-rebuild", "status": "not-run",
                      "reason": "opt-in; pass --rebuild"})

    if release_verify:
        rv_findings, rv_tools = CR.run_release_verify(
            root, rebuilt_hashes=rebuilt_hashes)
        findings.extend(rv_findings)
        tools.extend(rv_tools)
    else:
        tools.append({"name": "gh-attestation", "status": "not-run",
                      "reason": "opt-in; pass --release-verify"})

    return _dedupe_findings(findings), tools


# ---------- helpers --------------------------------------------------------

def _dedupe_findings(items) -> list:
    seen = set()
    out = []
    for f in items:
        if f.fp in seen:
            continue
        seen.add(f.fp)
        out.append(f)
    return out


def _ensure_git_exclude(root: Path) -> None:
    """Idempotently add the CodeQL DB directory pattern to
    .git/info/exclude so 53 MB DBs don't show up as untracked.

    Uses .git/info/exclude (local-only, per-clone) instead of .gitignore
    which belongs to the user's repo. Best-effort: silent no-op if the
    file cannot be written (bare repo, submodule, permission issue).
    """
    marker = "security-audit/codeql-db-*/"
    info_dir = root / ".git" / "info"
    exclude = info_dir / "exclude"
    try:
        if not info_dir.is_dir():
            return
        existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
        if marker in existing:
            return
        header = "\n# added by security-audit skill (CodeQL DBs)\n"
        exclude.write_text(existing.rstrip() + header + marker + "\n",
                           encoding="utf-8")
    except Exception:
        return


def _git_head(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(root), text=True,
            stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def _git_branch(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=str(root),
            text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"


# ---------- orchestration --------------------------------------------------

def run_all(root: Path, scope: str = "full", base: str = "main",
            rng: str | None = None, taxonomy: dict | None = None,
            write_baseline: bool = True) -> dict:
    project = DET.detect_project(root)
    sr = SCOPE.resolve_scope(root, scope, base=base, rng=rng)
    files = sr.files

    # Keep CodeQL DBs out of git status. Idempotent, silent no-op if
    # the .git/info/ directory is not writable or not present.
    _ensure_git_exclude(root)

    surfaces = DET.enumerate_surfaces(root, files)
    sast_findings, sast_tools = run_sast(root, files, project)
    secret_findings, secret_tools = run_secrets(root, files)
    sca_findings, sca_tools = run_sca(root)
    supply_findings, supply_tools = run_supply_chain(root)

    all_findings = _dedupe_findings(
        sast_findings + secret_findings + sca_findings + supply_findings)
    tools = sast_tools + secret_tools + sca_tools + supply_tools

    result = {
        "schema": 1,
        "generated_by": "security-audit/tools/audit_scan.py",
        "git_branch": _git_branch(root),
        "git_head": _git_head(root),
        "scope": scope,
        "scope_detail": sr.detail,
        "scope_files": files,
        "taxonomy": taxonomy or {},
        "project_type": project,
        "surfaces": surfaces,
        "tools": tools,
        "findings": [f.to_dict() for f in all_findings],
        "meta": {
            "offline": not _net_available(),
            "file_count": len(files),
            "finding_count": len(all_findings),
        },
    }

    if write_baseline:
        F.write_baseline(root, all_findings, scope=scope, taxonomy=taxonomy or {})

    return result


# ---------- CLI ------------------------------------------------------------

def _add_scope_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("root", nargs="?", default=None)
    p.add_argument("--scope", default="full", choices=SCOPE.ALL_SCOPES)
    p.add_argument("--base", default="main")
    p.add_argument("--range", dest="rng", default=None)


def _resolve_root(arg) -> Path:
    return find_repo_root(Path(arg).resolve() if arg else None)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Security-audit scan orchestrator.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_detect = sub.add_parser("detect")
    p_detect.add_argument("root", nargs="?", default=None)

    p_surface = sub.add_parser("surface")
    _add_scope_args(p_surface)

    p_sast = sub.add_parser("sast")
    _add_scope_args(p_sast)

    p_secrets = sub.add_parser("secrets")
    _add_scope_args(p_secrets)

    p_sca = sub.add_parser("sca")
    p_sca.add_argument("root", nargs="?", default=None)

    p_supply = sub.add_parser("supply-chain")
    p_supply.add_argument("root", nargs="?", default=None)
    p_supply.add_argument("--rebuild", action="store_true",
                          help="opt-in clean-room rebuild (runs the project build)")
    p_supply.add_argument("--release-verify", action="store_true",
                          help="opt-in gh attestation verify of latest release assets")
    p_supply.add_argument("--build-cmd", default=None)
    p_supply.add_argument("--artifact", action="append", default=None,
                          help="tracked artifact path (repeatable)")
    p_supply.add_argument("--registry-host", action="append", default=None,
                          help="additional allowed registry host (repeatable)")

    p_all = sub.add_parser("all")
    _add_scope_args(p_all)
    p_all.add_argument("--taxonomy", default=None,
                       help="JSON string of the audit's snapshotted taxonomy set")
    p_all.add_argument("--no-baseline", action="store_true")

    args = ap.parse_args(argv)
    root = _resolve_root(getattr(args, "root", None))

    if args.cmd == "detect":
        out = DET.detect_project(root)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "surface":
        sr = SCOPE.resolve_scope(root, args.scope, base=args.base, rng=args.rng)
        out = DET.enumerate_surfaces(root, sr.files)
        print(json.dumps({"scope": args.scope, "surfaces": out}, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "sast":
        sr = SCOPE.resolve_scope(root, args.scope, base=args.base, rng=args.rng)
        project = DET.detect_project(root)
        fs, tools = run_sast(root, sr.files, project)
        print(json.dumps({"tools": tools, "findings": [f.to_dict() for f in fs]},
                         indent=2, ensure_ascii=False))
        return 1 if fs else 0

    if args.cmd == "secrets":
        sr = SCOPE.resolve_scope(root, args.scope, base=args.base, rng=args.rng)
        fs, tools = run_secrets(root, sr.files)
        print(json.dumps({"tools": tools, "findings": [f.to_dict() for f in fs]},
                         indent=2, ensure_ascii=False))
        return 1 if fs else 0

    if args.cmd == "sca":
        fs, tools = run_sca(root)
        print(json.dumps({"tools": tools, "findings": [f.to_dict() for f in fs]},
                         indent=2, ensure_ascii=False))
        return 1 if fs else 0

    if args.cmd == "supply-chain":
        cli_cfg = {"build_command": args.build_cmd,
                   "artifacts": args.artifact,
                   "registry_hosts": args.registry_host}
        fs, tools = run_supply_chain(root, rebuild=args.rebuild,
                                     release_verify=args.release_verify,
                                     cli_cfg=cli_cfg)
        print(json.dumps({"tools": tools, "findings": [f.to_dict() for f in fs]},
                         indent=2, ensure_ascii=False))
        return 1 if fs else 0

    if args.cmd == "all":
        taxonomy = None
        if args.taxonomy:
            try:
                taxonomy = json.loads(args.taxonomy)
            except Exception:
                print("ERROR: --taxonomy must be valid JSON", file=sys.stderr)
                return 2
        result = run_all(root, scope=args.scope, base=args.base, rng=args.rng,
                         taxonomy=taxonomy, write_baseline=not args.no_baseline)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if result["findings"] else 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
