# Dateinamen-Konventionen -- Vollstaendige Referenz

## Analyse-Dokumente

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| Business Analysis | `BA-{PROJECT}.md` | `BA-obsilo.md`, `BA-downstream-portal.md` |
| Constitution | `constitution-draft.md` | Fester Name, ein pro Projekt |
| Security Audit | `AUDIT-{PROJECT}-{YYYY-MM-DD}.md` | `AUDIT-obsilo-2026-03-22.md` |

## Requirements-Dokumente

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| Epic | `EPIC-{XXX}-{slug}.md` | `EPIC-001-ai-agent-core.md` |
| Feature | `FEATURE-{XXX}-{slug}.md` | `FEATURE-042-semantic-search.md` |
| Architect Handoff | `architect-handoff.md` | Fester Name |
| Plan Context | `plan-context.md` | Fester Name |

## Architektur-Dokumente

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| ADR | `ADR-{XXX}-{slug}.md` | `ADR-003-embedding-provider.md` |
| arc42 | `arc42.md` | Fester Name, ein pro Projekt |

## Backlog & Context

| Typ | Muster | Beispiele |
|-----|--------|-----------|
| Backlog | `10_backlog.md` | Fester Name |
| Memory | `MEMORY.md` | Fester Name |

## Regeln fuer Nummern

- Immer 3-stellig: `001`, `042`, `103`
- Fortlaufend innerhalb eines Typs
- Keine Luecken erzwingen (042 nach 041, nicht nach 040)
- Nummern werden NICHT wiederverwendet

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
- Kurzform des Projektnamens: `obsilo`, `downstream-portal`, `af-gateway`
- Konsistent innerhalb eines Projekts

## Anti-Patterns

| Falsch | Richtig | Grund |
|--------|---------|-------|
| `ADR-1-framework.md` | `ADR-001-framework.md` | 3-stellig |
| `adr-001-framework.md` | `ADR-001-framework.md` | Prefix uppercase |
| `ADR-001-Backend Framework.md` | `ADR-001-backend-framework.md` | Keine Leerzeichen |
| `FEATURE-42-Suche.md` | `FEATURE-042-search.md` | 3-stellig, Englisch, kebab |
| `BA_obsilo.md` | `BA-obsilo.md` | Bindestrich, nicht Unterstrich |
| `audit-obsilo.md` | `AUDIT-obsilo-2026-03-22.md` | Prefix uppercase, Datum |
