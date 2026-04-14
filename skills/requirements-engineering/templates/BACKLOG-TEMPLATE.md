# Backlog -- {PROJECT}

> Single Source of Truth fuer den Projektstand. Lebendes zentrales
> PM-Artefakt des V-Model-Workflows. Wird nach JEDER Status-aendernden
> Aktion vom ausfuehrenden Agent (oder User) aktualisiert.
>
> Pflegende Skills: `/business-analyse`, `/requirements-engineering`,
> `/reverse-engineering`, `/security-audit`, `/coding`, `/testing`.
>
> Querverweise: Bugs leben in `20_bugs.md` (FIX-NN) und werden hier nur
> referenziert. Handoffs in `30_handoffs.md`.

Letztes Update: {YYYY-MM-DD} durch {skill oder user}

---

## Dashboard

| Status   | Count | | Prioritaet | Count |
|----------|-------|-|------------|-------|
| Planned  | 0     | | P0         | 0     |
| Active   | 0     | | P1         | 0     |
| Review   | 0     | | P2         | 0     |
| Done     | 0     | | P3         | 0     |
| Waiting  | 0     | |            |       |
| Deferred | 0     | |            |       |

Counts werden bei jedem Backlog-Write vom schreibenden Agent aktualisiert.

---

## Legende

**Status:**

- `Planned`  -- eingetragen, noch nicht gestartet
- `Active`   -- in Bearbeitung (Spec-, Plan- und Impl-Phase zusammengefasst)
- `Review`   -- Arbeit abgeschlossen, in Review
- `Done`     -- fertig, Eintrag bleibt beim zugehoerigen Epic
- `Waiting`  -- blockiert, wartet auf Entscheidung oder Abhaengigkeit
- `Deferred` -- bewusst zurueckgestellt, nicht committed

**Prioritaet:**

- `P0` -- Blocker, sofort
- `P1` -- kurzfristig
- `P2` -- mittelfristig
- `P3` -- Idee, nicht committed

**Typ:** `Feature` | `Enhancement` | `Chore` | `Security` | `Bug-Followup`

**Source:** `BA` | `RE` | `REV` (Reverse-Engineering) | `SEC` | `USER` | `BUG`

**ID-Schema:** `BL-NNN` fortlaufend, monoton, nie wiederverwendet.

---

## Aktive Epics

### EPIC-001: {Epic-Titel}

Link: `_devprocess/requirements/epics/EPIC-001-{slug}.md`
Status: In Arbeit | Zielzeitraum: {Q2 2026}

| ID     | Titel        | Typ     | Prio | Status  | Feature-Spec    | ADR     | Source | Commit    | Notizen    |
|--------|--------------|---------|------|---------|-----------------|---------|--------|-----------|------------|
| BL-001 | Kurzer Titel | Feature | P1   | Active  | FEATURE-001-001 | ADR-003 | BA     | --        | kurze Note |
| BL-002 | Kurzer Titel | Chore   | P2   | Planned | --              | --      | REV    | --        |            |
| BL-003 | Kurzer Titel | Feature | P1   | Done    | FEATURE-001-002 | ADR-002 | BA     | `a1b2c3d` | 2026-04-10 |

---

### EPIC-002: {Epic-Titel}

{...}

---

## Standalone Items (ohne Epic)

Eintraege ohne Epic-Zuordnung: Reverse-Engineering-Funde,
Security-Findings, direkte Stakeholder-Requests, technische Schuld.

| ID     | Titel                    | Typ      | Prio | Status  | Evidence              | Source | Commit | Notizen |
|--------|--------------------------|----------|------|---------|-----------------------|--------|--------|---------|
| BL-050 | CSRF-Token fehlt         | Security | P1   | Planned | `src/api/login.ts:88` | SEC    | --     | H-2     |
| BL-051 | Veraltete lodash-Version | Chore    | P3   | Planned | `package.json`        | REV    | --     |         |

---

## Offene Bugs (Referenz)

Details in `_devprocess/context/20_bugs.md`. Hier nur Kurzliste fuer den
PM-Ueberblick. Diese Zeilen werden von `/coding` synchronisiert.

| FIX-ID | Titel              | Prio | Status | Bezug                      |
|--------|--------------------|------|--------|----------------------------|
| FIX-01 | Login-Race bei SSO | P0   | Open   | EPIC-001 / FEATURE-001-001 |

---

## Deferred / Ideen

Bewusst zurueckgestellte Items. Keine SLA, keine Zusage. Werden bei Bedarf
in "Aktive Epics" oder "Standalone Items" hochgezogen.

| ID     | Titel | Grund                       | Wiedervorlage |
|--------|-------|-----------------------------|---------------|
| BL-099 | {...} | Wartet auf ADR-Entscheidung | Q3 2026       |

---

## Traceability-Konvention

Jeder Eintrag MUSS, sofern vorhanden, folgende Verweise fuehren. Damit
bildet das Backlog die Kette `Backlog -> FEATURE -> ADR -> Commit` als
zentrales Einstiegsartefakt ab.

- `Feature-Spec`: `_devprocess/requirements/features/FEATURE-{EPIC}-{NNN}-{slug}.md`
  (EPIC = 3-stellige Epic-Nummer, NNN = 3-stellige Feature-Nummer lokal
  zum Epic -- Epic 001 ergibt FEATURE-001-001, FEATURE-001-002, ...;
  Epic 013 ergibt FEATURE-013-001, ...)
- `Epic`: `_devprocess/requirements/epics/EPIC-{NNN}-{slug}.md`
- `ADR`: `_devprocess/architecture/ADR-{NNN}-{slug}.md` (mehrere kommasepariert)
- `Commit`: Short-SHA nach Abschluss
- `Evidence`: `path/file.ts:LineNN` bei Code-Referenzen

---

## Schreibregeln fuer Agents (verbindlich)

Dieses Template ist **Single Source of Truth fuer den Projektstand**. Nach
jeder Status-aendernden Aktion MUSS der ausfuehrende Agent das Backlog
aktualisieren, bevor die Phase oder der Schritt als abgeschlossen gilt.

**Was zaehlt als Status-aendernde Aktion:**

- Neuer Eintrag angelegt (Feature, Chore, Finding, Idee)
- Status-Uebergang (`Planned -> Active`, `Active -> Review`, ...)
- Prioritaet oder Epic-Zuordnung geaendert
- Implementierung abgeschlossen (Status `Done` + Commit-SHA)
- Item deferred, blockiert, abgebrochen oder wieder aktiviert
- Bug als Backlog-Item verlinkt oder geschlossen

**Ablauf pro Write:**

1. Zeile in der passenden Sektion aktualisieren oder anhaengen
2. Dashboard-Counts neu zaehlen und beide Tabellen updaten
3. Kopfzeile "Letztes Update" auf heutiges Datum und eigene Kennung setzen
4. Bei `Status = Done`: Commit-SHA eintragen, Eintrag bleibt beim Epic
5. IDs sind monoton, werden nie wiederverwendet

**Verboten:**

- Bug-Eintraege volltextlich ins Backlog schreiben (nur Referenz-Zeile)
- Items beim Done-Uebergang loeschen oder verschieben (bleiben beim Epic)
- Backlog-Write ohne Dashboard-Count-Update
- Mehrere Agents schreiben gleichzeitig ohne Rebase auf aktuellen Stand
