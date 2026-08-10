#!/usr/bin/env python3
"""Assemble the human audit report from the audit_scan.py findings JSON.

Two commands:

    report_assembler.py fill  --findings F.json [--template T.md]
                              [--project NAME] [--date YYYY-MM-DD]
        Deterministically pre-fills AUDIT-TEMPLATE.md: the executive
        summary count matrix, the P1/P2/P3 buckets, the SCA table, an
        HONEST "Scope and Tools" section (only tools that actually ran),
        and a mandatory "Coverage and limitations" section that names the
        method blindspots (grep-only vs semgrep, offline SCA, CWE/OWASP
        edition, scope). The LLM then writes the narrative Risk/Remediation
        prose on top.

    report_assembler.py delta --before prev.json --after last.json
        Set difference over finding fingerprints -> resolved / new /
        persisted. This is the reliable re-audit delta (no eyeballing).

stdlib-only, no network. Exit 0.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

SEVERITIES = ["critical", "high", "medium", "low", "info"]
_CODE_PHASES = {"sast", "surface"}  # code-domain findings for the matrix


def _load_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _count_matrix(findings: list) -> dict:
    """{domain: {severity: n}} for code / sca / supply / total."""
    zero = {s: 0 for s in SEVERITIES}
    code = dict(zero)
    sca = dict(zero)
    supply = dict(zero)
    for f in findings:
        sev = f.get("severity", "low")
        if sev not in code:
            sev = "low"
        if f.get("phase") == "sca":
            sca[sev] += 1
        elif f.get("phase") == "supply-chain":
            supply[sev] += 1
        else:
            code[sev] += 1
    total = {s: code[s] + sca[s] + supply[s] for s in SEVERITIES}
    return {"code": code, "sca": sca, "supply": supply, "total": total}


def _finding_line(f: dict) -> str:
    loc = f"{f['file']}:{f['line']}" if f.get("line") else f.get("file", "?")
    cwe = f.get("cwe") or "n/a"
    cvss = f" / CVSS {f['cvss']}" if f.get("cvss") else ""
    return (f"- **{f.get('fp', '?')}** - {f.get('severity', '?')} / {cwe}{cvss} / "
            f"`{loc}` (engine: {f.get('engine', '?')}, status: {f.get('status', 'unconfirmed')}) "
            f"- {f.get('message', '')}")


def _bucket(findings: list) -> tuple:
    p1, p2, p3 = [], [], []
    for f in findings:
        sev = f.get("severity", "low")
        if sev in ("critical", "high"):
            p1.append(f)
        elif sev == "medium":
            p2.append(f)
        else:
            p3.append(f)
    key = lambda f: (f.get("file", ""), f.get("line") or 0)
    return sorted(p1, key=key), sorted(p2, key=key), sorted(p3, key=key)


def _tools_block(tools: list) -> str:
    lines = []
    for t in tools:
        extra = ""
        if t.get("ruleset"):
            extra = f" (ruleset: {t['ruleset']})"
        elif t.get("reason"):
            extra = f" ({t['reason']})"
        elif t.get("note"):
            extra = f" ({t['note']})"
        lines.append(f"  - {t.get('name', '?')}: {t.get('status', '?')}{extra}")
    return "\n".join(lines) if lines else "  - (none)"


def _ran_tool_names(tools: list) -> list:
    return [t["name"] for t in tools if t.get("status") == "ran"]


def _limitations_block(result: dict) -> str:
    tools = result.get("tools", [])
    ran = set(_ran_tool_names(tools))
    meta = result.get("meta", {})
    project = result.get("project_type", {})
    taxonomy = result.get("taxonomy", {}) or {}
    lines = ["## Coverage and limitations", ""]
    # SAST depth: three-layer cascade honesty. CodeQL beats semgrep beats grep.
    codeql_ran = [t for t in tools
                  if t.get("status") == "ran" and t.get("name", "").startswith("codeql/")]
    if codeql_ran:
        langs = sorted({t["name"].split("/", 1)[1].split("-", 1)[0]
                        for t in codeql_ran})
        base = f"- SAST: CodeQL taint analysis ({', '.join(langs)})"
        if "semgrep" in ran:
            base += " + semgrep AST rules + grep patterns."
        else:
            base += " + grep patterns (semgrep not on PATH)."
        lines.append(base)
    elif "semgrep" in ran:
        lines.append("- SAST: semgrep AST rules + grep patterns (no CodeQL taint analysis)."
                     " Install codeql for source->sink verification.")
    else:
        lines.append("- SAST: grep patterns only, NO AST/taint analysis. Higher false-negative risk."
                     " Install codeql or semgrep.")
    # Stale CodeQL query pack currency: name each pack older than 90 days.
    for t in codeql_ran:
        age = t.get("pack_age_days")
        if isinstance(age, int) and age > 90:
            lines.append(f"- Query pack currency: {t['name']} is {age} days old."
                         f" Run `codeql pack upgrade {t['name']}` for the latest rules.")
    # Secrets
    if "gitleaks" in ran or "trufflehog" in ran:
        lines.append("- Secrets: dedicated scanner ran.")
    else:
        lines.append("- Secrets: redacting pattern fallback only; git history not fully scanned.")
    # SCA
    sca_ran = {t["name"] for t in tools if t.get("status") == "ran"} & {"npm-audit", "osv-scanner", "pip-audit"}
    if meta.get("offline"):
        lines.append("- SCA: OFFLINE - dependency advisories not fetched; CVE coverage is stale/absent.")
    elif not sca_ran:
        lines.append("- SCA: no dependency scanner ran; vendored/WASM/native deps unscanned.")
    else:
        lines.append(f"- SCA: {', '.join(sorted(sca_ran))} ran; vendored/WASM/git-embedded deps still unscanned.")
    # Supply chain: name what each stage actually did.
    by_name = {t.get("name"): t for t in tools}
    static_names = {"lockfile-provenance", "action-pinning", "install-scripts",
                    "manifest-hygiene", "python-pins"}
    static_ran = sorted(n for n in static_names
                        if by_name.get(n, {}).get("status") == "ran")
    if static_ran:
        lines.append(f"- Supply chain (static): {', '.join(static_ran)} ran;"
                     " YAML checks are regex-based, exotic workflow syntax may"
                     " slip through.")
    elif static_names & set(by_name):
        lines.append("- Supply chain (static): no applicable manifests; checks"
                     " recorded as not-applicable.")
    rebuild = by_name.get("cleanroom-rebuild", {})
    if rebuild.get("status") == "ran":
        if rebuild.get("mismatches", 0):
            lines.append(f"- Clean-room rebuild: MISMATCH in"
                         f" {rebuild['mismatches']} artifact(s); the committed"
                         " artifact does not fall out of the committed sources.")
        else:
            lines.append(f"- Clean-room rebuild: byte-identical"
                         f" ({rebuild.get('artifacts', '?')} artifact(s))."
                         " Proves mapping fidelity, not benignity.")
    elif rebuild:
        lines.append(f"- Clean-room rebuild: not run"
                     f" ({rebuild.get('reason', 'opt-in')}).")
    attest = by_name.get("gh-attestation", {})
    if attest.get("status") == "ran":
        lines.append(f"- Release attestation: verified against release"
                     f" {attest.get('release', '?')}"
                     f" ({attest.get('assets', '?')} asset(s)).")
    elif attest:
        lines.append(f"- Release attestation: not run"
                     f" ({attest.get('reason', 'opt-in')}).")
    # No DAST
    lines.append("- No DAST/runtime testing (except opt-in isolated PoC probes); this is static analysis.")
    # Scope
    lines.append(f"- Scope: {result.get('scope', '?')} ({result.get('scope_detail', '')}); "
                 f"{meta.get('file_count', '?')} files in reported scope.")
    # Taxonomy editions
    if taxonomy:
        edition_bits = ", ".join(f"{k} {v}" for k, v in taxonomy.items())
        lines.append(f"- Threat taxonomy snapshot: {edition_bits}.")
    else:
        lines.append("- Threat taxonomy: bundled baseline (edition unrecorded); live-currency step not snapshotted.")
    # Project kinds not covered
    kinds = project.get("project_kinds", [])
    if kinds:
        lines.append(f"- Detected project kinds: {', '.join(kinds)}.")
    return "\n".join(lines)


def fill(result: dict, template: str, project: str = "{Projektname}",
         date: str = "{YYYY-MM-DD}") -> str:
    findings = result.get("findings", [])
    matrix = _count_matrix(findings)
    p1, p2, p3 = _bucket(findings)

    overall = "Low"
    if matrix["total"]["critical"]:
        overall = "Critical"
    elif matrix["total"]["high"]:
        overall = "High"
    elif matrix["total"]["medium"]:
        overall = "Medium"

    scope_label = result.get("scope", "full")
    scan_scope = f"{scope_label} ({result.get('scope_detail', '')})"

    out = template

    # Metadata table.
    out = out.replace("{Projektname}", project)
    out = out.replace("{YYYY-MM-DD}", date)
    out = out.replace("{Full / Partial, welche Phasen}", scan_scope)
    out = out.replace("{Critical / High / Medium / Low}", overall, 1)

    # Executive summary matrix: replace the three data rows.
    def _row(cells):
        return " | ".join(str(c) for c in cells)

    code = matrix["code"]; sca = matrix["sca"]; tot = matrix["total"]
    supply = matrix["supply"]
    out = out.replace(
        "| Code findings (SAST, OWASP, Zero Trust, Quality) | {n} | {n} | {n} | {n} | {n} |",
        f"| Code findings (SAST, OWASP, Zero Trust, Quality) | {code['critical']} | {code['high']} | {code['medium']} | {code['low']} | {code['info']} |",
    )
    out = out.replace(
        "| SCA (Dependencies) | {n} | {n} | {n} | {n} | {n} |",
        f"| SCA (Dependencies) | {sca['critical']} | {sca['high']} | {sca['medium']} | {sca['low']} | {sca['info']} |",
    )
    out = out.replace(
        "| Supply chain (provenance, build integrity) | {n} | {n} | {n} | {n} | {n} |",
        f"| Supply chain (provenance, build integrity) | {supply['critical']} | {supply['high']} | {supply['medium']} | {supply['low']} | {supply['info']} |",
    )
    out = out.replace(
        "| License Compliance | {n} | {n} | {n} | {n} | {n} |",
        "| License Compliance | 0 | 0 | 0 | 0 | 0 |",
    )
    out = out.replace(
        "| Total | {n} | {n} | {n} | {n} | {n} |",
        f"| Total | {tot['critical']} | {tot['high']} | {tot['medium']} | {tot['low']} | {tot['info']} |",
    )

    # Finding buckets: replace each placeholder bullet with real lines.
    def _bucket_text(items):
        return "\n".join(_finding_line(f) for f in items) if items else "- (none)"

    out = out.replace(
        "### P1: Must Fix (Critical + High)\n\n- {Finding-Zeile}",
        "### P1: Must Fix (Critical + High)\n\n" + _bucket_text(p1),
    )
    out = out.replace(
        "### P2: Should Fix (Medium)\n\n- {Finding-Zeile}",
        "### P2: Should Fix (Medium)\n\n" + _bucket_text(p2),
    )
    out = out.replace(
        "### P3: Consider (Low + Info)\n\n- {Finding-Zeile}",
        "### P3: Consider (Low + Info)\n\n" + _bucket_text(p3),
    )

    # SCA table rows.
    sca_rows = [f for f in findings if f.get("phase") == "sca"]
    if sca_rows:
        rows = "\n".join(
            f"| {f.get('message', '?')} | - | {f.get('cwe') or '-'} | {f.get('severity')} | - |"
            for f in sca_rows
        )
        out = out.replace("| {pkg} | {ver} | {CVE-ID} | {sev} | {fix} |", rows)

    # Supply-chain table rows.
    supply_rows = [f for f in findings if f.get("phase") == "supply-chain"]
    if supply_rows:
        rows = "\n".join(
            f"| {f.get('message', '?')} | {f.get('severity')} | {f.get('cwe') or '-'} | "
            f"`{f.get('file', '?')}` |"
            for f in supply_rows
        )
        out = out.replace("| {finding} | {sev} | {cwe} | {loc} |", rows)

    # Honest tools + files + limitations in the Scope and Tools section.
    ran = _ran_tool_names(result.get("tools", []))
    out = out.replace(
        "- Tools: {z.B. semgrep, npm audit, custom CWE patterns}",
        "- Tools (full ledger):\n" + _tools_block(result.get("tools", []))
        + f"\n- Tools that produced results: {', '.join(ran) if ran else '(none)'}",
    )
    out = out.replace(
        "- Files analyzed: {Pfade oder Anzahl, kurz}",
        f"- Files analyzed: {result.get('meta', {}).get('file_count', '?')} "
        f"(scope: {scope_label})",
    )
    out = out.replace(
        "- Excluded: {Was bewusst nicht geprüft wurde, plus Grund}",
        "- Excluded: see Coverage and limitations below.",
    )

    # Replace the template's Coverage-and-limitations stub with the
    # generated block. The template stub only exists so the section
    # is visible when someone opens the raw template; at fill time
    # `_limitations_block` produces the honest, project-specific content
    # and the stub would just be a duplicate.
    marker = "## Coverage and limitations"
    idx = out.find(marker)
    if idx != -1:
        out = out[:idx].rstrip()
        # Drop the separator that used to divide the previous section
        # from the (now removed) template stub; otherwise the appended
        # block below would double up the horizontal rule.
        if out.endswith("---"):
            out = out[:-3].rstrip()
    out = out.rstrip() + "\n\n---\n\n" + _limitations_block(result) + "\n"
    return out


def delta_from_files(before_path: Path, after_path: Path) -> dict:
    before = _load_json(before_path)
    after = _load_json(after_path)
    b = [f["fp"] for f in before.get("findings", []) if "fp" in f]
    a = [f["fp"] for f in after.get("findings", []) if "fp" in f]
    bs, as_ = set(b), set(a)
    return {
        "before": len(bs),
        "after": len(as_),
        "resolved": sorted(bs - as_),
        "new": sorted(as_ - bs),
        "persisted": sorted(bs & as_),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Assemble audit report / compute re-audit delta.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_fill = sub.add_parser("fill")
    p_fill.add_argument("--findings", required=True)
    p_fill.add_argument("--template", default=None)
    p_fill.add_argument("--project", default="{Projektname}")
    p_fill.add_argument("--date", default="{YYYY-MM-DD}")

    p_delta = sub.add_parser("delta")
    p_delta.add_argument("--before", required=True)
    p_delta.add_argument("--after", required=True)

    args = ap.parse_args(argv)

    if args.cmd == "fill":
        result = _load_json(Path(args.findings))
        template_path = Path(args.template) if args.template else (
            Path(__file__).resolve().parent.parent / "templates" / "AUDIT-TEMPLATE.md")
        template = template_path.read_text(encoding="utf-8")
        print(fill(result, template, project=args.project, date=args.date))
        return 0

    if args.cmd == "delta":
        d = delta_from_files(Path(args.before), Path(args.after))
        print(json.dumps(d, indent=2, ensure_ascii=False))
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
