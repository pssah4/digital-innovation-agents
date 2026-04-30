#!/usr/bin/env python3
"""
V-Model Graph Parser.

Liest die Markdown-Artefakte unter `<root>/` (entweder `docs/` oder
`_devprocess/`) und baut daraus einen Graph aus Knoten (BA-Personas,
Epics, Features, ADRs, PLANs, BL-Items) und Kanten (Zugehoerigkeit,
Referenzen). Gibt das Ergebnis als JSON auf stdout aus, kompatibel
mit graph-viewer.html.

Aufruf:
    python3 parse-graph.py <root>
    python3 parse-graph.py docs

Keine externen Dependencies, nur stdlib.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any


# -----------------------------
# Regex-Helfer
# -----------------------------

RE_EPIC_FILE = re.compile(r"EPIC-(\d+)-.*\.md$")
RE_FEATURE_FILE = re.compile(r"FEATURE-(\d+)(?:-(\d+))?-.*\.md$")
RE_ADR_FILE = re.compile(r"ADR-(\d+)-.*\.md$")
RE_PLAN_FILE = re.compile(r"PLAN-(\d+)-.*\.md$")

RE_EPIC_LINK = re.compile(r"EPIC-(\d+)")
RE_FEATURE_LINK = re.compile(r"FEATURE-(\d{3})(?:-(\d+))?")
RE_ADR_LINK = re.compile(r"ADR-(\d+)")
RE_PLAN_LINK = re.compile(r"PLAN-(\d+)")
RE_BL_LINK = re.compile(r"BL-(\d+)")

RE_PERSONA_HEADER = re.compile(r"^#{3,4}\s+Persona\s+([0-9a-z]+):\s*(.*?)$", re.MULTILINE | re.IGNORECASE)

RE_MARKDOWN_LINK = re.compile(r"\[(?P<label>[^\]]+)\]\((?P<path>[^)]+)\)")


# -----------------------------
# IO-Helfer
# -----------------------------

def find_root(arg: str | None) -> Path:
    """Prueft ob docs/ oder _devprocess/ relativ zum Argument existiert."""
    candidate = Path(arg or ".").resolve()
    if candidate.name in ("docs", "_devprocess") and candidate.is_dir():
        return candidate
    for sub in ("docs", "_devprocess"):
        if (candidate / sub).is_dir():
            return candidate / sub
    raise SystemExit(
        f"Kein docs/ oder _devprocess/ unter {candidate} gefunden"
    )


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def normalize_adr_id(raw: str) -> str:
    return f"ADR-{int(raw):03d}"


def normalize_epic_id(raw: str) -> str:
    return f"EPIC-{int(raw):03d}"


def normalize_feature_id(raw_epic: str, raw_nnn: str | None) -> str:
    """Supports both FEATURE-NNN and FEATURE-EPIC-NNN styles."""
    if raw_nnn:
        return f"FEATURE-{int(raw_epic):03d}-{int(raw_nnn):03d}"
    return f"FEATURE-{int(raw_epic):03d}"


def normalize_plan_id(raw: str) -> str:
    return f"PLAN-{int(raw):03d}"


def normalize_bl_id(raw: str) -> str:
    return f"BL-{int(raw):03d}"


# -----------------------------
# Parser
# -----------------------------

class GraphBuilder:
    def __init__(self, root: Path):
        self.root = root
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: list[dict[str, Any]] = []

    def add_node(self, node_id: str, type_: str, label: str, **attrs) -> None:
        if node_id in self.nodes:
            # Update bestehende Node, keine Duplikate
            self.nodes[node_id].update({k: v for k, v in attrs.items() if v is not None})
            return
        node = {"id": node_id, "type": type_, "label": label}
        node.update({k: v for k, v in attrs.items() if v is not None})
        self.nodes[node_id] = node

    def add_edge(self, source: str, target: str, label: str = "") -> None:
        if source == target:
            return
        # Dedupe
        key = (source, target, label)
        if any((e["source"], e["target"], e.get("label", "")) == key for e in self.edges):
            return
        self.edges.append({"source": source, "target": target, "label": label})

    # ---- Epic -----
    def parse_epics(self) -> None:
        epic_dir = self.root / "requirements" / "epics"
        if not epic_dir.is_dir():
            return
        for fp in sorted(epic_dir.glob("EPIC-*.md")):
            m = RE_EPIC_FILE.search(fp.name)
            if not m:
                continue
            eid = normalize_epic_id(m.group(1))
            txt = read_text(fp)
            title = self._extract_title(txt) or eid
            self.add_node(eid, "Epic", title, path=str(fp))
            # Feature-Links in MVP-Features-Tabelle -> edges spaeter aus Feature-Seite
            # Persona-Mention in den ersten 100 Zeilen
            for pm in RE_PERSONA_HEADER.finditer(txt[:4000]):
                pid = f"Persona-{pm.group(1)}"
                self.add_node(pid, "Persona", pm.group(2).strip() or pid)

    # ---- Feature -----
    def parse_features(self) -> None:
        feat_dir = self.root / "requirements" / "features"
        if not feat_dir.is_dir():
            return
        for fp in sorted(feat_dir.glob("FEATURE-*.md")):
            m = RE_FEATURE_FILE.search(fp.name)
            if not m:
                continue
            fid = normalize_feature_id(m.group(1), m.group(2))
            txt = read_text(fp)
            title = self._extract_title(txt) or fid
            status = self._extract_frontmatter_field(txt, "status")
            phase = self._extract_phase_from_verification(txt)
            self.add_node(fid, "Feature", title, path=str(fp), status=status, phase=phase)
            # Epic-Link: erste EPIC-Referenz im Header-Block
            head = txt[:2500]
            em = RE_EPIC_LINK.search(head)
            if em:
                eid = normalize_epic_id(em.group(1))
                self.add_node(eid, "Epic", eid)  # placeholder falls noch nicht gesehen
                self.add_edge(eid, fid, "enthaelt")
            # ADR-Links: im ganzen Body
            for am in RE_ADR_LINK.finditer(txt):
                aid = normalize_adr_id(am.group(1))
                self.add_node(aid, "ADR", aid)
                self.add_edge(fid, aid, "referenziert")

    # ---- ADR -----
    def parse_adrs(self) -> None:
        adr_dir = self.root / "adr"
        if not adr_dir.is_dir():
            # Fallback: architecture/
            adr_dir = self.root / "architecture"
        if not adr_dir.is_dir():
            return
        for fp in sorted(adr_dir.glob("ADR-*.md")):
            m = RE_ADR_FILE.search(fp.name)
            if not m:
                continue
            aid = normalize_adr_id(m.group(1))
            txt = read_text(fp)
            title = self._extract_title(txt) or aid
            status = self._extract_adr_status(txt)
            phase = self._extract_phase_from_verification(txt)
            self.add_node(aid, "ADR", title, path=str(fp), status=status, phase=phase)
            # ADR-to-ADR Supersedes
            for am in RE_ADR_LINK.finditer(txt):
                other = normalize_adr_id(am.group(1))
                if other == aid:
                    continue
                # Wir registrieren nur die Zielknoten, keine Kante (redundant zu Feature-Refs)

    # ---- PLAN -----
    def parse_plans(self) -> None:
        plan_dir = self.root / "implementation" / "plans"
        if not plan_dir.is_dir():
            return
        for fp in sorted(plan_dir.glob("PLAN-*.md")):
            m = RE_PLAN_FILE.search(fp.name)
            if not m:
                continue
            pid = normalize_plan_id(m.group(1))
            txt = read_text(fp)
            title = self._extract_title(txt) or pid
            status = self._extract_frontmatter_field(txt, "status")
            self.add_node(pid, "PLAN", title, path=str(fp), status=status)
            # feature-refs im Frontmatter
            refs = self._extract_frontmatter_field(txt, "feature-refs") or ""
            for m2 in RE_FEATURE_LINK.finditer(refs):
                fid = normalize_feature_id(m2.group(1), m2.group(2))
                self.add_node(fid, "Feature", fid)
                self.add_edge(pid, fid, "realisiert")
            adr_refs = self._extract_frontmatter_field(txt, "adr-refs") or ""
            for m2 in RE_ADR_LINK.finditer(adr_refs):
                aid = normalize_adr_id(m2.group(1))
                self.add_node(aid, "ADR", aid)
                self.add_edge(pid, aid, "realisiert")

    # ---- Backlog -----
    def parse_backlog(self) -> None:
        bl_file = self.root / "context" / "BACKLOG.md"
        if not bl_file.is_file():
            return
        txt = read_text(bl_file)
        # Jede BL-Zeile
        # Heuristik: Zeilen mit "BL-NNN" als erster Spalte
        for line in txt.splitlines():
            line = line.strip()
            if not line.startswith("| BL-"):
                continue
            bm = RE_BL_LINK.match(line[2:])  # skip "| "
            if not bm:
                continue
            bid = normalize_bl_id(bm.group(1))
            # Title = zweite Spalte
            cols = [c.strip() for c in line.split("|")[1:-1]]
            title = cols[1] if len(cols) > 1 else bid
            self.add_node(bid, "BL-Item", title, path=str(bl_file))
            # Parse alle Refs in der Zeile
            for m2 in RE_FEATURE_LINK.finditer(line):
                fid = normalize_feature_id(m2.group(1), m2.group(2))
                self.add_node(fid, "Feature", fid)
                self.add_edge(bid, fid, "zeigt auf")
            for m2 in RE_ADR_LINK.finditer(line):
                aid = normalize_adr_id(m2.group(1))
                self.add_node(aid, "ADR", aid)
                self.add_edge(bid, aid, "zeigt auf")
            for m2 in RE_PLAN_LINK.finditer(line):
                pid = normalize_plan_id(m2.group(1))
                self.add_node(pid, "PLAN", pid)
                self.add_edge(bid, pid, "zeigt auf")

    # ---- Hilfen -----
    def _extract_title(self, txt: str) -> str:
        for line in txt.splitlines()[:30]:
            line = line.strip()
            if line.startswith("# "):
                return line.lstrip("# ").strip()
        return ""

    def _extract_frontmatter_field(self, txt: str, field: str) -> str | None:
        if not txt.startswith("---"):
            return None
        end = txt.find("---", 3)
        if end < 0:
            return None
        head = txt[3:end]
        m = re.search(rf"^{re.escape(field)}\s*:\s*(.+)$", head, re.MULTILINE)
        return m.group(1).strip() if m else None

    def _extract_adr_status(self, txt: str) -> str | None:
        m = re.search(r"\*\*Status:\*\*\s*([^\n]+)", txt) or re.search(r"-\s*\*\*Status\*\*\s*:\s*([^\n]+)", txt)
        if m:
            return m.group(1).strip()
        return self._extract_frontmatter_field(txt, "status")

    def _extract_phase_from_verification(self, txt: str) -> str | None:
        m = re.search(r"##\s+Codebase-Verifikation.*?\n.*?\*\*Phase:\*\*\s*(\w+)", txt, re.DOTALL)
        return m.group(1).strip() if m else None

    # ---- Orphan-Check -----
    def mark_orphans(self) -> None:
        in_edges: dict[str, int] = {}
        out_edges: dict[str, int] = {}
        for e in self.edges:
            in_edges[e["target"]] = in_edges.get(e["target"], 0) + 1
            out_edges[e["source"]] = out_edges.get(e["source"], 0) + 1

        for nid, node in self.nodes.items():
            has_in = in_edges.get(nid, 0) > 0
            has_out = out_edges.get(nid, 0) > 0

            # Features ohne Epic-Parent (no inbound from Epic)
            if node["type"] == "Feature":
                epic_parents = [e for e in self.edges if e["target"] == nid and
                                self.nodes.get(e["source"], {}).get("type") == "Epic"]
                if not epic_parents:
                    node["orphan"] = True
            # ADRs ohne eingehende Referenz
            elif node["type"] == "ADR":
                if not has_in:
                    node["orphan"] = True
            # Epics ohne Feature-Children
            elif node["type"] == "Epic":
                feat_children = [e for e in self.edges if e["source"] == nid and
                                 self.nodes.get(e["target"], {}).get("type") == "Feature"]
                if not feat_children:
                    node["orphan"] = True

    def build(self) -> dict[str, Any]:
        self.parse_epics()
        self.parse_features()
        self.parse_adrs()
        self.parse_plans()
        self.parse_backlog()
        self.mark_orphans()
        return {
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
            "meta": {
                "root": str(self.root),
                "generated_by": "dia-orchestrator/tools/parse-graph.py",
            },
        }


def main() -> int:
    arg = sys.argv[1] if len(sys.argv) > 1 else "."
    root = find_root(arg)
    graph = GraphBuilder(root).build()
    json.dump(graph, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
