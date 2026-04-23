# Dateinamen-Konventionen -- Vollstaendige Referenz

## Analyse-Dokumente

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| Business Analysis | `BA-{PROJECT}.md` | `BA-myapp.md`, `BA-intranet-portal.md` |
| Constitution | `constitution-draft.md` | Fester Name, ein pro Projekt |
| Security Audit | `AUDIT-{PROJECT}-{YYYY-MM-DD}.md` | `AUDIT-myapp-2026-03-22.md` |

## Requirements-Dokumente

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| Epic | `EPIC-{NNN}-{slug}.md` | `EPIC-001-ai-agent-core.md` |
| Feature | `FEATURE-{EPIC}-{NNN}-{slug}.md` | `FEATURE-001-001-semantic-search.md`, `FEATURE-013-002-reindex-job.md` |
| Architect Handoff | `architect-handoff.md` | Fester Name |
| Plan Context | `plan-context.md` | Fester Name |

## Architektur-Dokumente

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| ADR | `ADR-{NNN}-{slug}.md` | `ADR-003-embedding-provider.md` |
| arc42 | `arc42.md` | Fester Name, ein pro Projekt |

## Backlog & Context

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| Backlog | `10_backlog.md` | Fester Name, Struktur per `BACKLOG-TEMPLATE.md` |
| Bug Log | `20_bugs.md` | Fester Name, FIX-NN Eintraege |
| Handoffs | `30_handoffs.md` | Fester Name, append-only |
| Memory | `MEMORY.md` | Fester Name |

## Fix- und Improvement-Artefakte

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| Fix | `docs/context/fixes/FIX-{NNN}-{slug}.md` | `FIX-001-auth-token-leak.md` |
| Improvement | `docs/context/improvements/IMP-{NNN}-{slug}.md` | `IMP-001-reindex-perf.md`, `IMP-007-doc-drift.md` |

- `FIX` und `IMP` sind 3-stellig fortlaufend, projekt-global (nicht
  epic-lokal).
- Frontmatter-Pflicht: `feature:` und `epic:` (Bindung an existierendes
  Feature/Epic). Ohne diese Bindung ist das Artefakt ein Orphan und wird
  von `/consistency-check` geflaggt.
- FIX-Eintraege zusaetzlich im Bug Log `20_bugs.md` verlinken.

## Regeln fuer Nummern

- Epics und ADRs immer 3-stellig: `001`, `042`, `103`
- Features epic-lokal im Muster `{EPIC}-{NNN}`:
  - `EPIC` = 3-stellige Epic-Nummer (identisch zur Nummer im
    Epic-Dateinamen)
  - `NNN` = 3-stellige Feature-Nummer lokal zum Epic
  - Epic 001 -> FEATURE-001-001, FEATURE-001-002, ...
  - Epic 013 -> FEATURE-013-001, FEATURE-013-002, ...
- Fortlaufend innerhalb des jeweiligen Scopes
- Keine Luecken erzwingen (042 nach 041, nicht nach 040)
- Nummern werden NICHT wiederverwendet
- 3-stellig auf beiden Seiten der Feature-ID haelt alphabetische
  Sortierung stabil (FEATURE-002-001 vor FEATURE-010-001)

## Regeln fuer Slugs

- Immer kebab-case: `semantic-search`, `api-key-storage`
- Nur ASCII: keine Umlaute, keine Sonderzeichen
- Kurz aber aussagekraeftig: 2-5 Woerter
- Englisch (auch in deutschen Kontexten)

## Regeln fuer Datums-Formate

- Immer ISO 8601: `YYYY-MM-DD`
- In Dateinamen: `2026-03-22`
- In Dokumenten-Headern: `2026-03-22`

## Regeln fuer Projekt-Namen in Dateinamen

- Lowercase, keine Sonderzeichen
- Kurzform des Projektnamens: `myapp`, `intranet-portal`, `af-gateway`
- Konsistent innerhalb eines Projekts

## Anti-Patterns

| Falsch | Richtig | Grund |
|--------|---------|-------|
| `ADR-1-framework.md` | `ADR-001-framework.md` | 3-stellig |
| `adr-001-framework.md` | `ADR-001-framework.md` | Prefix uppercase |
| `ADR-001-Backend Framework.md` | `ADR-001-backend-framework.md` | Keine Leerzeichen |
| `FEATURE-042-search.md` | `FEATURE-001-001-search.md` | Epic-lokal, `{EPIC}-{NNN}` |
| `FEATURE-1-1-Suche.md` | `FEATURE-001-001-search.md` | 3-stellig, Englisch, kebab |
| `BA_myapp.md` | `BA-myapp.md` | Bindestrich, nicht Unterstrich |
| `audit-myapp.md` | `AUDIT-myapp-2026-03-22.md` | Prefix uppercase, Datum |
