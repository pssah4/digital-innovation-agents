# Dateinamen-Konventionen -- Vollstaendige Referenz

## Analyse-Dokumente (`_devprocess/analysis/`)

Flache Ablage. Prefix pro Artefakttyp. Keine Unterordner pro Typ.
Einzige Ausnahme: `sources/` fuer User-bereitgestellte Quellen.

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| Project-BA (Singleton) | `BA-{PROJECT}.md` | `BA-myapp.md`, `BA-intranet-portal.md` |
| Item-BA fuer Epic | `BA-EPIC-{nn}-{slug}.md` | `BA-EPIC-04-onboarding.md` |
| Item-BA fuer Feature | `BA-FEAT-{ee}-{ff}-{slug}.md` | `BA-FEAT-04-02-magic-link-login.md` |
| Item-BA fuer Improvement | `BA-IMP-{ee}-{ff}-{nn}-{slug}.md` | `BA-IMP-04-02-01-reduce-onboarding-steps.md` |
| Item-BA fuer Fix | `BA-FIX-{ee}-{ff}-{nn}-{slug}.md` | `BA-FIX-04-02-03-magic-link-expiry-bug.md` |
| Exploration Board | `EXPLORE-{PROJECT}.md` | `EXPLORE-myapp.md` |
| Security Audit | `AUDIT-{PROJECT}-{YYYY-MM-DD}.md` | `AUDIT-myapp-2026-03-22.md` |
| Research-Notiz | `RESEARCH-{TOPIC}.md` | `RESEARCH-pricing.md` (optional, n pro Projekt) |
| ADR-Review | `ADR-{nn}-review.md` | Mid-course Root-Cause-Notiz fuer ADR-Aenderung |
| Constitution | `constitution-draft.md` | Fester Name, ein pro Projekt |
| User-Quelle | `SOURCE-{name}.{ext}` | Liegt in `analysis/sources/`, nicht im Wurzelordner |

## Requirements-Dokumente

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| Epic | `EPIC-{nn}-{slug}.md` | `EPIC-01-ai-agent-core.md` |
| Feature | `FEAT-{ee}-{ff}-{slug}.md` | `FEAT-01-01-semantic-search.md`, `FEAT-13-02-reindex-job.md` |
| Architect Handoff | `architect-handoff.md` | Fester Name |
| Plan Context | `plan-context.md` | Fester Name |

## Architektur-Dokumente

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| ADR | `ADR-{nn}-{slug}.md` | `ADR-03-embedding-provider.md` |
| arc42 | `arc42.md` | Fester Name, ein pro Projekt |

## Backlog & Context

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| Backlog | `BACKLOG.md` | Fester Name, Struktur per `BACKLOG-TEMPLATE.md`, FIX-Rows leben hier |
| Handoffs | `HANDOFFS.md` | Fester Name, append-only |
| Memory | `MEMORY.md` | Fester Name |

## Fix- und Improvement-Artefakte

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| Fix | `_devprocess/requirements/fixes/FIX-{ee}-{ff}-{nn}-{slug}.md` | `FIX-001-auth-token-leak.md` |
| Improvement | `_devprocess/requirements/improvements/IMP-{ee}-{ff}-{nn}-{slug}.md` | `IMP-001-reindex-perf.md`, `IMP-007-doc-drift.md` |

- `FIX` und `IMP` sind feature-lokal nummeriert: `FIX-{ee}-{ff}-{nn}`
  bzw. `IMP-{ee}-{ff}-{nn}`. `{ee}` Epic, `{ff}` Feature, `{nn}` Counter
  lokal zum Feature.
- Frontmatter-Pflicht: `feature:` und `epic:` (Bindung an existierendes
  Feature/Epic). Ohne diese Bindung ist das Artefakt ein Orphan und wird
  von `/consistency-check` geflaggt.
- FIX-Eintraege erscheinen als Row im `BACKLOG.md` und als Detail-Datei
  in `_devprocess/requirements/fixes/`. Es gibt keine separate Bug-Log-
  Aggregationsdatei.

## Regeln fuer Nummern

- Epics und ADRs immer 3-stellig: `001`, `042`, `103`
- Features epic-lokal im Muster `FEAT-{ee}-{ff}`:
  - `EPIC` = 3-stellige Epic-Nummer (identisch zur Nummer im
    Epic-Dateinamen)
  - `NNN` = 3-stellige Feature-Nummer lokal zum Epic
  - Epic 01 -> FEAT-01-01, FEAT-01-02, ...
  - Epic 13 -> FEAT-13-01, FEAT-13-02, ...
- Fortlaufend innerhalb des jeweiligen Scopes
- Keine Luecken erzwingen (042 nach 041, nicht nach 040)
- Nummern werden NICHT wiederverwendet
- 3-stellig auf beiden Seiten der Feature-ID haelt alphabetische
  Sortierung stabil (FEAT-02-01 vor FEAT-10-01)

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
| `ADR-1-framework.md` | `ADR-01-framework.md` | 3-stellig |
| `adr-001-framework.md` | `ADR-01-framework.md` | Prefix uppercase |
| `ADR-01-Backend Framework.md` | `ADR-01-backend-framework.md` | Keine Leerzeichen |
| `FEAT-NN-42-search.md` | `FEAT-01-01-search.md` | Epic-lokal, `FEAT-{ee}-{ff}` |
| `FEATURE-1-1-Suche.md` | `FEAT-01-01-search.md` | 3-stellig, Englisch, kebab |
| `BA_myapp.md` | `BA-myapp.md` | Bindestrich, nicht Unterstrich |
| `audit-myapp.md` | `AUDIT-myapp-2026-03-22.md` | Prefix uppercase, Datum |
| `EPIC-04-ba.md` (in `requirements/epics/`) | `BA-EPIC-04-{slug}.md` (in `analysis/`) | Item-BA lebt in `analysis/`, nicht neben dem Epic |
| `BA-EPIC-onboarding.md` | `BA-EPIC-04-onboarding.md` | ID des Ziel-Items mitfuehren |
| `BA-feat-04-02-login.md` | `BA-FEAT-04-02-login.md` | Item-Typ uppercase |
